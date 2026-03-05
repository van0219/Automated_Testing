"""Approval workflow test executor"""

from typing import Dict, Any
from ..engine.test_state import TestState
from ..engine.step_engine import StepEngine
from ..engine.results import ScenarioResult, StepResult
from ..utils.logger import Logger


class ApprovalExecutor:
    """
    Execute approval workflow test scenarios.
    
    Handles FSM approval flow testing with:
    - Login and navigation
    - Invoice/transaction creation
    - Approval submission
    - Work unit monitoring
    - Status verification
    """
    
    def __init__(
        self,
        step_engine: StepEngine,
        state: TestState,
        logger: Logger
    ):
        """
        Initialize approval executor.
        
        Args:
            step_engine: StepEngine instance
            state: TestState instance
            logger: Logger instance
        """
        self.step_engine = step_engine
        self.state = state
        self.logger = logger
    
    def execute_scenario(self, scenario: Dict[str, Any]) -> ScenarioResult:
        """
        Execute single approval scenario.
        
        Args:
            scenario: Scenario configuration with steps
        
        Returns:
            ScenarioResult with pass/fail status
        """
        scenario_id = scenario.get('scenario_id', 'Unknown')
        title = scenario.get('title', 'Untitled')
        steps = scenario.get('steps', [])
        
        self.logger.info(f"Executing approval scenario: {scenario_id} - {title}")
        
        # Initialize state for this scenario
        self.state.initialize_run_group()
        
        # Load password from credentials
        # This should be loaded from credential manager
        # For now, we'll set it in state
        self.state.set('password', 'L@ws0n678')  # TODO: Load from credential manager
        
        # Execute steps
        step_results = []
        all_passed = True
        
        for step_config in steps:
            step_number = step_config.get('number')
            description = step_config.get('description', '')
            action_config = step_config.get('action', {})
            expected_result = step_config.get('expected_result', '')
            
            self.logger.info(f"Step {step_number}: {description}")
            
            try:
                # Execute step - pass the full step config to StepEngine
                action_result = self.step_engine.execute_step(step_config)
                
                # Build step result from StepEngine result
                step_result = StepResult(
                    step_number=str(step_number),
                    description=description,
                    action_result=action_result.action_result if hasattr(action_result, 'action_result') else None,
                    passed=action_result.passed if hasattr(action_result, 'passed') else False,
                    screenshot_path=action_result.screenshot_path if hasattr(action_result, 'screenshot_path') else None
                )
                
                step_results.append(step_result)
                
                if not step_result.passed:
                    all_passed = False
                    error_msg = step_result.error if hasattr(step_result, 'error') else 'Unknown error'
                    self.logger.error(f"Step {step_number} failed: {error_msg}")
                    # Continue to next step even if this one failed
                else:
                    self.logger.info(f"Step {step_number} passed")
                
            except Exception as e:
                self.logger.error(f"Step {step_number} error: {str(e)}")
                
                step_result = StepResult(
                    step_number=str(step_number),
                    description=description,
                    passed=False,
                    error=str(e),
                    screenshot_path=step_config.get('screenshot')
                )
                
                step_results.append(step_result)
                all_passed = False
        
        # Build scenario result
        result = ScenarioResult(
            scenario_id=scenario_id,
            title=title,
            step_results=step_results,
            passed=all_passed
        )
        
        self.logger.info(f"Scenario {scenario_id} {'PASSED' if all_passed else 'FAILED'}")
        
        return result
