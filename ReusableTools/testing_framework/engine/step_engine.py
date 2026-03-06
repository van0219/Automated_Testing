"""Step execution engine with pluggable action handlers"""

from typing import Dict, Any, Optional
from .test_state import TestState
from .validator_engine import ValidatorEngine
from .results import StepResult, ActionResult
from ..evidence.screenshot_manager import ScreenshotManager
from ..utils.exceptions import ActionError
from ..utils.logger import Logger


class StepEngine:
    """
    Orchestrate test step execution with pluggable actions.
    
    Provides centralized step execution with:
    - State variable interpolation
    - Action routing
    - Validation execution
    - Screenshot capture
    """
    
    def __init__(
        self,
        state: TestState,
        validator_engine: ValidatorEngine,
        screenshot_manager: ScreenshotManager,
        logger: Optional[Logger] = None
    ):
        """
        Initialize step engine.
        
        Args:
            state: TestState instance for variable management
            validator_engine: ValidatorEngine for validation routing
            screenshot_manager: ScreenshotManager for evidence capture
            logger: Optional logger instance
        """
        self.state = state
        self.validator_engine = validator_engine
        self.screenshot_manager = screenshot_manager
        self.logger = logger
        self._action_handlers: Dict[str, Any] = {}
        self._register_default_handlers()
    
    def register_action(self, action_type: str, handler: Any) -> None:
        """
        Register custom action handler.
        
        Args:
            action_type: Action type identifier (e.g., 'sftp_upload', 'wait', 'api_call')
            handler: Action handler instance (must have execute method)
        """
        if self.logger:
            self.logger.debug(f"Registering action handler: {action_type}")
        
        self._action_handlers[action_type] = handler
    
    def execute_step(self, step_config: Dict[str, Any]) -> StepResult:
        """
        Execute single test step with action, validation, and screenshot.
        
        Args:
            step_config: Step configuration with number, description, action, validation, screenshot
        
        Returns:
            StepResult with action result, validation result, and screenshot path
        
        Raises:
            ValueError: If action type is unknown
            ActionError: If action execution fails
        """
        step_number = step_config.get('number', 0)
        description = step_config.get('description', '')
        
        if self.logger:
            self.logger.info(f"Executing step {step_number}: {description}")
        
        try:
            # 1. Interpolate state variables in step config
            interpolated_config = self.state.interpolate(step_config)
            
            # 2. Extract action configuration
            action_config = interpolated_config.get('action', {})
            action_type = action_config.get('type')
            
            if not action_type:
                raise ValueError("Step configuration missing action type")
            
            # 3. Route to action handler
            if action_type not in self._action_handlers:
                raise ValueError(f"Unknown action type: {action_type}")
            
            handler = self._action_handlers[action_type]
            
            if self.logger:
                self.logger.debug(f"Executing action: {action_type}")
            
            # 4. Execute action
            action_result = handler.execute(action_config, self.state)
            
            # 5. Update state with action results
            if action_result.state_updates:
                for key, value in action_result.state_updates.items():
                    self.state.set(key, value)
                    if self.logger:
                        self.logger.debug(f"State updated: {key} = {value}")
            
            # 6. Capture screenshot if configured
            screenshot_path = None
            screenshot_name = interpolated_config.get('screenshot')
            if screenshot_name:
                screenshot_path = self.screenshot_manager.capture(step_number, screenshot_name)
            
            # 7. Execute validation if configured
            validation_result = None
            validation_config = interpolated_config.get('validation')
            if validation_config:
                validation_result = self.validator_engine.validate(validation_config)
            
            # 8. Build and return StepResult
            passed = action_result.success
            if validation_result:
                passed = passed and validation_result.passed
            
            result = StepResult(
                step_number=step_number,
                description=description,
                action_result=action_result,
                validation_result=validation_result,
                screenshot_path=screenshot_path,
                passed=passed
            )
            
            if self.logger:
                status = "PASSED" if passed else "FAILED"
                self.logger.info(f"Step {step_number} {status}: {description}")
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Step {step_number} failed: {str(e)}")
            
            # Return failure result
            return StepResult(
                step_number=step_number,
                description=description,
                action_result=ActionResult(
                    success=False,
                    message=f"Step execution failed: {str(e)}"
                ),
                validation_result=None,
                screenshot_path=None,
                passed=False
            )
    
    def _register_default_handlers(self) -> None:
        """
        Register built-in action handlers.
        
        Note: Action handlers will be registered when they are implemented.
        For now, this is a placeholder.
        """
        # Action handlers will be registered here once implemented:
        # - SFTPUploadAction
        # - WaitAction
        # - APICallAction
        
        if self.logger:
            self.logger.debug("Default action handlers registered")
