"""
New Project Setup Tool

Creates complete project folder structure and credential file templates
for a new FSM testing client.

Usage:
    python ReusableTools/new_project_setup.py

This script is typically invoked by the "New Project Setup" hook.
"""

import os
from pathlib import Path
from datetime import datetime


def create_project_structure(
    client_name,
    tenant_id,
    fsm_url,
    fsm_username,
    fsm_password,
    sftp_server_name,
    sftp_host,
    sftp_username,
    sftp_password,
    sftp_inbound_path="/Infor_FSM/Inbound/",
    sftp_outbound_path="/Infor_FSM/Outbound/"
):
    """
    Create complete project structure with credential files.
    
    Args:
        client_name: Client/project name (e.g., "TAMICS10")
        tenant_id: FSM tenant ID (e.g., "TAMICS10_AX1")
        fsm_url: FSM portal URL
        fsm_username: FSM login username (email)
        fsm_password: FSM login password
        sftp_server_name: SFTP server identifier
        sftp_host: SFTP hostname
        sftp_username: SFTP username
        sftp_password: SFTP password
        sftp_inbound_path: SFTP inbound directory path
        sftp_outbound_path: SFTP outbound directory path
    
    Returns:
        dict: Summary of created files and folders
    """
    
    base_path = Path(f"Projects/{client_name}")
    
    # Check if project already exists
    if base_path.exists():
        return {
            "success": False,
            "error": f"Project folder 'Projects/{client_name}' already exists!"
        }
    
    # Create folder structure
    folders = [
        "Credentials",
        "TestScripts/inbound",
        "TestScripts/outbound",
        "TestScripts/approval",
        "TestScripts/test_data",
        "TES-070/Generated_TES070s",
        "Temp"
    ]
    
    created_folders = []
    for folder in folders:
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        created_folders.append(str(folder_path))
    
    # Create .env.fsm
    env_fsm_content = f"""# FSM Login Credentials - {client_name}
# DO NOT COMMIT TO VERSION CONTROL

# Tenant: {tenant_id}
{client_name.upper().replace(' ', '_')}_URL={fsm_url}
{client_name.upper().replace(' ', '_')}_USERNAME={fsm_username}

"""
    
    env_fsm_path = base_path / "Credentials" / ".env.fsm"
    with open(env_fsm_path, 'w', encoding='utf-8') as f:
        f.write(env_fsm_content)
    
    # Create .env.passwords
    env_passwords_content = f"""# FSM Password File - {client_name}
# DO NOT COMMIT TO VERSION CONTROL

{client_name.upper().replace(' ', '_')}_PASSWORD={fsm_password}

# SFTP Credentials ({sftp_server_name})
# Used for testing inbound/outbound file interfaces
SFTP_SERVER_NAME={sftp_server_name}
SFTP_HOST={sftp_host}
SFTP_PORT=22
SFTP_USERNAME={sftp_username}
SFTP_PASSWORD={sftp_password}

# SFTP Paths (defaults - adjust per interface as needed)
# Different RICE items may use different paths
SFTP_INBOUND_PATH={sftp_inbound_path}
SFTP_OUTBOUND_PATH={sftp_outbound_path}

# Additional SFTP configurations can be added here for specific interfaces:
# SFTP_INBOUND_PATH_INT_FIN_013=/custom/path/inbound/
# SFTP_OUTBOUND_PATH_INT_FIN_127=/custom/path/outbound/

"""
    
    env_passwords_path = base_path / "Credentials" / ".env.passwords"
    with open(env_passwords_path, 'w', encoding='utf-8') as f:
        f.write(env_passwords_content)
    
    # Create README.md
    readme_content = f"""# {client_name} Project

## Overview
This folder contains all testing artifacts for the {client_name} FSM implementation.

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Tenant Information
- **Tenant ID:** {tenant_id}
- **FSM URL:** {fsm_url}
- **SFTP Server:** {sftp_server_name}

## Structure
- `Credentials/` - FSM credentials (.env.fsm, .env.passwords, *.ionapi)
- `TestScripts/` - Test scenario JSON files and test data
  - `inbound/` - Inbound interface test scenarios
  - `outbound/` - Outbound interface test scenarios
  - `approval/` - Approval workflow test scenarios
  - `test_data/` - CSV/JSON test data files
- `TES-070/Generated_TES070s/` - Generated test results documents
- `Temp/` - Test execution screenshots and temporary files

## Getting Started

### 1. Verify Credentials
Check that credentials in `Credentials/` folder are correct:
- `.env.fsm` - FSM portal login credentials
- `.env.passwords` - Actual passwords and SFTP credentials

**Note:** SFTP paths in `.env.passwords` are defaults. Each interface may use different paths.
Add interface-specific SFTP configurations as needed (e.g., `SFTP_INBOUND_PATH_INT_FIN_013=/custom/path/`).

### 2. Add ION API Credentials (Optional)
If using ION API for data queries:
- Download `.ionapi` file from ION API Gateway
- Place in `Credentials/` folder
- Name it `{tenant_id}.ionapi`

### 3. Create Test Scenarios
Use the Test Scenario Builder GUI:
1. Click "Step 1: Define Test Scenarios" hook
2. Select interface type (Inbound/Outbound/Approval)
3. Fill in interface details
4. Edit pre-loaded scenarios
5. Save to `TestScripts/{{interface_type}}/`

### 4. Execute Tests
1. Click "Step 2: Execute Tests in FSM" hook
2. Tests run automatically with Playwright
3. Screenshots saved to `Temp/`

### 5. Generate TES-070 Documents
1. Click "Step 3: Generate TES-070" hook
2. Document generated in `TES-070/Generated_TES070s/`

## Security Notes
⚠️ **NEVER commit credential files to version control!**
- `.env.fsm`
- `.env.passwords`
- `*.ionapi`

These files are already in `.gitignore` at the workspace root.

## Support
For questions or issues, contact the FSM Testing Team.
"""
    
    readme_path = base_path / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create TEST_DATA_README.md in test_data folder
    test_data_readme = """# Test Data Files

This folder contains CSV, XML, and JSON test data files used for interface testing.

## File Naming Convention
- `{INTERFACE_ID}_valid.csv` - Valid data for successful import
- `{INTERFACE_ID}_invalid_format.csv` - Invalid format/structure
- `{INTERFACE_ID}_duplicate.csv` - Duplicate records
- `{INTERFACE_ID}_empty.csv` - Empty file
- `{INTERFACE_ID}_business_error.csv` - Business rule violations

## Generating Test Data
Use the "Step 0: Generate Test Data" hook to create fresh test data files with:
- Current dates (YYYYMMDD format)
- Correct FSM field names (queried from FSM API)
- Appropriate test scenarios (valid, invalid, duplicate, etc.)

## Usage
Test data files are referenced in test scenario JSON files via the `test_data_file` field.
"""
    
    test_data_readme_path = base_path / "TestScripts" / "test_data" / "README.md"
    with open(test_data_readme_path, 'w', encoding='utf-8') as f:
        f.write(test_data_readme)
    
    return {
        "success": True,
        "client_name": client_name,
        "base_path": str(base_path),
        "folders_created": len(created_folders),
        "files_created": [
            str(env_fsm_path),
            str(env_passwords_path),
            str(readme_path),
            str(test_data_readme_path)
        ]
    }


def interactive_setup():
    """Interactive command-line setup"""
    print("=" * 60)
    print("FSM Testing Project Setup")
    print("=" * 60)
    print()
    
    # Collect information
    client_name = input("Client/Project Name (e.g., TAMICS10): ").strip()
    tenant_id = input("Tenant ID (e.g., TAMICS10_AX1): ").strip()
    fsm_url = input("FSM Portal URL: ").strip()
    fsm_username = input("FSM Username (email): ").strip()
    fsm_password = input("FSM Password: ").strip()
    
    print("\n--- SFTP Configuration ---")
    print("Note: SFTP paths can vary per interface. These are defaults only.")
    sftp_server_name = input("SFTP Server Name (e.g., Tamics10_AX1): ").strip()
    sftp_host = input("SFTP Host (default: sftp.inforcloudsuite.com): ").strip() or "sftp.inforcloudsuite.com"
    sftp_username = input("SFTP Username: ").strip()
    sftp_password = input("SFTP Password: ").strip()
    sftp_inbound = input("SFTP Inbound Path (optional, press Enter to skip): ").strip() or "/Infor_FSM/Inbound/"
    sftp_outbound = input("SFTP Outbound Path (optional, press Enter to skip): ").strip() or "/Infor_FSM/Outbound/"
    
    print("\n" + "=" * 60)
    print("Creating project structure...")
    print("=" * 60)
    
    result = create_project_structure(
        client_name=client_name,
        tenant_id=tenant_id,
        fsm_url=fsm_url,
        fsm_username=fsm_username,
        fsm_password=fsm_password,
        sftp_server_name=sftp_server_name,
        sftp_host=sftp_host,
        sftp_username=sftp_username,
        sftp_password=sftp_password,
        sftp_inbound_path=sftp_inbound,
        sftp_outbound_path=sftp_outbound
    )
    
    if result["success"]:
        print(f"\n✅ Project created successfully!")
        print(f"\n📁 Base Path: {result['base_path']}")
        print(f"📂 Folders Created: {result['folders_created']}")
        print(f"📄 Files Created: {len(result['files_created'])}")
        print("\n📝 Files:")
        for file in result['files_created']:
            print(f"   - {file}")
        
        print("\n⚠️  Next Steps:")
        print("   1. Verify credentials in Credentials/ folder")
        print("   2. Add .ionapi file if using ION API")
        print("   3. NEVER commit credential files to git!")
        print("   4. Use Test Scenario Builder to create test scenarios")
    else:
        print(f"\n❌ Error: {result['error']}")


if __name__ == "__main__":
    interactive_setup()
