"""SFTP client for file operations with connection management"""

import paramiko
from pathlib import Path
from typing import List, Optional
from ..utils.exceptions import ConnectionError as FrameworkConnectionError
from ..utils.logger import Logger


class SFTPClient:
    """
    SFTP file operations with connection management.
    
    Provides upload, download, list, and file existence checking.
    Uses paramiko for SFTP operations.
    """
    
    def __init__(self, host: str, username: str, password: str, port: int = 22, logger: Optional[Logger] = None):
        """
        Initialize SFTP client.
        
        Args:
            host: SFTP server hostname
            username: SFTP username
            password: SFTP password
            port: SFTP port (default: 22)
            logger: Optional logger instance
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.logger = logger
        
        self._transport: Optional[paramiko.Transport] = None
        self._sftp: Optional[paramiko.SFTPClient] = None
    
    def connect(self) -> None:
        """
        Establish SFTP connection.
        
        Raises:
            FrameworkConnectionError: If connection fails
        """
        try:
            if self.logger:
                self.logger.info(f"Connecting to SFTP server: {self.host}:{self.port}")
            
            # Create transport
            self._transport = paramiko.Transport((self.host, self.port))
            self._transport.connect(username=self.username, password=self.password)
            
            # Create SFTP client
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            
            if self.logger:
                self.logger.info("SFTP connection established")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"SFTP connection failed: {str(e)}")
            raise FrameworkConnectionError(f"Failed to connect to SFTP server {self.host}: {str(e)}")
    
    def disconnect(self) -> None:
        """Close SFTP connection and cleanup resources."""
        try:
            if self._sftp:
                self._sftp.close()
                self._sftp = None
            
            if self._transport:
                self._transport.close()
                self._transport = None
            
            if self.logger:
                self.logger.info("SFTP connection closed")
                
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Error closing SFTP connection: {str(e)}")
    
    def _ensure_connected(self) -> None:
        """
        Ensure SFTP connection is active.
        
        Raises:
            FrameworkConnectionError: If not connected
        """
        if not self._sftp or not self._transport or not self._transport.is_active():
            raise FrameworkConnectionError("SFTP client is not connected. Call connect() first.")
    
    def upload(self, local_path: str, remote_path: str) -> None:
        """
        Upload file to SFTP server.
        
        Args:
            local_path: Local file path
            remote_path: Remote destination path
        
        Raises:
            FrameworkConnectionError: If not connected
            FileNotFoundError: If local file does not exist
            Exception: If upload fails
        """
        self._ensure_connected()
        
        local_file = Path(local_path)
        if not local_file.exists():
            raise FileNotFoundError(f"Local file not found: {local_path}")
        
        try:
            if self.logger:
                self.logger.info(f"Uploading file: {local_path} -> {remote_path}")
            
            self._sftp.put(str(local_file), remote_path)
            
            if self.logger:
                self.logger.info(f"File uploaded successfully: {remote_path}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"File upload failed: {str(e)}")
            raise Exception(f"Failed to upload file to {remote_path}: {str(e)}")
    
    def download(self, remote_path: str, local_path: str) -> None:
        """
        Download file from SFTP server.
        
        Args:
            remote_path: Remote file path
            local_path: Local destination path
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If download fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.info(f"Downloading file: {remote_path} -> {local_path}")
            
            # Create local directory if needed
            local_file = Path(local_path)
            local_file.parent.mkdir(parents=True, exist_ok=True)
            
            self._sftp.get(remote_path, str(local_file))
            
            if self.logger:
                self.logger.info(f"File downloaded successfully: {local_path}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"File download failed: {str(e)}")
            raise Exception(f"Failed to download file from {remote_path}: {str(e)}")
    
    def list_files(self, remote_dir: str) -> List[str]:
        """
        List files in remote directory.
        
        Args:
            remote_dir: Remote directory path
        
        Returns:
            List of filenames in directory
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If listing fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.debug(f"Listing files in directory: {remote_dir}")
            
            files = self._sftp.listdir(remote_dir)
            
            if self.logger:
                self.logger.debug(f"Found {len(files)} files in {remote_dir}")
            
            return files
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to list files in {remote_dir}: {str(e)}")
            raise Exception(f"Failed to list files in {remote_dir}: {str(e)}")
    
    def file_exists(self, remote_path: str) -> bool:
        """
        Check if file exists on SFTP server.
        
        Args:
            remote_path: Remote file path
        
        Returns:
            True if file exists, False otherwise
        
        Raises:
            FrameworkConnectionError: If not connected
        """
        self._ensure_connected()
        
        try:
            self._sftp.stat(remote_path)
            if self.logger:
                self.logger.debug(f"File exists: {remote_path}")
            return True
        except FileNotFoundError:
            if self.logger:
                self.logger.debug(f"File does not exist: {remote_path}")
            return False
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Error checking file existence: {str(e)}")
            return False
    
    def __enter__(self):
        """Context manager entry - connect to SFTP."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - disconnect from SFTP."""
        self.disconnect()
        return False
