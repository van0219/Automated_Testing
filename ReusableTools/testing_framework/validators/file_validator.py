"""File validator for SFTP file existence checks"""

from typing import Dict, Any
from .base import BaseValidator
from ..engine.test_state import TestState
from ..engine.results import ValidationResult
from ..integration.sftp_client import SFTPClient
from ..utils.logger import Logger


class FileValidator(BaseValidator):
    """
    Validate file existence on SFTP server.
    
    Checks if specified file exists at given path.
    """
    
    def __init__(self, sftp_client: SFTPClient, logger: Logger = None):
        """
        Initialize file validator.
        
        Args:
            sftp_client: SFTP client instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.sftp_client = sftp_client
    
    def validate(self, config: Dict[str, Any], state: TestState) -> ValidationResult:
        """
        Check if file exists on SFTP.
        
        Config:
        - path: SFTP file path
        
        Returns:
            ValidationResult with passed=True if file exists
        """
        try:
            # Extract configuration
            path = config.get('path')
            if not path:
                return ValidationResult(
                    passed=False,
                    message="Missing required field: path",
                    details={'error': 'path field is required'}
                )
            
            if self.logger:
                self.logger.debug(f"Validating file existence: {path}")
            
            # Check if file exists
            exists = self.sftp_client.file_exists(path)
            
            if exists:
                if self.logger:
                    self.logger.info(f"File validation passed: {path} exists")
                
                return ValidationResult(
                    passed=True,
                    message=f"File exists: {path}",
                    details={'path': path, 'exists': True}
                )
            else:
                if self.logger:
                    self.logger.warning(f"File validation failed: {path} does not exist")
                
                return ValidationResult(
                    passed=False,
                    message=f"File does not exist: {path}",
                    details={'path': path, 'exists': False}
                )
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"File validation error: {str(e)}")
            
            return ValidationResult(
                passed=False,
                message=f"File validation failed: {str(e)}",
                details={'error': str(e), 'path': config.get('path')}
            )
