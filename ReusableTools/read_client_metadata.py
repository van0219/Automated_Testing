"""
Read Client Metadata from Project README

This utility reads client metadata from the project's README.md file.
Used during test execution to get the full client name for TES-070 generation.

Usage:
    from read_client_metadata import get_client_metadata
    
    metadata = get_client_metadata("SONH")
    print(metadata['client_name'])  # "State of New Hampshire"
"""

import re
from pathlib import Path
from typing import Dict, Optional


def get_client_metadata(client_code: str) -> Dict[str, str]:
    """
    Read client metadata from project README.md
    
    Args:
        client_code: Short client code (e.g., 'SONH')
    
    Returns:
        Dictionary with client metadata:
        - client_code: Short code (e.g., 'SONH')
        - client_name: Full name (e.g., 'State of New Hampshire')
        - tenant_id: FSM tenant ID
        - fsm_url: FSM portal URL
        - created: Project creation date
    
    Raises:
        FileNotFoundError: If README.md not found
        ValueError: If required metadata not found in README
    """
    readme_path = Path(f"Projects/{client_code}/README.md")
    
    if not readme_path.exists():
        raise FileNotFoundError(f"README.md not found at: {readme_path}")
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = {
        'client_code': client_code
    }
    
    # Extract client name
    client_name_match = re.search(r'\*\*Client Name:\*\*\s*(.+)', content)
    if client_name_match:
        metadata['client_name'] = client_name_match.group(1).strip()
    else:
        # Fallback: use client code if not found
        metadata['client_name'] = client_code
        print(f"⚠️  Warning: Client Name not found in README, using client code: {client_code}")
    
    # Extract tenant ID
    tenant_match = re.search(r'\*\*Tenant ID:\*\*\s*(.+)', content)
    if tenant_match:
        metadata['tenant_id'] = tenant_match.group(1).strip()
    
    # Extract FSM URL
    url_match = re.search(r'\*\*FSM URL:\*\*\s*(.+)', content)
    if url_match:
        metadata['fsm_url'] = url_match.group(1).strip()
    
    # Extract created date
    created_match = re.search(r'\*\*Created:\*\*\s*(.+)', content)
    if created_match:
        metadata['created'] = created_match.group(1).strip()
    
    return metadata


def validate_client_metadata(metadata: Dict[str, str]) -> bool:
    """
    Validate that required metadata fields are present
    
    Args:
        metadata: Client metadata dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['client_code', 'client_name']
    
    for field in required_fields:
        if field not in metadata or not metadata[field]:
            print(f"❌ Missing required field: {field}")
            return False
    
    return True


def print_client_metadata(metadata: Dict[str, str]):
    """Print client metadata in a readable format"""
    print("\n" + "="*60)
    print("CLIENT METADATA")
    print("="*60)
    
    print(f"\n📋 Client Code: {metadata.get('client_code', 'N/A')}")
    print(f"🏢 Client Name: {metadata.get('client_name', 'N/A')}")
    
    if 'tenant_id' in metadata:
        print(f"🔑 Tenant ID: {metadata['tenant_id']}")
    
    if 'fsm_url' in metadata:
        print(f"🌐 FSM URL: {metadata['fsm_url']}")
    
    if 'created' in metadata:
        print(f"📅 Created: {metadata['created']}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python read_client_metadata.py <client_code>")
        print("\nExample:")
        print("  python ReusableTools/read_client_metadata.py SONH")
        sys.exit(1)
    
    client_code = sys.argv[1]
    
    try:
        metadata = get_client_metadata(client_code)
        
        if validate_client_metadata(metadata):
            print_client_metadata(metadata)
            print("\n✅ Client metadata loaded successfully!")
        else:
            print("\n❌ Client metadata validation failed!")
            sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
