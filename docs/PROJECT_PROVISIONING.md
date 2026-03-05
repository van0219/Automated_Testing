# Project Provisioning Guide

## Overview

This guide explains how to set up a new FSM testing project with complete folder structure and credential templates.

## Method 1: Using the Hook (Recommended)

### Step 1: Trigger the Hook
1. Open Kiro Agent Hooks panel
2. Click **"New Project Setup"** hook
3. The AI will guide you through the setup process

### Step 2: Provide Information
The AI will ask for:

**FSM Credentials:**
- Client/Project Name (e.g., "TAMICS10", "BayCare")
- Tenant ID (e.g., "TAMICS10_AX1", "NMR2N66J9P445R7P_AX4")
- FSM Portal URL (e.g., "https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1/")
- FSM Username (email address)
- FSM Password

**SFTP Credentials:**
- SFTP Server Name (e.g., "Tamics10_AX1")
- SFTP Host (default: "sftp.inforcloudsuite.com")
- SFTP Username
- SFTP Password
- SFTP Inbound Path (optional - defaults to "/Infor_FSM/Inbound/")
- SFTP Outbound Path (optional - defaults to "/Infor_FSM/Outbound/")

**Note:** SFTP paths are optional defaults. Each RICE item may use different paths. You can add interface-specific paths to `.env.passwords` later (e.g., `SFTP_INBOUND_PATH_INT_FIN_013=/custom/path/`).

### Step 3: Review Created Structure
The AI will create:

```
Projects/{ClientName}/
├── Credentials/
│   ├── .env.fsm              # FSM login credentials
│   └── .env.passwords        # Passwords and SFTP credentials
├── TestScripts/
│   ├── inbound/              # Inbound interface test scenarios
│   ├── outbound/             # Outbound interface test scenarios
│   ├── approval/             # Approval workflow test scenarios
│   └── test_data/            # CSV/JSON test data files
│       └── README.md
├── TES-070/
│   └── Generated_TES070s/    # Generated test results documents
├── Temp/                     # Test execution screenshots
└── README.md                 # Project documentation
```

## Method 2: Using Python Script Directly

### Interactive Mode
```bash
python ReusableTools/new_project_setup.py
```

Follow the prompts to enter all required information.

### Programmatic Mode
```python
from ReusableTools.new_project_setup import create_project_structure

result = create_project_structure(
    client_name="MyClient",
    tenant_id="MYCLIENT_TST",
    fsm_url="https://mingle-portal.inforcloudsuite.com/MYCLIENT_TST/",
    fsm_username="user@example.com",
    fsm_password="password123",
    sftp_server_name="MyClient_TST",
    sftp_host="sftp.inforcloudsuite.com",
    sftp_username="sftp-user",
    sftp_password="sftp-pass",
    sftp_inbound_path="/Infor_FSM/Inbound/",
    sftp_outbound_path="/Infor_FSM/Outbound/"
)

if result["success"]:
    print(f"Project created: {result['base_path']}")
else:
    print(f"Error: {result['error']}")
```

## What Gets Created

### 1. Folder Structure
- **Credentials/** - Secure storage for credentials (never commit!)
- **TestScripts/** - Test scenario JSON files organized by type
- **TES-070/** - Generated test results documents
- **Temp/** - Temporary files and test execution screenshots

### 2. Credential Files

#### .env.fsm
```bash
# FSM Login Credentials - {ClientName}
# DO NOT COMMIT TO VERSION CONTROL

# Tenant: {TenantID}
{CLIENT}_URL=https://mingle-portal.inforcloudsuite.com/{TenantID}/
{CLIENT}_USERNAME=user@example.com
{CLIENT}_PASSWORD=${CLIENT_PASSWORD}
```

#### .env.passwords
```bash
# FSM Password File - {ClientName}
# DO NOT COMMIT TO VERSION CONTROL

{CLIENT}_PASSWORD=actual_password_here

# SFTP Credentials
SFTP_SERVER_NAME=Server_Name
SFTP_HOST=sftp.inforcloudsuite.com
SFTP_PORT=22
SFTP_USERNAME=sftp_user
SFTP_PASSWORD=sftp_pass

# SFTP Paths (defaults - adjust per interface as needed)
# Different RICE items may use different paths
SFTP_INBOUND_PATH=/Infor_FSM/Inbound/
SFTP_OUTBOUND_PATH=/Infor_FSM/Outbound/

# Additional SFTP configurations can be added here for specific interfaces:
# SFTP_INBOUND_PATH_INT_FIN_013=/custom/path/inbound/
# SFTP_OUTBOUND_PATH_INT_FIN_127=/custom/path/outbound/
```

### 3. Documentation Files
- **README.md** - Project overview and getting started guide
- **TestScripts/test_data/README.md** - Test data file conventions

## Post-Setup Steps

### 1. Verify Credentials
- Open `Credentials/.env.fsm` and verify FSM URL and username
- Open `Credentials/.env.passwords` and verify all passwords
- Test FSM login manually to confirm credentials work

### 2. Add ION API Credentials (Optional)
If using ION API for data queries:
1. Download `.ionapi` file from ION API Gateway
2. Place in `Credentials/` folder
3. Name it `{TenantID}.ionapi` (e.g., `TAMICS10_AX1.ionapi`)

### 3. Test SFTP Connection (Optional)
```python
from ReusableTools.sftp_helper import test_sftp_connection

# Test connection
test_sftp_connection(
    host="sftp.inforcloudsuite.com",
    username="your-sftp-user",
    password="your-sftp-pass"
)
```

### 4. Create First Test Scenario
1. Click **"Step 1: Define Test Scenarios"** hook
2. Select client from dropdown (your new client will appear!)
3. Select interface type
4. Fill in interface details
5. Edit scenarios
6. Save

## Security Best Practices

### ⚠️ CRITICAL: Never Commit Credentials!

The following files contain sensitive information and must NEVER be committed to version control:
- `Credentials/.env.fsm`
- `Credentials/.env.passwords`
- `Credentials/*.ionapi`

These files are already in `.gitignore` at the workspace root.

### Credential Storage
- Store credentials securely (password manager, encrypted vault)
- Rotate passwords regularly
- Use separate credentials for each environment (TST, PP1, PRD)
- Never share credentials via email or chat

### Access Control
- Limit access to Credentials/ folder
- Use read-only credentials when possible
- Audit credential usage regularly

## Troubleshooting

### Project Already Exists
**Error:** "Project folder 'Projects/{ClientName}' already exists!"

**Solution:** 
- Choose a different client name, or
- Manually delete the existing folder if it's a mistake

### Missing Credentials
**Error:** "Credentials not found for {ClientName}"

**Solution:**
- Verify `.env.fsm` and `.env.passwords` exist in `Credentials/` folder
- Check file names are exactly `.env.fsm` and `.env.passwords` (with leading dot)
- Verify files are not empty

### SFTP Connection Failed
**Error:** "Failed to connect to SFTP server"

**Solution:**
- Verify SFTP credentials in `.env.passwords`
- Check SFTP host and port (default: 22)
- Confirm network connectivity to SFTP server
- Test credentials manually using FileZilla or WinSCP

## Integration with Other Tools

### Test Scenario Builder
After project setup, the new client automatically appears in:
- Client Name dropdown
- SFTP Server dropdown

### Test Data Generator
Use "Step 0: Generate Test Data" hook to create test data files for the new client.

### Test Execution
Use "Step 2: Execute Tests in FSM" hook to run tests against the new client's FSM environment.

### TES-070 Generation
Use "Step 3: Generate TES-070" hook to create test results documents for the new client.

## Example: Complete Setup Flow

```
1. Click "New Project Setup" hook
   ↓
2. Provide client information
   - Client Name: "BayCare"
   - Tenant ID: "BAYCARE_TST"
   - FSM URL: https://mingle-portal.inforcloudsuite.com/BAYCARE_TST/
   - Credentials...
   ↓
3. AI creates complete structure
   ✅ Projects/BayCare/ created
   ✅ Credentials files created
   ✅ README.md created
   ↓
4. Verify credentials work
   ✅ Test FSM login
   ✅ Test SFTP connection
   ↓
5. Create first test scenario
   Click "Step 1: Define Test Scenarios"
   Select "BayCare" from dropdown
   ↓
6. Start testing!
```

## Support

For questions or issues with project provisioning:
1. Check this guide first
2. Review existing project structures (TAMICS10, StateOfNewHampshire)
3. Contact the FSM Testing Team

## Related Documentation
- [Test Scenario Builder Guide](../ReusableTools/README.md)
- [TES-070 Generation Guide](../TES-070/README.md)
- [SFTP Helper Guide](../ReusableTools/sftp_helper.py)
