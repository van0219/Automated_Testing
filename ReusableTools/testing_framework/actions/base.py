"""Base action handler interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..engine.test_state import TestState
from ..engine.results import ActionResult
from ..utils.logger import Logger


class BaseAction(ABC):
    """
    Base class for action handlers.
    
    All action handlers must inherit from this class and implement
    the execute method.
    """
    
    def __init__(self, logger: Optional[Logger] = None):
        """
        Initialize base action.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger
    
    @abstractmethod
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Execute action and return result.
        
        Args:
            config: Action configuration dictionary
            state: TestState instance for variable access
        
        Returns:
            ActionResult with status, message, data, and state_updates
        
        Raises:
            ActionError: If action execution fails
        """
        pass
