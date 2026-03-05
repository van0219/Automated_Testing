"""Base validator interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..engine.test_state import TestState
from ..engine.results import ValidationResult
from ..utils.logger import Logger


class BaseValidator(ABC):
    """
    Base class for validators.
    
    All validators must inherit from this class and implement
    the validate method.
    """
    
    def __init__(self, logger: Optional[Logger] = None):
        """
        Initialize base validator.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger
    
    @abstractmethod
    def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
        """
        Execute validation and return result.
        
        Args:
            config: Validation configuration dictionary
            state: TestState instance for variable access
        
        Returns:
            ValidationResult with passed status, message, and details
        
        Raises:
            ValidationError: If validation encounters an error
        """
        pass
