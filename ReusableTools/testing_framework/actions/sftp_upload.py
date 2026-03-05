"""SFTP upload action handler"""

from pathlib import Path
from typing import Dict, Any
from .base import BaseAction
from ..engine.test_state import TestState
from ..engine.results import ActionResult
from ..integration.sftp_client import SFTPClient
from ..utils.exceptions import ActionError
from ..utils.logger import Logger


class SFTPUploadAction(BaseAction):
    """
    Upload test data files to SFTP server.
    
    Uploads files from TestScripts/test_data/ directory to SFTP destination.
    """
    
    def __init__(self, sftp_client: SFTPClient, client_name: str, logger: Logger = None):
        """
        Initialize SFTP upload action.
        
        Args:
            sftp_client: SFTP client instance
            client_name: Client name for path construction
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.sftp_client = sftp_client
        self.client_name = client_name
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Upload file to SFTP.
        
        Config:
        - test_data_file: Filename in TestScripts/test_data/
        - destination_path: SFTP destination path
        
        Returns:
            ActionResult with state_updates: uploaded_file, sftp_destination
        
        Raises:
            ActionError: If upload fails
        """
        try:
            # Extract configuration
            test_data_file = config.get('test_data_file')
            destination_path = config.get('destination_path')
            
            if not test_data_file:
                raise ActionError("Missing required field: test_data_file")
            if not destination_path:
                raise ActionError("Missing required field: destination_path")
            
            # Construct source path
            source_path = Path("Projects") / self.client_name / "TestScripts" / "test_data" / test_data_file
            
            # Validate source file exists
            if not source_path.exists():
                raise ActionError(f"Test data file not found: {source_path}")
            
            if self.logger:
                self.logger.info(f"Uploading file: {source_path} -> {destination_path}")
            
            # Upload file
            self.sftp_client.upload(str(source_path), destination_path)
            
            if self.logger:
                self.logger.info(f"File uploaded successfully: {destination_path}")
            
            # Return success result
            return ActionResult(
                success=True,
                message=f"File uploaded: {test_data_file}",
                state_updates={
                    'uploaded_file': test_data_file,
                    'sftp_destination': destination_path
                }
            )
            
        except ActionError:
            raise
        except Exception as e:
            if self.logger:
                self.logger.error(f"SFTP upload failed: {str(e)}")
            raise ActionError(f"Failed to upload file: {str(e)}")
