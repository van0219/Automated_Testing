"""FSM API client with OAuth2 authentication"""

import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from ..utils.exceptions import ConnectionError as FrameworkConnectionError
from ..utils.logger import Logger


class FSMAPIClient:
    """
    FSM API operations with OAuth2 authentication.
    
    Provides business class operations (List, Get, Add, Update, Delete)
    with automatic token management and retry logic.
    """
    
    def __init__(
        self,
        ionapi_config: Dict[str, Any],
        context_fields: Dict[str, str],
        logger: Optional[Logger] = None
    ):
        """
        Initialize FSM API client.
        
        Args:
            ionapi_config: ION API configuration from .ionapi file
            context_fields: Required context fields (FinanceEnterpriseGroup, AccountingEntity, etc.)
            logger: Optional logger instance
        """
        self.ionapi_config = ionapi_config
        self.context_fields = context_fields
        self.logger = logger
        
        # OAuth2 token management
        self._token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        
        # API endpoint
        self._base_url = ionapi_config.get('oa', '')
        if not self._base_url:
            raise FrameworkConnectionError("ION API base URL not found in configuration")
    
    def _get_token(self) -> str:
        """
        Obtain OAuth2 token from ION.
        
        Returns:
            Access token
        
        Raises:
            FrameworkConnectionError: If token request fails
        """
        try:
            if self.logger:
                self.logger.info("Requesting OAuth2 token from ION")
            
            token_url = self.ionapi_config.get('iu', '')
            client_id = self.ionapi_config.get('ci', '')
            client_secret = self.ionapi_config.get('cs', '')
            
            if not all([token_url, client_id, client_secret]):
                raise FrameworkConnectionError("Missing OAuth2 credentials in ION API configuration")
            
            # Request token
            response = requests.post(
                token_url,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': client_id,
                    'client_secret': client_secret
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            self._token = token_data.get('access_token')
            expires_in = token_data.get('expires_in', 3600)  # Default 1 hour
            
            # Set expiry time
            self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            if self.logger:
                self.logger.info(f"OAuth2 token obtained (expires in {expires_in}s)")
            
            return self._token
            
        except requests.exceptions.RequestException as e:
            if self.logger:
                self.logger.error(f"OAuth2 token request failed: {str(e)}")
            raise FrameworkConnectionError(f"Failed to obtain OAuth2 token: {str(e)}")
    
    def _refresh_token_if_needed(self) -> None:
        """
        Refresh token if expiring within 10 minutes.
        
        Proactive refresh strategy to avoid mid-request expiration.
        """
        if not self._token or not self._token_expiry:
            self._get_token()
            return
        
        # Refresh if expiring within 10 minutes
        time_until_expiry = (self._token_expiry - datetime.now()).total_seconds()
        if time_until_expiry < 600:  # 10 minutes
            if self.logger:
                self.logger.info(f"Token expiring in {time_until_expiry:.0f}s, refreshing...")
            self._get_token()
    
    def _call_api(
        self,
        business_class: str,
        action: str,
        data: Optional[Dict[str, Any]] = None,
        retry_on_401: bool = True
    ) -> Dict[str, Any]:
        """
        Call FSM API with automatic token refresh.
        
        Args:
            business_class: Business class name (e.g., 'POSInventoryInterface')
            action: API action (List, Get, Add, Update, Delete)
            data: Request payload data
            retry_on_401: Whether to retry once on 401 error
        
        Returns:
            API response as dictionary
        
        Raises:
            FrameworkConnectionError: If API call fails
        """
        self._refresh_token_if_needed()
        
        # Build request payload
        payload = {
            '_actionName': action,
            '_objectName': business_class,
            '_module': 'pfi',  # Process Flow Integrator module
            **self.context_fields
        }
        
        # Add data fields if provided
        if data:
            payload.update(data)
        
        # Build endpoint URL
        endpoint = f"{self._base_url}/{business_class}/{action}"
        
        try:
            if self.logger:
                self.logger.debug(f"Calling FSM API: {action} {business_class}")
            
            response = requests.post(
                endpoint,
                json=payload,
                headers={
                    'Authorization': f'Bearer {self._token}',
                    'Content-Type': 'application/json'
                }
            )
            
            # Handle 401 - token expired
            if response.status_code == 401 and retry_on_401:
                if self.logger:
                    self.logger.warning("Received 401, refreshing token and retrying...")
                self._get_token()
                # Retry once with new token
                return self._call_api(business_class, action, data, retry_on_401=False)
            
            response.raise_for_status()
            result = response.json()
            
            if self.logger:
                self.logger.debug(f"FSM API call successful: {action} {business_class}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            if self.logger:
                self.logger.error(f"FSM API call failed: {str(e)}")
            raise FrameworkConnectionError(f"FSM API call failed ({action} {business_class}): {str(e)}")
    
    def list_records(
        self,
        business_class: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        List records from business class.
        
        Args:
            business_class: Business class name
            filters: Optional filter criteria
        
        Returns:
            List of records
        
        Raises:
            FrameworkConnectionError: If API call fails
        """
        if self.logger:
            self.logger.info(f"Listing records from {business_class}")
        
        result = self._call_api(business_class, 'List', filters)
        
        # Extract records from response
        records = result.get('items', [])
        
        if self.logger:
            self.logger.info(f"Retrieved {len(records)} records from {business_class}")
        
        return records
    
    def get_record(self, business_class: str, record_id: str) -> Dict[str, Any]:
        """
        Get single record by ID.
        
        Args:
            business_class: Business class name
            record_id: Record ID
        
        Returns:
            Record data
        
        Raises:
            FrameworkConnectionError: If API call fails
        """
        if self.logger:
            self.logger.info(f"Getting record {record_id} from {business_class}")
        
        result = self._call_api(business_class, 'Get', {'id': record_id})
        
        return result
    
    def add_record(self, business_class: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add new record.
        
        Args:
            business_class: Business class name
            data: Record data
        
        Returns:
            Created record data
        
        Raises:
            FrameworkConnectionError: If API call fails
        """
        if self.logger:
            self.logger.info(f"Adding record to {business_class}")
        
        result = self._call_api(business_class, 'Add', data)
        
        if self.logger:
            self.logger.info(f"Record added to {business_class}")
        
        return result
    
    def update_record(
        self,
        business_class: str,
        record_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update existing record.
        
        Args:
            business_class: Business class name
            record_id: Record ID
            data: Updated record data
        
        Returns:
            Updated record data
        
        Raises:
            FrameworkConnectionError: If API call fails
        """
        if self.logger:
            self.logger.info(f"Updating record {record_id} in {business_class}")
        
        data['id'] = record_id
        result = self._call_api(business_class, 'Update', data)
        
        if self.logger:
            self.logger.info(f"Record updated in {business_class}")
        
        return result
    
    def delete_record(self, business_class: str, record_id: str) -> Dict[str, Any]:
        """
        Delete record.
        
        Args:
            business_class: Business class name
            record_id: Record ID
        
        Returns:
            Deletion result
        
        Raises:
            FrameworkConnectionError: If API call fails
        """
        if self.logger:
            self.logger.info(f"Deleting record {record_id} from {business_class}")
        
        result = self._call_api(business_class, 'Delete', {'id': record_id})
        
        if self.logger:
            self.logger.info(f"Record deleted from {business_class}")
        
        return result
