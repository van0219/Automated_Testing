"""API validator for FSM data verification"""

from typing import Dict, Any, List
from .base import BaseValidator
from ..engine.test_state import TestState
from ..engine.results import ValidationResult
from ..integration.fsm_api_client import FSMAPIClient
from ..utils.logger import Logger


class APIValidator(BaseValidator):
    """
    Validate FSM data via API queries.
    
    Supports record count, status, and field value validations.
    """
    
    def __init__(self, fsm_api_client: FSMAPIClient, logger: Logger = None):
        """
        Initialize API validator.
        
        Args:
            fsm_api_client: FSM API client instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.fsm_api_client = fsm_api_client
    
    def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
        """
        Validate data via FSM API.
        
        Config:
        - business_class: Business class name
        - filters: Query filters
        - expected_count: Expected record count (optional)
        - expected_status: Expected status value (optional)
        - field_validations: List of field validations (optional)
        
        Returns:
            ValidationResult with passed=True if all validations pass
        """
        try:
            # Extract configuration
            business_class = config.get('business_class')
            filters = config.get('filters', {})
            expected_count = config.get('expected_count')
            expected_status = config.get('expected_status')
            field_validations = config.get('field_validations', [])
            
            if not business_class:
                return ValidationResult(
                    passed=False,
                    message="Missing required field: business_class",
                    details={'error': 'business_class is required'}
                )
            
            if self.logger:
                self.logger.debug(f"Validating API data: {business_class}")
            
            # Query records
            records = self.fsm_api_client.list_records(business_class, filters)
            actual_count = len(records)
            
            # Track validation failures
            failures = []
            
            # Validate record count
            if expected_count is not None:
                if actual_count != expected_count:
                    failures.append(
                        f"Record count mismatch: expected {expected_count}, got {actual_count}"
                    )
            
            # Validate status (if records exist)
            if expected_status is not None and records:
                for i, record in enumerate(records):
                    record_status = record.get('Status')
                    if record_status != expected_status:
                        failures.append(
                            f"Record {i} status mismatch: expected {expected_status}, got {record_status}"
                        )
            
            # Validate field values
            for validation in field_validations:
                field = validation.get('field')
                operator = validation.get('operator', 'equals')
                value = validation.get('value')
                
                if not field:
                    continue
                
                for i, record in enumerate(records):
                    field_value = record.get(field)
                    
                    if operator == 'equals':
                        if field_value != value:
                            failures.append(
                                f"Record {i} field {field}: expected {value}, got {field_value}"
                            )
                    elif operator == 'not_equals':
                        if field_value == value:
                            failures.append(
                                f"Record {i} field {field}: should not equal {value}"
                            )
                    elif operator == 'greater_than':
                        if not (field_value and field_value > value):
                            failures.append(
                                f"Record {i} field {field}: expected > {value}, got {field_value}"
                            )
                    elif operator == 'less_than':
                        if not (field_value and field_value < value):
                            failures.append(
                                f"Record {i} field {field}: expected < {value}, got {field_value}"
                            )
                    elif operator == 'contains':
                        if not (field_value and value in str(field_value)):
                            failures.append(
                                f"Record {i} field {field}: expected to contain {value}, got {field_value}"
                            )
            
            # Return result
            if failures:
                if self.logger:
                    self.logger.warning(f"API validation failed: {len(failures)} failures")
                
                return ValidationResult(
                    passed=False,
                    message=f"API validation failed: {len(failures)} validation(s) failed",
                    details={
                        'business_class': business_class,
                        'actual_count': actual_count,
                        'expected_count': expected_count,
                        'failures': failures
                    }
                )
            else:
                if self.logger:
                    self.logger.info(f"API validation passed: {business_class}")
                
                return ValidationResult(
                    passed=True,
                    message=f"API validation passed: {actual_count} records validated",
                    details={
                        'business_class': business_class,
                        'record_count': actual_count
                    }
                )
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"API validation error: {str(e)}")
            
            return ValidationResult(
                passed=False,
                message=f"API validation failed: {str(e)}",
                details={'error': str(e)}
            )
