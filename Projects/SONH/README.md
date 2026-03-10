# SONH Project

## Client Information
- **Client Code:** SONH
- **Client Name:** State of New Hampshire
- **Created:** 2026-03-05 09:12:10

## Overview
This folder contains all testing artifacts for the SONH FSM implementation.

## Tenant Information
- **Tenant ID:** NMR2N66J9P445R7P_AX4
- **FSM URL:** https://mingle-portal.inforcloudsuite.com/v2/NMR2N66J9P445R7P_AX4/03b3ab89-37e0-4632-a578-7700d803b32e
- **SFTP Server:** SONH_AX4_SFTP

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
- Name it `NMR2N66J9P445R7P_AX4.ionapi`

### 3. Create Test Scenarios
Use the Test Scenario Builder GUI:
1. Click "Interface Step 1: Define Test Scenarios" hook
2. Select interface type (Inbound/Outbound/Approval)
3. Fill in interface details
4. Edit pre-loaded scenarios
5. Save to `TestScripts/{interface_type}/`

### 4. Execute Tests
1. Click "Interface Step 2: Execute Tests in FSM" hook
2. Tests run automatically with Playwright
3. Screenshots saved to `Temp/`

### 5. Generate TES-070 Documents
1. Click "Interface Step 3: Generate TES-070" hook
2. Document generated in `TES-070/Generated_TES070s/`

## Security Notes
⚠️ **NEVER commit credential files to version control!**
- `.env.fsm`
- `.env.passwords`
- `*.ionapi`

These files are already in `.gitignore` at the workspace root.

## Support
For questions or issues, contact the FSM Testing Team.
