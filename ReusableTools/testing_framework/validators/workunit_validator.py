"""Work unit validator for status verification"""

from typing import Dict, Any
from .base import BaseValidator
from ..engine.test_state import TestState
from ..engine.results import ValidationResult
from ..integration.workunit_monitor import WorkUnitMonitor
from ..utils.logger import Logger


class WorkUnitValidator(BaseValidator):
    """
    Validate work unit status.
    
    Checks if work unit has expected status.
    """
    
    def __init__(self, workunit_monitor: WorkUnitMonitor, logger: Logger = None):
        """
        Initialize work unit validator.
        
        Args:
            workunit_monitor: WorkUnitMonitor instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.workunit_monitor = workunit_monitor
    
    def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
        """
        Validate work unit status.
        
        Config:
        - work_unit_id: Work unit ID (or read from state)
        - expected_status: Expected status value
        
        Returns:
            ValidationResult with passed=True if status matches
        """
        try:
            # Extract configuration
            work_unit_id = config.get('work_unit_id') or state.get('work_unit_id')
            expected_status = config.get('expected_status')
            
            if not work_unit_id:
                return ValidationResult(
                    passed=False,
                    message="work_unit_id not found in config or state",
                    details={'error': 'work_unit_id is required'}
                )
            
            if not expected_status:
                return ValidationResult(
                    passed=False,
                    message="Missing required field: expected_status",
                    details={'error': 'expected_status is required'}
                )
            
            if self.logger:
                self.logger.debug(f"Validating work unit status: {work_unit_id}")
            
            # Get work unit status
            # Note: This is a simplified implementation
            # Real implementation would use WorkUnitMonitor to get current status
            actual_status = state.get('work_unit_status', 'Unknown')
            
            # Compare status
            if actual_status == expected_status:
                if self.logger:
                    self.logger.info(
                        f"Work unit validation passed: {work_unit_id} "
                        f"status={actual_status}"
                    )
                
                return ValidationResult(
                    passed=True,
                    message=f"Work unit status matches: {actual_status}",
                    details={
                        'work_unit_id': work_unit_id,
                        'expected_status': expected_status,
                        'actual_status': actual_status
                    }
                )
            else:
                if self.logger:
                    self.logger.warning(
                        f"Work unit validation failed: {work_unit_id} "
                        f"expected={expected_status}, actual={actual_status}"
                    )
                
                return ValidationResult(
                    passed=False,
                    message=f"Work unit status mismatch: expected {expected_status}, got {actual_status}",
                    details={
                        'work_unit_id': work_unit_id,
                        'expected_status': expected_status,
                        'actual_status': actual_status
                    }
                )
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Work unit validation error: {str(e)}")
            
            return ValidationResult(
                passed=False,
                message=f"Work unit validation failed: {str(e)}",
                details={'error': str(e)}
            )
