# Workspace Structure

## Clean, Organized Structure ✅

```
Automated_Testing/
├── .kiro/                          # Kiro configuration
│   ├── hooks/                      # 4 workflow hooks
│   ├── steering/                   # 9 steering files (00-08)
│   └── settings/                   # MCP configuration
│
├── Projects/                       # 🎯 MAIN WORKING AREA
│   ├── StateOfNewHampshire/       # Client 1
│   │   ├── Credentials/           # FSM credentials
│   │   ├── TestScripts/           # Test scenario JSON files
│   │   │   ├── inbound/
│   │   │   ├── outbound/
│   │   │   └── approval/
│   │   ├── TES-070/               # Generated documents
│   │   │   └── Generated_TES070s/
│   │   └── Temp/                  # Screenshots
│   └── README.md
│
├── ReusableTools/                  # Shared Python utilities
│   ├── automation_examples/       # Playwright examples
│   ├── tes070_generator.py        # Core generator
│   ├── generate_tes070_from_json.py
│   ├── tes070_analyzer.py
│   ├── test_scenario_builder_gui.py
│   └── ...
│
├── TES-070/                        # Shared TES-070 resources
│   ├── Sample_Documents/          # Reference examples (3 samples)
│   └── README.md
│
├── docs/                           # Documentation
│   ├── screenshots/
│   └── diagrams/
│
├── README.md                       # Workspace overview
├── SETUP.md                        # Setup guide
├── MIGRATION_COMPLETE.md          # Migration details
└── requirements.txt               # Python dependencies
```

## Key Principles

### 1. Client Separation
- Each client gets their own folder in `Projects/`
- Complete isolation of credentials, test scenarios, and results
- No mixing of client data

### 2. Shared Resources
- `ReusableTools/` - Python utilities used by all clients
- `TES-070/Sample_Documents/` - Reference examples
- `.kiro/` - Hooks and steering files

### 3. Clean Organization
- No deprecated folders at root
- Clear separation between client work and shared resources
- Easy to navigate and understand

## Workflow

### For Consultants

**Interface Step 1: Define Test Scenarios**
- Click hook → Modern GUI launches → Fill in details → Save JSON
- Saves to: `Projects/{ClientName}/TestScripts/`

**Interface Step 2: Execute Tests in FSM**
- Click hook → Playwright automation → Capture screenshots
- Reads from: `Projects/{ClientName}/Credentials/`
- Saves to: `Projects/{ClientName}/Temp/`

**Interface Step 3: Generate TES-070**
- Click hook → Generate document
- Saves to: `Projects/{ClientName}/TES-070/Generated_TES070s/`

### Adding New Clients

1. Click "Interface Step 1: Define Test Scenarios"
2. GUI launches - enter new client name in the Client field
3. Fill in interface details and save
4. Folder structure automatically created
5. Continue with Steps 2 and 3

## File Locations

### Client-Specific Files
- **Credentials**: `Projects/{ClientName}/Credentials/`
- **Test Scenarios**: `Projects/{ClientName}/TestScripts/{type}/`
- **Generated TES-070s**: `Projects/{ClientName}/TES-070/Generated_TES070s/`
- **Screenshots**: `Projects/{ClientName}/Temp/`

### Shared Files
- **Python Tools**: `ReusableTools/`
- **Sample TES-070s**: `TES-070/Sample_Documents/`
- **Documentation**: `docs/`
- **Hooks**: `.kiro/hooks/`
- **Steering**: `.kiro/steering/`

## Benefits

✅ **Scalable**: Add unlimited clients easily
✅ **Secure**: Credentials never mix
✅ **Organized**: Clear structure, easy to find files
✅ **Professional**: Industry-standard multi-client setup
✅ **Git-friendly**: Can .gitignore specific clients

## Current Clients

| Client | Tenant | Environment | Credentials | Status |
|--------|--------|-------------|-------------|--------|
| **StateOfNewHampshire** | NMR2N66J9P445R7P_AX4 | Production | ✅ Complete | Active |
| **TAMICS10** | TAMICS10_AX1 | Sandbox/POC | ✅ Complete | Active |
| **BayCare** | BAYCAREHS_TRN | Training | ✅ Complete | Active |
| **ACUITY** | ACUITY_TST | Test | ✅ Complete | Active |

### Credential Files Per Client
Each client has:
- `.env.fsm` - FSM URL and username
- `.env.passwords` - Password (git-ignored)
- `*.ionapi` - ION API credentials (optional, git-ignored)

## Quick Start

1. Choose a client: StateOfNewHampshire, TAMICS10, BayCare, or ACUITY
2. Click "Interface Step 1: Define Test Scenarios" hook in Kiro
3. Follow the 3-step workflow to create TES-070 documents

See [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) for detailed instructions.

---

**Last Updated**: February 13, 2026
**Status**: ✅ Ready for Testing
