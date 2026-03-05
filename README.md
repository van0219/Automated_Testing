# FSM Automated Testing Workspace

Automated testing framework for Infor FSM (Financials & Supply Management) focusing on RICE methodology (Reports, Interfaces, Conversions, Enhancements) and IPA process automation.

## 🚀 Quick Start

### For New Projects
1. **Click "New Project Setup"** hook to provision a new client folder
2. **Provide credentials** (FSM URL, username, password, SFTP details)
3. **Complete structure created** automatically with credential templates

### For Functional Consultants
1. **Choose a client**: StateOfNewHampshire, TAMICS10, BayCare, or ACUITY
2. **Click "Interface Step 0: Generate Test Data"** to create fresh test data files
3. **Click "Interface Step 1: Define Test Scenarios"** to create test scenarios
4. **Follow the 5-step workflow** to create TES-070 documents

See [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) for the complete workflow.

### For Developers
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Tesseract-OCR (see SETUP.md)

# 3. Configure credentials in Projects/{ClientName}/Credentials/

# 4. Start testing!
```

See [SETUP.md](SETUP.md) for detailed setup instructions.

## 📁 Workspace Structure

```
Automated_Testing/
├── .kiro/                  # Kiro AI configuration
│   ├── steering/          # AI guidance files (00-08)
│   ├── settings/          # MCP and other configs
│   └── hooks/             # 3-step workflow hooks
│
├── Projects/              # 🎯 MAIN WORKING AREA
│   ├── StateOfNewHampshire/  # Client 1
│   │   ├── Credentials/      # Client FSM credentials
│   │   ├── TestScripts/      # Test scenario JSON files
│   │   ├── TES-070/          # Generated documents
│   │   └── Temp/             # Screenshots
│   ├── TAMICS10/             # Client 2
│   ├── BayCare/              # Client 3
│   ├── ACUITY/               # Client 4
│   └── README.md
│
├── ReusableTools/         # Shared Python utilities
│   ├── new_project_setup.py      # New project provisioning
│   ├── tes070_generator.py       # TES-070 document generator
│   ├── generate_tes070_from_json.py  # JSON to TES-070
│   ├── tes070_analyzer.py        # TES-070 analyzer
│   ├── test_scenario_builder_modern.py  # Modern GUI builder
│   └── automation_examples/      # Playwright examples
│
├── TES-070/               # Shared TES-070 resources
│   ├── Sample_Documents/  # Reference examples (3 samples)
│   └── README.md
│
├── docs/                  # Documentation
│   ├── screenshots/
│   └── diagrams/
│
├── requirements.txt       # Python dependencies
├── SETUP.md              # Setup guide
├── QUICK_START_GUIDE.md  # 3-step workflow guide
├── WORKSPACE_STRUCTURE.md # Detailed structure
├── MULTI_CLIENT_SETUP_COMPLETE.md  # Setup summary
└── README.md             # This file
```

See [WORKSPACE_STRUCTURE.md](WORKSPACE_STRUCTURE.md) for complete details.

## 🎯 What This Workspace Does

### Multi-Client Testing Platform
- **4 Active Clients**: StateOfNewHampshire, TAMICS10, BayCare, ACUITY
- **Complete Isolation**: Each client has separate credentials, test scenarios, and results
- **3-Step Workflow**: Define scenarios → Execute tests → Generate TES-070 documents

### Testing Focus
- **Custom IPA Interfaces**: Test non-CIS integration processes
- **File Channel Automation**: Automatic inbound file processing
- **Approval Workflows**: Multi-step approval testing
- **Data Validation**: Compass SQL queries for verification

### Key Capabilities
- ✅ Browser automation via Playwright
- ✅ TES-070 document generation and analysis
- ✅ FSM UI navigation and testing
- ✅ Work unit monitoring and validation
- ✅ Screenshot capture and embedding
- ✅ Data Fabric API integration

## 🛠️ Key Tools

### 5-Step Workflow (Recommended)
The easiest way to create TES-070 documents:

1. **New Project Setup (One-Time)** - Provision new client folder with credentials
2. **Interface Step 0: Generate Test Data** - Create fresh test data files with current dates
3. **Interface Step 1: Define Test Scenarios** - Launch modern GUI to create JSON file
4. **Interface Step 2: Execute Tests in FSM** - Run tests and capture screenshots
5. **Interface Step 3: Generate TES-070** - Create final Word document

See [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) and [docs/PROJECT_PROVISIONING.md](docs/PROJECT_PROVISIONING.md) for details.

### TES-070 Generator
Generate TES-070 documents from JSON:
```bash
python ReusableTools/generate_tes070_from_json.py Projects/{ClientName}/TestScripts/inbound/{interface_id}_test_scenarios.json
```

### TES-070 Analyzer
Analyze existing test results documents:
```bash
python ReusableTools/tes070_analyzer.py "TES-070/Sample_Documents/your_document.docx"
```

### Test Scenario Builder GUI
Visual interface for creating test scenarios:
```bash
python ReusableTools/test_scenario_builder_gui.py
```

## 📚 Documentation

### Quick References
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - 3-step workflow for consultants
- **[WORKSPACE_STRUCTURE.md](WORKSPACE_STRUCTURE.md)** - Complete folder structure and client details
- **[SETUP.md](SETUP.md)** - Installation and setup guide

### Steering Files (AI Guidance)
Located in `.kiro/steering/`:
- `00_Index.md` - Overview and quick reference
- `01_FSM_Navigation_Guide.md` - FSM UI navigation
- `02_RICE_Methodology_and_Specifications.md` - RICE analysis
- `03_IPA_and_IPD_Complete_Guide.md` - IPA design
- `04_FSM_Business_Classes_and_API.md` - API integration
- `05_Compass_SQL_CheatSheet.md` - SQL queries
- `06_Infor_OS_Data_Fabric_Guide.md` - Data Fabric APIs
- `07_CIS_Configurable_Integration_Solution.md` - CIS testing
- `08_TES070_Standards_and_Generation.md` - TES-070 document standards

### Client-Specific Documentation
Each client folder has its own README:
- `Projects/StateOfNewHampshire/README.md`
- `Projects/TAMICS10/README.md`
- `Projects/BayCare/README.md`
- `Projects/ACUITY/README.md`

## 🔒 Security

**CRITICAL**: Never commit credentials!
- All credential files are git-ignored
- Each client has separate credentials in `Projects/{ClientName}/Credentials/`
- Passwords stored in `.env.passwords` files
- ION API keys in `*.ionapi` files
- See `.gitignore` for complete exclusion list

### Credential Files Per Client
```
Projects/{ClientName}/Credentials/
├── .env.fsm          # FSM URLs and usernames
├── .env.passwords    # Passwords (git-ignored)
└── *.ionapi          # ION API credentials (git-ignored)
```

## 🤝 Team Collaboration

### For New Team Members
1. Clone this repository
2. Follow [SETUP.md](SETUP.md) instructions
3. Ask admin for client credentials
4. Add credentials to `Projects/{ClientName}/Credentials/` folder
5. Read [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
6. Start with "Interface Step 1: Define Test Scenarios" hook

### What to Commit
✅ Python scripts and tools in `ReusableTools/`
✅ Steering files and documentation
✅ Test scenario JSON files (optional)
✅ requirements.txt and SETUP.md
✅ .gitignore

### What NOT to Commit
❌ `Projects/{ClientName}/Credentials/` folder contents
❌ `Projects/{ClientName}/Temp/` folder contents
❌ Generated TES-070 documents (unless required)
❌ __pycache__/ folders
❌ *.ionapi files
❌ .env* files

## 🧪 Testing Workflow

### Using the 5-Step Workflow (Recommended)
1. **New Project Setup (One-Time)** - Click hook, provide credentials, structure created
2. **Interface Step 0: Generate Test Data** - Click hook, fresh test data files created
3. **Interface Step 1: Define Test Scenarios** - Click hook, GUI launches, create JSON
4. **Interface Step 2: Execute Tests in FSM** - Click hook, run tests, capture screenshots
5. **Interface Step 3: Generate TES-070** - Click hook, generate Word document

See [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) and [docs/PROJECT_PROVISIONING.md](docs/PROJECT_PROVISIONING.md) for complete instructions.

### Manual Testing Workflow
1. **Trigger IPAs**: Use Playwright to navigate FSM and start processes
2. **Monitor Execution**: Track work unit IDs and status
3. **Document Errors**: Capture UI error messages (not logs)
4. **Validate Data**: Query FSM via UI or Compass SQL
5. **Report Results**: Generate TES-070 format evidence

## 🌟 Available Clients

| Client | Environment | Tenant |
|--------|-------------|--------|
| StateOfNewHampshire | Production | NMR2N66J9P445R7P_AX4 |
| TAMICS10 | Sandbox/POC | TAMICS10_AX1 |
| BayCare | Training | BAYCAREHS_TRN |
| ACUITY | Test | ACUITY_TST |

See [WORKSPACE_STRUCTURE.md](WORKSPACE_STRUCTURE.md) for complete details.

## 🆘 Support

- Check steering files in `.kiro/steering/`
- Review tool documentation in `ReusableTools/`
- See [SETUP.md](SETUP.md) for troubleshooting
- Ask Kiro for help! 🤖

## 📝 License

Internal use only - Infor FSM implementation team.
