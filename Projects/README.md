# Projects Folder

This folder contains all client/project-specific work. Each client gets their own subfolder to keep everything organized and separated.

## Structure

```
Projects/
├── StateOfNewHampshire/     # Client 1
│   ├── Credentials/         # Client-specific credentials
│   ├── TestScripts/         # Test scenario JSON files
│   ├── TES-070/            # Generated TES-070 documents
│   └── Temp/               # Screenshots and temp files
├── AnotherClient/          # Client 2
│   ├── Credentials/
│   ├── TestScripts/
│   ├── TES-070/
│   └── Temp/
└── README.md               # This file
```

## Current Clients

1. **State of New Hampshire** - `Projects/StateOfNewHampshire/`
   - Tenant: NMR2N66J9P445R7P_AX4
   - Environment: Production
   - Status: Active

2. **TAMICS10** - `Projects/TAMICS10/`
   - Tenant: TAMICS10_AX1
   - Environment: Sandbox/POC
   - Status: Active

3. **BayCare** - `Projects/BayCare/`
   - Tenant: BAYCAREHS_TRN
   - Environment: Training
   - Status: Active

4. **ACUITY** - `Projects/ACUITY/`
   - Tenant: ACUITY_TST
   - Environment: Test
   - Status: Active

## Creating a New Client Project

When starting work for a new client:

1. Create a new folder: `Projects/{ClientName}/`
2. Create subfolders:
   - `Credentials/` - Store client FSM credentials
   - `TestScripts/inbound/` - Inbound interface test scenarios
   - `TestScripts/outbound/` - Outbound interface test scenarios
   - `TestScripts/approval/` - Approval workflow test scenarios
   - `TES-070/Generated_TES070s/` - Generated test documents
   - `Temp/` - Screenshots and temporary files

3. Copy credentials template:
   - `.env.fsm` - FSM URLs and usernames
   - `.env.passwords` - Passwords (git-ignored)
   - `*.ionapi` - ION API credentials (if needed)

## Using the 3-Step Workflow

When using the hooks, specify the client folder:

**Interface Step 1: Define Test Scenarios**
- Launches modern GUI tool
- JSON saved to: `Projects/{ClientName}/TestScripts/{type}/{interface_id}_test_scenarios.json`

**Step 2: Execute Tests in FSM**
- Reads credentials from: `Projects/{ClientName}/Credentials/`
- Saves screenshots to: `Projects/{ClientName}/Temp/{interface_id}_{timestamp}/`

**Step 3: Generate TES-070**
- Reads JSON from: `Projects/{ClientName}/TestScripts/`
- Reads screenshots from: `Projects/{ClientName}/Temp/`
- Saves document to: `Projects/{ClientName}/TES-070/Generated_TES070s/`

## Benefits

✅ **Separation**: Each client's data is completely isolated
✅ **Security**: Client credentials never mix
✅ **Organization**: Easy to find client-specific files
✅ **Scalability**: Add unlimited clients without confusion
✅ **Git-friendly**: Can .gitignore specific client folders if needed

## Example: State of New Hampshire

```
Projects/StateOfNewHampshire/
├── Credentials/
│   ├── .env.fsm
│   ├── .env.passwords
│   └── ACUITY_TST.ionapi
├── TestScripts/
│   ├── inbound/
│   │   ├── INT_FIN_013_test_scenarios.json
│   │   └── INT_FIN_010_test_scenarios.json
│   └── outbound/
│       └── INT_FIN_127_test_scenarios.json
├── TES-070/
│   └── Generated_TES070s/
│       ├── INT_FIN_013_GL_Transaction_Interface_20260213.docx
│       └── INT_FIN_010_Receivables_Invoice_Import_20260213.docx
└── Temp/
    ├── INT_FIN_013_20260213_120000/
    │   ├── 01_sftp_file_drop.png
    │   └── 02_file_channel_scan.png
    └── INT_FIN_010_20260213_130000/
        └── screenshots...
```

## Shared Resources

These remain at the workspace root (shared across all clients):

- **ReusableTools/** - Python utilities (tes070_generator.py, etc.)
- **.kiro/** - Hooks and steering files
- **TES-070/Sample_Documents/** - Reference TES-070 examples
- **docs/** - General documentation

## Migration from Current Structure

To migrate existing State of New Hampshire work:

1. Create `Projects/StateOfNewHampshire/` folder structure
2. Move `Credentials/` → `Projects/StateOfNewHampshire/Credentials/`
3. Move `TestScripts/` → `Projects/StateOfNewHampshire/TestScripts/`
4. Move `TES-070/Generated_TES070s/` → `Projects/StateOfNewHampshire/TES-070/Generated_TES070s/`
5. Move `Temp/` screenshots → `Projects/StateOfNewHampshire/Temp/`
6. Keep `TES-070/Sample_Documents/` at root (shared reference)
