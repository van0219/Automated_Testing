"""Credential management for secure access to FSM, SFTP, and APIs"""

import json
from pathlib import Path
from typing import Dict, Any
from ..utils.exceptions import ConfigurationError


class CredentialManager:
    """
    Manages credentials for FSM, SFTP, and ION API access.
    
    Reads credentials from Credentials/ folder at runtime.
    NEVER logs or commits credentials.
    """
    
    def __init__(self, credentials_dir: Path = None):
        """
        Initialize credential manager.
        
        Args:
            credentials_dir: Path to credentials directory (default: Credentials/)
        """
        self.credentials_dir = credentials_dir or Path("Credentials")
        
        if not self.credentials_dir.exists():
            raise ConfigurationError(f"Credentials directory not found: {self.credentials_dir}")
    
    def get_fsm_credentials(self, environment: str) -> Dict[str, str]:
        """
        Get FSM login credentials for environment.
        
        Args:
            environment: Environment name (e.g., 'ACUITY_TST')
        
        Returns:
            Dict with 'url', 'username', 'password'
        """
        env_file = self.credentials_dir / ".env.fsm"
        password_file = self.credentials_dir / ".env.passwords"
        
        if not env_file.exists():
            raise ConfigurationError(f"FSM credentials file not found: {env_file}")
        if not password_file.exists():
            raise ConfigurationError(f"Password file not found: {password_file}")
        
        # Parse .env.fsm
        creds = {}
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if f'{environment}_URL=' in line:
                    creds['url'] = line.split('=', 1)[1].strip()
                elif f'{environment}_USERNAME=' in line:
                    creds['username'] = line.split('=', 1)[1].strip()
        
        # Parse .env.passwords
        with open(password_file, 'r') as f:
            for line in f:
                line = line.strip()
                if f'{environment}_PASSWORD=' in line:
                    creds['password'] = line.split('=', 1)[1].strip()
        
        # Validate
        required = ['url', 'username', 'password']
        missing = [k for k in required if k not in creds]
        if missing:
            raise ConfigurationError(f"Missing FSM credentials for {environment}: {missing}")
        
        return creds
    
    def get_ionapi_config(self, environment: str) -> Dict[str, Any]:
        """
        Get ION API OAuth credentials for environment.
        
        Args:
            environment: Environment/tenant name (e.g., 'ACUITY_TST')
        
        Returns:
            Dict with ION API configuration
        """
        ionapi_file = self.credentials_dir / f"{environment}.ionapi"
        
        if not ionapi_file.exists():
            raise ConfigurationError(f"ION API credentials not found: {ionapi_file}")
        
        with open(ionapi_file, 'r') as f:
            config = json.load(f)
        
        return config
    
    def get_sftp_credentials(self, environment: str = None) -> Dict[str, str]:
        """
        Get SFTP credentials.
        
        Args:
            environment: Optional environment name
        
        Returns:
            Dict with 'host', 'username', 'password', 'inbound_path', 'outbound_path'
        """
        password_file = self.credentials_dir / ".env.passwords"
        
        if not password_file.exists():
            raise ConfigurationError(f"Password file not found: {password_file}")
        
        creds = {}
        with open(password_file, 'r') as f:
            for line in f:
                line = line.strip()
                if 'SFTP_HOST=' in line:
                    creds['host'] = line.split('=', 1)[1].strip()
                elif 'SFTP_USERNAME=' in line:
                    creds['username'] = line.split('=', 1)[1].strip()
                elif 'SFTP_PASSWORD=' in line:
                    creds['password'] = line.split('=', 1)[1].strip()
                elif 'SFTP_INBOUND_PATH=' in line:
                    creds['inbound_path'] = line.split('=', 1)[1].strip()
                elif 'SFTP_OUTBOUND_PATH=' in line:
                    creds['outbound_path'] = line.split('=', 1)[1].strip()
        
        # Validate
        required = ['host', 'username', 'password']
        missing = [k for k in required if k not in creds]
        if missing:
            raise ConfigurationError(f"Missing SFTP credentials: {missing}")
        
        return creds
