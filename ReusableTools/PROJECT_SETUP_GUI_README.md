# Project Setup GUI - User Guide

## Overview

Modern GUI for setting up FSM testing projects with full multi-tenant support. Replaces the old single-tenant setup script with a flexible, card-based interface.

## Features

✨ **Multi-Tenant Support**
- Add unlimited tenants (TST, PP1, PRD, DEV)
- Each tenant has its own credentials folder
- Separate FSM credentials per environment
- Optional ION API file per tenant

🌐 **Multiple SFTP Servers**
- Configure multiple SFTP servers per project
- Each with its own credentials and paths
- Consolidated SFTP credentials file

📁 **File Channels**
- Define file channels that link SFTP servers to IPA processes
- Configure scan intervals and file patterns
- Track which channels trigger which IPAs

💾 **Import/Export**
- Export configuration to JSON for backup
- Import existing configurations to edit
- Preview configuration before generating

## Usage

### Launch the GUI

```bash
python ReusableTools/project_setup_gui.py
```

### Workflow

1. **Create New Project**
   - Click "Create New Project"
   - Enter project name (e.g., "StateOfNewHampshire")

2. **Add Tenants** (Tab 1: 🏢 Tenants)
   - Click "➕ Add Tenant"
   - Fill in:
     - Environment (TST/PP1/PRD/DEV)
     - Tenant ID (e.g., "NMR2N66J9P445R7P_AX4")
     - FSM Portal URL
     - FSM Username (email)
     - FSM Password
     - ION API File (optional - browse to select)
   - Click "Save"
   - Repeat for each tenant

3. **Add SFTP Servers** (Tab 2: 🌐 SFTP Servers)
   - Click "➕ Add SFTP Server"
   - Fill in:
     - Server Name (e.g., "StateOfNH_TST")
     - Host (default: sftp.inforcloudsuite.com)
     - Port (default: 22)
     - Username
     - Password
     - Inbound Path (default: /Infor_FSM/Inbound/)
     - Outbound Path (default: /Infor_FSM/Outbound/)
   - Click "Save"
   - Repeat for each SFTP server

4. **Add File Channels** (Tab 3: 📁 File Channels)
   - Click "➕ Add File Channel"
   - Fill in:
     - Channel Name (e.g., "INT_FIN_013_Channel")
     - SFTP Server (dropdown - select from added servers)
     - Scan Interval (minutes, default: 5)
     - File Pattern (e.g., "*.csv", "GLTRANSREL_*.csv")
     - IPA Process (e.g., "INT_FIN_013_Import")
   - Click "Save"
   - Repeat for each file channel

5. **Generate Project**
   - Review counts in top bar (tenants, SFTP, channels)
   - Click "👁️ Preview" to see JSON configuration
   - Click "💾 Export Config" to save configuration for later
   - Click "🚀 Generate Project" to create folder structure

## Generated Structure

```
Projects/{ProjectName}/
├── Credentials/
│   ├── TST/
│   │   ├── .env.fsm
│   │   ├── .env.passwords
│   │   └── {TENANT_ID}.ionapi (if provided)
│   ├── PP1/
│   │   ├── .env.fsm
│   │   ├── .env.passwords
│   │   └── {TENANT_ID}.ionapi (if provided)
│   ├── PRD/
│   │   ├── .env.fsm
│   │   ├── .env.passwords
│   │   └── {TENANT_ID}.ionapi (if provided)
│   └── sftp_credentials.env (consolidated SFTP credentials)
├── TestScripts/
│   ├── inbound/
│   ├── outbound/
│   ├── approval/
│   └── test_data/
│       └── README.md
├── TES-070/
│   └── Generated_TES070s/
├── Temp/
├── README.md
└── project_config.json (configuration backup)
```

## Credential File Formats

### .env.fsm (per tenant)
```bash
# FSM Login Credentials - {ProjectName} {Environment}
# DO NOT COMMIT TO VERSION CONTROL

# Tenant: {TENANT_ID}
{PROJECT}_{ENV}_URL=https://mingle-portal.inforcloudsuite.com/{TENANT_ID}/
{PROJECT}_{ENV}_USERNAME=user@example.com
{PROJECT}_{ENV}_PASSWORD=${PROJECT}_{ENV}_PASSWORD}
```

### .env.passwords (per tenant)
```bash
# FSM Password File - {ProjectName} {Environment}
# DO NOT COMMIT TO VERSION CONTROL

{PROJECT}_{ENV}_PASSWORD=actual_password_here
```

### sftp_credentials.env (consolidated)
```bash
# SFTP Credentials - {ProjectName}
# DO NOT COMMIT TO VERSION CONTROL

# {SERVER_NAME}
{SERVER_NAME}_HOST=sftp.inforcloudsuite.com
{SERVER_NAME}_PORT=22
{SERVER_NAME}_USERNAME=sftp_user
{SERVER_NAME}_PASSWORD=sftp_pass
{SERVER_NAME}_INBOUND_PATH=/Infor_FSM/Inbound/
{SERVER_NAME}_OUTBOUND_PATH=/Infor_FSM/Outbound/
```

## CRUD Operations

### Tenants
- **Add**: Click "➕ Add Tenant" button
- **Edit**: Click "✏️ Edit" on tenant card
- **Delete**: Click "🗑️ Delete" on tenant card

### SFTP Servers
- **Add**: Click "➕ Add SFTP Server" button
- **Edit**: Click "✏️ Edit" on SFTP card
- **Delete**: Click "🗑️ Delete" on SFTP card

### File Channels
- **Add**: Click "➕ Add File Channel" button
- **Edit**: Click "✏️ Edit" on channel card
- **Delete**: Click "🗑️ Delete" on channel card

## Example: StateOfNewHampshire Project

### Tenants
1. **TST**: NMR2N66J9P445R7P_AX4
2. **PP1**: NMR2N66J9P445R7P_AX5
3. **PRD**: NMR2N66J9P445R7P_AX6

### SFTP Servers
1. **StateOfNH_TST**: sftp.inforcloudsuite.com (test environment)
2. **StateOfNH_PRD**: sftp-prod.inforcloudsuite.com (production)

### File Channels
1. **INT_FIN_013_Channel**: StateOfNH_TST → INT_FIN_013_Import (5 min scan, *.csv)
2. **INT_FIN_127_Channel**: StateOfNH_TST → INT_FIN_127_Export (10 min scan, ACH_*.txt)

## Tips

💡 **Start with TST**: Add TST tenant first, then clone for PP1/PRD
💡 **SFTP per environment**: Create separate SFTP servers for TST/PP1/PRD
💡 **Export often**: Export configuration after major changes
💡 **Preview first**: Always preview before generating
💡 **ION API optional**: Only needed if using ION API for data queries

## Security

⚠️ **CRITICAL**: Generated credential files are automatically in .gitignore
⚠️ **NEVER** commit credential files to version control
⚠️ **ALWAYS** verify credentials after generation
⚠️ **ROTATE** passwords regularly

## Troubleshooting

### "Project already exists"
- Choose "Continue editing" to update existing project
- Or delete the existing folder first

### "At least one tenant is required"
- Add at least one tenant before generating

### SFTP dropdown empty in File Channels
- Add SFTP servers first in Tab 2

### ION API file not found
- Verify file path is correct
- File will be copied to Credentials/{ENV}/ folder

## Integration with Other Tools

After project setup, the new project automatically works with:
- ✅ Test Scenario Builder (client dropdown)
- ✅ Test Data Generator (credential loading)
- ✅ Test Execution (Playwright automation)
- ✅ TES-070 Generation

## Comparison: Old vs New

| Feature | Old Script | New GUI |
|---------|-----------|---------|
| Tenants | 1 only | Unlimited |
| SFTP Servers | 1 only | Unlimited |
| File Channels | Not tracked | Full management |
| Credentials | Single folder | Per-environment folders |
| UI | Command-line | Modern GUI |
| CRUD | No editing | Full CRUD |
| Import/Export | No | Yes |
| Preview | No | Yes |

## Future Enhancements

- [ ] Validate credentials (test FSM login)
- [ ] Test SFTP connections
- [ ] Import from existing project folders
- [ ] Duplicate tenant/SFTP/channel
- [ ] Drag-and-drop reordering
- [ ] Search/filter in lists

## Support

For questions or issues:
1. Check this guide
2. Review example projects (StateOfNewHampshire, TAMICS10)
3. Contact FSM Testing Team
