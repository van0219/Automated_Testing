# Reusable Tools

Collection of reusable Python tools for FSM automated testing, document analysis, and test result generation.

## Project Setup Tools

### New Project Setup

**new_project_setup.py** - Provision new client projects with complete folder structure
- Creates complete project folder structure for new clients
- Generates credential file templates (.env.fsm, .env.passwords)
- Auto-generates project README with tenant information
- Part of 5-step TES-070 workflow (New Project Setup - one-time)
- Triggered by "New Project Setup" hook

**What Gets Created:**
```
Projects/{ClientName}/
├── Credentials/
│   ├── .env.fsm              # FSM login credentials
│   └── .env.passwords        # Passwords + SFTP credentials
├── TestScripts/
│   ├── inbound/
│   ├── outbound/
│   ├── approval/
│   └── test_data/
│       └── README.md
├── TES-070/Generated_TES070s/
├── Temp/
└── README.md
```

**Usage:**
```bash
# Interactive mode (recommended)
python ReusableTools/new_project_setup.py
# Script will prompt for all information including optional SFTP paths

# Programmatic mode
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
    sftp_password="sftp-pass"
    # sftp_inbound_path and sftp_outbound_path are optional
)
```

**Note:** SFTP paths are optional defaults. Each interface may use different paths. Add interface-specific paths to `.env.passwords` as needed.

**Documentation:** See `docs/PROJECT_PROVISIONING.md` for complete guide

## Core Testing Tools

### FSM Field Discovery

**fsm_field_discovery.py** - Query FSM API for valid business class field names
- Uses OAuth2 authentication (.ionapi files or .env files)
- Returns all valid field names for a business class
- Used in Step 0 to ensure test data has correct FSM field names
- Kiro (AI) analyzes results and selects which fields to include

```python
from ReusableTools.fsm_field_discovery import discover_fsm_fields

fields = discover_fsm_fields(
    business_class='GLTransactionInterface',
    credentials_dir='Projects/TAMICS10/Credentials',
    tenant='TAMICS10_AX1'
)
# Returns: {'all': [list of all valid field names], 'required': [], 'optional': []}
```

### Test Data Generator

**test_data_generator.py** - Generate test data files with Kiro-selected fields
- Creates valid, invalid, duplicate, empty, and business error scenarios
- Uses field names selected by Kiro after FSM API discovery
- Generates CSV files with current dates and realistic values

```python
from ReusableTools.test_data_generator import generate_all_test_scenarios

# Kiro provides field list after analyzing FSM API response
selected_fields = ['FinanceEnterpriseGroup', 'AccountingEntity', 'PostingDate', ...]

generate_all_test_scenarios(
    output_dir='Projects/StateOfNewHampshire/TestScripts/test_data',
    interface_id='INT_FIN_013',
    field_names=selected_fields
)
```

### Test Scenario Builder

**test_scenario_builder_modern.py** - Modern GUI for creating test scenarios
- Beautiful 2026 design with card-based interface
- Smart workflow: Select interface type, scenarios auto-load from templates
- Templates stored in `.kiro/templates/` (inbound/outbound/approval)
- Single-screen layout with scrollable sidebar and scenario panels
- Saves to `Projects/{ClientName}/TestScripts/{interface_type}/`
- Part of 4-step TES-070 workflow (Interface Step 1: Define Test Scenarios)

**Template Files:**
- `.kiro/templates/inbound_interface_template.json` - 3 inbound scenarios
- `.kiro/templates/outbound_interface_template.json` - 3 outbound scenarios
- `.kiro/templates/approval_workflow_template.json` - 3 approval scenarios

### SFTP Helper

**sftp_helper.py** - SFTP operations for file upload/download
- Upload test data files to SFTP servers
- Download output files for validation
- Supports .env credential files
- Used in Step 2 for test execution

```python
from ReusableTools.sftp_helper import upload_file, load_sftp_credentials

creds = load_sftp_credentials('Projects/StateOfNewHampshire/Credentials/')
upload_file('test_data/GLTRANSREL_valid.csv', '/Infor_FSM/Inbound/', creds)
```

## TES-070 Generation Tools

### TES-070 Generator

**tes070_generator.py** - TES-070 document generator
- Generate properly formatted TES-070 test results documents
- Supports test scenarios, steps, and evidence

### JSON to TES-070 Converter

**generate_tes070_from_json.py** - Convert test scenario JSON to TES-070 .docx
- Integrates screenshots from test execution
- Part of 4-step TES-070 workflow (Interface Step 3: Generate TES-070)
- Reads JSON from `Projects/{ClientName}/TestScripts/{interface_type}/`
- Outputs to `Projects/{ClientName}/TES-070/Generated_TES070s/`

```bash
python ReusableTools/generate_tes070_from_json.py Projects/StateOfNewHampshire/TestScripts/inbound/INT_FIN_013_test_scenarios.json
```

## Document Analysis Tools

### PDF Study Reader

**pdf_study_reader.py** - Comprehensive PDF document analysis
- Extract text, tables, and metadata from PDF documents
- Useful for analyzing specification documents (ANA-050, DES-020)

### DOCX Image Extractor

**docx_image_extractor.py** - Extract images from .docx files with context
- Extract images with surrounding text context
- Useful for analyzing TES-070 documents and other Word files

### TES-070 Analyzer

**tes070_analyzer.py** - Complete TES-070 document analyzer
- Extract text and images from TES-070 test results documents
- OCR support for image-based content
- Comprehensive analysis of test evidence

## 5-Step TES-070 Workflow

These tools support the complete testing workflow:

1. **New Project Setup (One-Time)** → `new_project_setup.py` - Provision new client project
2. **Interface Step 0: Generate Test Data** → `fsm_field_discovery.py` + `test_data_generator.py`
3. **Interface Step 1: Define Test Scenarios** → `test_scenario_builder_modern.py`
4. **Interface Step 2: Execute Tests in FSM** → `sftp_helper.py` + Playwright automation
5. **Interface Step 3: Generate TES-070** → `generate_tes070_from_json.py`

## Usage

Import tools directly in your test scripts:

```python
from ReusableTools.fsm_field_discovery import discover_fsm_fields
from ReusableTools.test_data_generator import generate_all_test_scenarios
from ReusableTools.sftp_helper import upload_file, load_sftp_credentials
from ReusableTools.pdf_study_reader import PDFStudyReader
from ReusableTools.docx_image_extractor import extract_images_from_docx
from ReusableTools.tes070_analyzer import analyze_tes070
```

## Automation Examples

The `automation_examples/` folder contains Playwright automation examples for FSM testing.

## Purpose

These tools support FSM automated testing by:
- Discovering correct FSM field names via API
- Generating test data with proper field names and current dates
- Creating test scenario definitions
- Uploading/downloading files via SFTP
- Analyzing specification documents to understand requirements
- Extracting test evidence from TES-070 documents
- Generating properly formatted TES-070 test results documents
