# -*- coding: utf-8 -*-
"""
FSM Field Discovery

Query FSM API to discover valid field names for business classes.
Uses TAMICS10_AX1 sandbox since all FSM tenants have same OOB business classes.

Usage:
    from fsm_field_discovery import discover_fsm_fields
    
    fields = discover_fsm_fields('GLTransactionInterface', credentials_dir='Projects/StateOfNewHampshire/Credentials')
    print(fields['required'])  # Required fields
    print(fields['optional'])  # Optional fields
"""

import requests
import json
from pathlib import Path
from typing import Dict, List


def load_credentials(credentials_dir: str) -> Dict[str, str]:
    """
    Load FSM credentials from .env files or .ionapi files.
    
    Args:
        credentials_dir: Path to credentials directory
    
    Returns:
        Dictionary with credentials
    """
    creds = {}
    creds_path = Path(credentials_dir)
    
    # Check for .ionapi file first (preferred for OAuth2)
    ionapi_files = list(creds_path.glob('*.ionapi'))
    if ionapi_files:
        ionapi_file = ionapi_files[0]
        with open(ionapi_file, 'r') as f:
            ionapi_data = json.load(f)
            creds['ionapi'] = ionapi_data
            creds['tenant'] = ionapi_data.get('ti', '')
            creds['client_id'] = ionapi_data.get('ci', '')
            creds['client_secret'] = ionapi_data.get('cs', '')
            creds['token_url'] = ionapi_data.get('pu', '') + ionapi_data.get('ot', '')
            creds['ionapi_url'] = ionapi_data.get('iu', '')
            return creds
    
    # Fallback to .env files
    env_fsm = creds_path / '.env.fsm'
    if env_fsm.exists():
        with open(env_fsm, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    creds[key.strip()] = value.strip()
    
    env_passwords = creds_path / '.env.passwords'
    if env_passwords.exists():
        with open(env_passwords, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    creds[key.strip()] = value.strip()
    
    return creds


def discover_fsm_fields(business_class: str, credentials_dir: str = None, tenant: str = 'TAMICS10_AX1') -> Dict[str, List[str]]:
    """
    Discover valid FSM field names for a business class.
    
    Args:
        business_class: FSM business class name (e.g., 'GLTransactionInterface')
        credentials_dir: Path to credentials directory (optional, uses sandbox if not provided)
        tenant: FSM tenant (default: TAMICS10_AX1 sandbox)
    
    Returns:
        Dictionary with 'required' and 'optional' field lists
    """
    # Build API URL
    base_url = f"https://mingle-ionapi.inforcloudsuite.com/{tenant}/FSM/fsm/soap/classes/{business_class}/lists/_generic"
    params = {
        '_fields': '_all',
        '_limit': '1',
        '_links': 'false',
        '_pageNav': 'true',
        '_out': 'JSON',
        '_flatten': 'false',
        '_omitCountValue': 'false'
    }
    
    # Get OAuth2 token if credentials provided
    headers = {}
    if credentials_dir:
        token = _get_oauth2_token(credentials_dir, tenant)
        if token:
            headers['Authorization'] = f'Bearer {token}'
    
    # Make API request
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract field information
        required_fields = []
        optional_fields = []
        
        # FSM API returns a list with [metadata, fields_object]
        if isinstance(data, list) and len(data) > 1:
            fields_obj = data[1]
            if '_fields' in fields_obj:
                record = fields_obj['_fields']
                
                # All keys in the record are valid fields
                all_fields = list(record.keys())
                
                # Filter out system fields (starting with _)
                user_fields = [f for f in all_fields if not f.startswith('_')]
                
                print(f"📋 Discovered {len(user_fields)} fields from FSM API")
                
                # Return all fields - let Kiro decide which to use
                return {
                    'all': user_fields,
                    'required': [],  # Kiro will determine this
                    'optional': []   # Kiro will determine this
                }
        
        # If no fields found, return empty
        return {
            'required': [],
            'optional': [],
            'all': []
        }
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error querying FSM API: {e}")
        print(f"   URL: {base_url}")
        print(f"   This might be due to authentication or network issues.")
        print(f"   Falling back to default field list for {business_class}")
        
        # Fallback to known fields
        return _get_default_fields(business_class)


def _get_oauth2_token(credentials_dir: str, tenant: str) -> str:
    """
    Get OAuth2 access token using password grant flow with .ionapi credentials.
    
    Args:
        credentials_dir: Path to credentials directory
        tenant: FSM tenant (will be overridden if .ionapi file exists)
    
    Returns:
        Access token string or None if failed
    """
    try:
        # Load credentials
        creds = load_credentials(credentials_dir)
        
        # Check if we have .ionapi credentials (preferred)
        if 'ionapi' in creds:
            ionapi = creds['ionapi']
            token_url = creds['token_url']
            client_id = creds['client_id']
            client_secret = creds['client_secret']
            tenant = creds['tenant']
            
            # Service account credentials from .ionapi file
            # saak = Service Account Access Key (username)
            # sask = Service Account Secret Key (password)
            saak = ionapi.get('saak', '')
            sask = ionapi.get('sask', '')
            
            if not saak or not sask:
                print("⚠️  Missing service account keys (saak/sask) in .ionapi file")
                return None
            
            print(f"🔑 Using .ionapi service account for tenant: {tenant}")
            
            # OAuth2 password grant request with service account
            token_data = {
                'grant_type': 'password',
                'username': saak,  # Already includes TENANT# prefix
                'password': sask,
                'client_id': client_id,
                'client_secret': client_secret
            }
            
            response = requests.post(token_url, data=token_data, timeout=30)
            response.raise_for_status()
            
            token_response = response.json()
            access_token = token_response.get('access_token')
            
            if access_token:
                print(f"✅ OAuth2 token obtained successfully")
                return access_token
            else:
                print("⚠️  No access token in response")
                return None
        
        # Fallback to password grant if .env files exist
        if 'SONH_URL' in creds:
            url = creds['SONH_URL']
            # Extract tenant from URL: https://mingle-portal.inforcloudsuite.com/v2/{TENANT}
            if '/v2/' in url:
                tenant = url.split('/v2/')[-1]
        
        username = creds.get('SONH_USERNAME', '')
        password = creds.get('SONH_PASSWORD', '')
        
        if not username or not password:
            print("⚠️  Missing username or password in credentials")
            return None
        
        print(f"🔑 Using password grant for tenant: {tenant}")
        
        # OAuth2 token endpoint
        token_url = f"https://mingle-sso.inforcloudsuite.com:443/{tenant}/as/token.oauth2"
        
        # OAuth2 password grant request
        token_data = {
            'grant_type': 'password',
            'username': f'{tenant}#{username}',
            'password': password,
            'client_id': f'{tenant}~YWRtaW5AaW5mb3IuY29t',  # Default client ID
            'client_secret': ''  # Empty for password grant
        }
        
        response = requests.post(token_url, data=token_data, timeout=30)
        response.raise_for_status()
        
        token_response = response.json()
        access_token = token_response.get('access_token')
        
        if access_token:
            print(f"✅ OAuth2 token obtained successfully")
            return access_token
        else:
            print("⚠️  No access token in response")
            return None
    
    except Exception as e:
        print(f"⚠️  OAuth2 authentication failed: {e}")
        return None


def _get_default_fields(business_class: str) -> Dict[str, List[str]]:
    """
    Fallback field lists when API is unavailable.
    
    Args:
        business_class: FSM business class name
    
    Returns:
        Dictionary with 'required' and 'optional' field lists
    """
    defaults = {
        'GLTransactionInterface': {
            'required': [
                'FinanceEnterpriseGroup',
                'AccountingEntity',
                'PostingDate',
                'Account',
                'Amount',
                'DebitCredit'
            ],
            'optional': [
                'SubAccount',
                'Description',
                'Reference',
                'RunGroup',
                'TransactionNumber',
                'JournalType'
            ]
        }
    }
    
    if business_class in defaults:
        fields = defaults[business_class]
        fields['all'] = fields['required'] + fields['optional']
        return fields
    else:
        return {
            'required': [],
            'optional': [],
            'all': []
        }


if __name__ == "__main__":
    # Example: Discover fields for GLTransactionInterface
    print("🔍 Discovering FSM fields for GLTransactionInterface...")
    print("   Using TAMICS10_AX1 sandbox (no auth required)\n")
    
    fields = discover_fsm_fields('GLTransactionInterface')
    
    print(f"✅ Required fields ({len(fields['required'])}):")
    for field in fields['required']:
        print(f"   - {field}")
    
    print(f"\n📋 Optional fields ({len(fields['optional'])}):")
    for field in fields['optional'][:10]:  # Show first 10
        print(f"   - {field}")
    
    if len(fields['optional']) > 10:
        print(f"   ... and {len(fields['optional']) - 10} more")
