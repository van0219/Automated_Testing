"""Validation engine for routing validation requests"""

from typing import Dict, Any, Optional
from .test_state import TestState
from .results import ValidationResult
from ..utils.exceptions import ValidationError
from ..utils.logger import Logger


class ValidatorEngine:
    """
    Route validation requests to specialized validators.
    
    Provides pluggable architecture for validators with automatic routing
    based on validation type.
    """
    
    def __init__(self, state: TestState, logger: Optional[Logger] = None):
        """
        Initialize validator engine.
        
        Args:
            state: TestState instance for variable access
            logger: Optional logger instance
        """
        self.state = state
        self.logger = logger
        self._validators: Dict[str, Any] = {}
        self._register_default_validators()
    
    def register_validator(self, validator_type: str, validator: Any) -> None:
        """
        Register custom validator.
        
        Args:
            validator_type: Validator type identifier (e.g., 'file', 'api', 'workunit')
            validator: Validator instance (must have validate method)
        """
        if self.logger:
            self.logger.debug(f"Registering validator: {validator_type}")
        
        self._validators[validator_type] = validator
    
    def validate(self, validation_config: Dict[str, Any]) -> ValidationResult:
        """
        Execute validation and return result.
        
        Args:
            validation_config: Validation configuration with 'type' and validator-specific fields
        
        Returns:
            ValidationResult with pass/fail status
        
        Raises:
            ValueError: If validation type is unknown
            ValidationError: If validation encounters an error
        """
        # Extract validation type
        validation_type = validation_config.get('type')
        if not validation_type:
            raise ValueError("Validation configuration missing 'type' field")
        
        # Check if validator is registered
        if validation_type not in self._validators:
            raise ValueError(f"Unknown validation type: {validation_type}")
        
        # Get validator
        validator = self._validators[validation_type]
        
        if self.logger:
            self.logger.info(f"Executing validation: {validation_type}")
        
        try:
            # Execute validation
            result = validator.validate(validation_config, self.state)
            
            # Log result
            if result.passed:
                if self.logger:
                    self.logger.info(f"Validation passed: {validation_type} - {result.message}")
            else:
                if self.logger:
                    self.logger.warning(f"Validation failed: {validation_type} - {result.message}")
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Validation error: {validation_type} - {str(e)}")
            
            # Return failure result
            return ValidationResult(
                passed=False,
                message=f"Validation failed: {str(e)}",
                details={'error': str(e), 'type': validation_type}
            )
    
    def _register_default_validators(self) -> None:
        """
        Register built-in validators.
        
        Note: Validators will be registered when they are implemented.
        For now, this is a placeholder.
        """
        # Validators will be registered here once implemented:
        # - FileValidator
        # - WorkUnitValidator
        # - APIValidator
        
        if self.logger:
            self.logger.debug("Default validators registered")
