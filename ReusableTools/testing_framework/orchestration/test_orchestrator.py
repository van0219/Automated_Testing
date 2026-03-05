"""Main test orchestration engine"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from ..engine.test_state import TestState
from ..engine.step_engine import StepEngine
from ..engine.validator_engine import ValidatorEngine
from ..engine.results import TestResult
from ..integration.credential_manager import CredentialManager
from ..integration.sftp_client import SFTPClient
from ..integration.fsm_api_client import FSMAPIClient
from ..integration.playwright_client import PlaywrightMCPClient
from ..integration.workunit_monitor import WorkUnitMonitor
from ..evidence.screenshot_manager import ScreenshotManager
from ..evidence.tes070_generator import TES070Generator
from .inbound_executor import InboundExecutor
from .approval_executor import ApprovalExecutor
from ..actions.sftp_upload import SFTPUploadAction
from ..actions.wait import WaitAction
from ..actions.api_call import APICallAction
from ..actions.fsm_action_registry import register_fsm_actions
from ..validators.file_validator import FileValidator
from ..validators.workunit_validator import WorkUnitValidator
from ..validators.api_validator import APIValidator
from ..utils.exceptions import ConfigurationError
from ..utils.logger import Logger
from ..integration.ui_map_loader import UIMapLoader


class TestOrchestrator:
    """
    Coordinate end-to-end test execution.
    
    Main entry point for test framework - loads scenarios, initializes
    components, executes tests, and generates TES-070 documents.
    """
    
    def __init__(
        self,
        client_name: str,
        environment: str,
        logger: Logger
    ):
        """
        Initialize test orchestrator.
        
        Args:
            client_name: Client name for credential loading
            environment: FSM environment (e.g., 'ACUITY_TST')
            logger: Logger instance
        """
        self.client_name = client_name
        self.environment = environment
        self.logger = logger
        
        # Initialize credentials
        credentials_dir = Path("Projects") / client_name / "Credentials"
        self.credential_manager = CredentialManager(credentials_dir)
        
        # Initialize state
        self.state = TestState()
        
        # Initialize integration clients
        self._init_integration_clients()
        
        # Initialize engines
        self._init_engines()
        
        # Initialize executors
        self.inbound_executor = InboundExecutor(self.step_engine, self.state, logger)
        self.approval_executor = ApprovalExecutor(self.step_engine, self.state, logger)
    
    def _init_integration_clients(self) -> None:
        """Initialize integration clients."""
        # SFTP Client
        sftp_creds = self.credential_manager.get_sftp_credentials()
        self.sftp_client = SFTPClient(
            host=sftp_creds['host'],
            username=sftp_creds['username'],
            password=sftp_creds['password'],
            logger=self.logger
        )
        self.sftp_client.connect()
        
        # FSM API Client (optional - only needed for API-based tests)
        try:
            ionapi_config = self.credential_manager.get_ionapi_config(self.environment)
            fsm_creds = self.credential_manager.get_fsm_credentials(self.environment)
            context_fields = {
                'FinanceEnterpriseGroup': '100',  # TODO: Load from config
                'AccountingEntity': '1000',  # TODO: Load from config
                '_dataArea': self.environment
            }
            self.fsm_api_client = FSMAPIClient(ionapi_config, context_fields, self.logger)
            self.logger.info("FSM API client initialized")
        except Exception as e:
            self.logger.warning(f"FSM API client not available: {str(e)}")
            self.fsm_api_client = None
        
        # Playwright MCP Client
        self.playwright_client = PlaywrightMCPClient(self.logger)
        self.playwright_client.connect()
        
        # WorkUnit Monitor
        self.workunit_monitor = WorkUnitMonitor(self.playwright_client, self.logger)
    
    def _init_engines(self) -> None:
        """Initialize engines and register handlers."""
        # Screenshot Manager
        self.screenshot_manager = ScreenshotManager(self.playwright_client, "", self.logger)
        
        # UI Map Loader
        self.ui_map_loader = UIMapLoader(logger=self.logger)
        
        # Validator Engine
        self.validator_engine = ValidatorEngine(self.state, self.logger)
        
        # Register validators
        file_validator = FileValidator(self.sftp_client, self.logger)
        workunit_validator = WorkUnitValidator(self.workunit_monitor, self.logger)
        
        self.validator_engine.register_validator('file', file_validator)
        self.validator_engine.register_validator('workunit', workunit_validator)
        
        # Only register API validator if API client is available
        if self.fsm_api_client:
            api_validator = APIValidator(self.fsm_api_client, self.logger)
            self.validator_engine.register_validator('api', api_validator)
        
        # Step Engine
        self.step_engine = StepEngine(
            self.state,
            self.validator_engine,
            self.screenshot_manager,
            self.logger
        )
        
        # Register action handlers
        sftp_upload_action = SFTPUploadAction(self.sftp_client, self.client_name, self.logger)
        wait_action = WaitAction(self.workunit_monitor, self.logger)
        
        self.step_engine.register_action('sftp_upload', sftp_upload_action)
        self.step_engine.register_action('wait', wait_action)
        
        # Only register API action if API client is available
        if self.fsm_api_client:
            api_call_action = APICallAction(self.fsm_api_client, self.logger)
            self.step_engine.register_action('api_call', api_call_action)
        
        # Register FSM actions
        register_fsm_actions(
            step_engine=self.step_engine,
            playwright_client=self.playwright_client,
            ui_map_loader=self.ui_map_loader,
            screenshot_manager=self.screenshot_manager,
            logger=self.logger
        )
    
    def run(self, scenario_file: str) -> TestResult:
        """
        Execute test scenarios from JSON file.
        
        Args:
            scenario_file: Path to JSON test scenario file
        
        Returns:
            TestResult with overall pass/fail status
        
        Raises:
            ConfigurationError: If JSON parsing or validation fails
        """
        self.logger.info(f"Loading test scenario: {scenario_file}")
        
        # Load JSON
        try:
            with open(scenario_file, 'r') as f:
                test_data = json.load(f)
        except Exception as e:
            raise ConfigurationError(f"Failed to load scenario file: {str(e)}")
        
        # Extract metadata
        interface_id = test_data.get('interface_id', 'Unknown')
        interface_type = test_data.get('interface_type', 'inbound')
        scenarios = test_data.get('scenarios', [])
        
        self.logger.info(f"Executing test: {interface_id} ({interface_type})")
        
        # Set screenshot output directory
        self.screenshot_manager.set_output_dir(interface_id)
        
        # Select executor based on interface type
        if interface_type == 'inbound':
            executor = self.inbound_executor
        elif interface_type == 'approval':
            executor = self.approval_executor
        else:
            raise ConfigurationError(f"Unsupported interface type: {interface_type}")
        
        # Execute scenarios
        scenario_results = []
        all_passed = True
        
        for scenario in scenarios:
            self.logger.info(f"Executing scenario: {scenario.get('scenario_id')}")
            
            try:
                result = executor.execute_scenario(scenario)
                scenario_results.append(result)
                
                if not result.passed:
                    all_passed = False
                    
            except Exception as e:
                self.logger.error(f"Scenario execution failed: {str(e)}")
                all_passed = False
        
        # Generate TES-070 document
        tes070_path = None
        try:
            generator = TES070Generator(self.logger)
            tes070_path = generator.generate(
                interface_id,
                scenarios,
                scenario_results,
                str(self.screenshot_manager.output_dir)
            )
        except Exception as e:
            self.logger.error(f"TES-070 generation failed: {str(e)}")
        
        # Build final result
        result = TestResult(
            interface_id=interface_id,
            interface_name=interface_id,  # Use interface_id as name for now
            scenario_results=scenario_results,
            passed=all_passed,
            execution_time=0.0  # TODO: Track execution time
        )
        
        # Store TES-070 path in result metadata if generated
        if tes070_path:
            result.tes070_path = tes070_path
        
        self.logger.info(f"Test execution complete: {'PASSED' if all_passed else 'FAILED'}")
        
        return result
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        try:
            if self.sftp_client:
                self.sftp_client.disconnect()
            if self.playwright_client:
                self.playwright_client.close()
        except Exception as e:
            self.logger.warning(f"Cleanup error: {str(e)}")
