---
inclusion: always
---

# FSM Automated Testing Guide

## Workspace Purpose

This workspace supports FSM (Financials & Supply Management) automated testing using RICE
methodology (Reports, Interfaces, Conversions, Enhancements). Focus on testing existing FSM
functionality, not developing new IPA processes or integrations.

**Primary Activities**:

- Test existing IPAs, CIS interfaces, and FSM functionality
- Automate FSM UI testing with Playwright
- Generate test data and TES-070 documentation
- Validate data using Compass SQL and FSM APIs

**Out of Scope**:

- Building new IPA processes or .lpd files
- Designing custom workflows or activity nodes
- Developing custom integrations from scratch

## Workspace Structure

### Client Projects (Primary Location)

`Projects/{ClientName}/` - All client-specific work:

- `Credentials/` - FSM credentials (.env.fsm, .env.passwords, *.ionapi) - NEVER commit
- `TestScripts/` - Test scenarios and data
  - `inbound/`, `outbound/`, `approval/` - Organized by interface type
  - `test_data/` - CSV/JSON test data files
- `TES-070/` - Test documentation
  - `Generated_TES070s/` - Generated test results
  - `Approval_TES070s_For_Regression_Testing/` - Original approval TES-070s
- `Temp/` - Test execution screenshots and temporary files

### Reusable Tools

`ReusableTools/` - Python utilities for cross-project use:

- `new_project_setup.py` - Provision new client projects
- `fsm_field_discovery.py` - Query FSM API for valid field names
- `test_data_generator.py` - Generate test data
- `test_scenario_builder_modern.py` - GUI for creating test scenarios
- `generate_tes070_from_json.py` - Convert JSON to TES-070 documents
- `tes070_analyzer.py` - Analyze existing TES-070 documents
- `sftp_helper.py` - SFTP operations
- `testing_framework/` - Automated testing framework
- `automation_examples/` - Playwright automation examples

### File Organization Rules

**CRITICAL**: Always place files in correct locations:

- Client-specific files → `Projects/{ClientName}/`
- Reusable utilities → `ReusableTools/`
- Documentation screenshots → `docs/screenshots/`
- Test execution screenshots → `Projects/{ClientName}/Temp/`

## Communication Style

- Professional yet conversational - like a knowledgeable FSM colleague
- Use emojis, bullets, and code blocks for clarity
- Be confident and direct - avoid robotic language
- Never mention steering files or documentation sources
- If asked to build/develop IPAs, redirect to testing existing functionality
- Never mention "AI", "LLM", "model", or "assistant" - respond as a knowledgeable colleague

## Critical Testing Rules

1. **User Control**: "wait" = pause, "stop" = halt immediately
2. **Browser Efficiency**: Keep browser open across scenarios - close only when complete
3. **FSM Navigation**: Always expand sidebar (☰) before navigating
4. **Browser Zoom**: Use Ctrl+Minus 3x (NOT CSS zoom)
5. **Record Access**: Double-click to open, single-click only selects
6. **Data Queries**: Call Data Catalog API before writing Compass SQL
7. **Large Datasets**: >1M records → use Data Orchestrator/Warehouse (not IPA)
8. **JavaScript**: IPA uses ES5 only (Mozilla Rhino 1.7R4) - NO ES6 features
9. **File Systems**: FSM File Storage ≠ SFTP - use File Channels to bridge
10. **WorkUnit API**: Not exposed - use Process Server Administrator UI
11. **Date Format**: YYYYMMDD (no separators)
12. **Error Documentation**: Document UI error messages only - do NOT analyze work unit logs
13. **Credentials**: NEVER commit to git, NEVER log, ALWAYS read from Credentials/ at runtime
14. **Data Validation**: Filter by RunGroup field to identify test records
15. **Framework Execution**: Testing framework MUST run in Kiro's execution context
    (Playwright MCP tools only available when Kiro executes code directly)

## Quick Decision Trees

### Data Volume → API Selection

| Records | Recommended API             | Notes                               |
|---------|-----------------------------|-------------------------------------|
| <10K    | Data Lake API               | Simpler filter syntax               |
| 10K-1M  | Compass API via IPA         | Implement pagination, manage memory |
| >1M     | Data Orchestrator/Warehouse | Avoid IPA memory limits             |
| Joins   | Metagraph API/Warehouse     | Cross-object queries                |
| Raw BOD | ION OneView API             | Troubleshooting                     |

### IPA vs LPL Requirements

| Need                                                              | Solution       |
|-------------------------------------------------------------------|----------------|
| Data integration, file processing, scheduled jobs, API calls      | IPA            |
| UI modifications, field defaults, validation rules, form behavior | LPL            |
| Approval workflows with UI, triggered processes                   | Both IPA + LPL |

## FSM Credentials & Security

**Location**: `Projects/{ClientName}/Credentials/`

- `.env.fsm` - Environment URLs and usernames
- `.env.passwords` - User passwords and SFTP credentials
- `*.ionapi` - ION API OAuth2 credentials

**Security Rules** (CRITICAL):

- NEVER commit credential files to git
- NEVER log credentials or tokens
- NEVER hardcode credentials
- ALWAYS read from Credentials/ at runtime

**Available Environments**:

- ACUITY_TST - Cloud Identities only (best for testing, real data)
- TAMICS10_AX1 - Cloud or Windows (POC, limited data)
- ACUITY_PRD - Cloud Identities only (production, restricted)

## FSM Navigation Best Practices

**Access Path**: Portal > Applications > See more > Financials & Supply Management

**Common Roles**:

- Integration Architect - CIS, File Creation Utility
- Process Server Administrator - Process Definitions, File Channels, Work Units
- Service Definitions - Configuration
- Payables Manager - Invoice Management

**Navigation Rules**:

- Expand sidebar (☰) before navigating
- Use Search bar for comprehensive lists (not homepage widgets)
- Double-click to open records (single-click only selects)
- Use browser zoom Ctrl+Minus 3x (NOT CSS zoom)

## RICE Methodology

**Categories**:

- **R**eports - Data outputs (BI reports, FSM Lists, Spreadsheet Designer)
- **I**nterfaces - Data exchange (IPA, CIS)
- **C**onversions - Legacy migration (one-time or phased data loads)
- **E**nhancements - Customizations (IPA + LPL combination)

**Specification Documents**:

- ANA-050 - Functional spec (business requirements)
- DES-020 - Technical spec (implementation details)
- Combined ANA-050 - Modern format (functional + technical in one)
- TES-070 - Test results (evidence, pass/fail, validation)

## IPA Architecture Essentials

**Core Components**:

- IPA - Workflow automation engine
- IPD - Eclipse IDE (v9.0.1, Java 17) for process design
- LPD Files - Process definitions (XML format)
- Work Units - Execution instances with logs and variables
- JavaScript - Mozilla Rhino 1.7R4 (ES5 only - NO ES6)

**File Operations** (CRITICAL):

- FSM File Storage (Cloud) → File Access (ACCFIL) nodes only
- SFTP Servers (External) → FTP nodes only
- File Channels → Bridge between SFTP and FSM File Storage

**File Channels** (Auto-Trigger):

- Purpose: Auto-trigger custom IPA when files arrive
- Location: Process Server Administrator > Channels Administrator > File Channels
- Architecture: 1 Channel → Many File Receivers (1-to-many)
- Flow: Channel scans SFTP → Receiver matches pattern → Triggers IPA
- Scan Interval: Configurable (typically 5 minutes, minimum 1 minute)
- CIS Incompatibility: File Channels bypass CIS - use CIS built-in scheduling instead

**Testing Wait Times**:

- Known interval: Wait 1 full cycle + 30s buffer (e.g., 5.5 min for 5-min interval)
- Unknown interval: Wait 6 minutes
- Best: Active monitoring - refresh Work Units every 30s, timeout after 10 min
- Quick test: Right-click channel > "Scan Now"

**Memory Constraint** (CRITICAL):

- Work unit limit: 100GB total memory
- Memory accumulates in pagination loops
- For >1M records: Use Data Orchestrator/Warehouse (not IPA)
- Always clear variables in pagination loops

## FSM Business Classes & API

**Key Business Classes**:

- GLTransactionInterface - GL staging
  - Status: 0=Unreleased, 1=Released, 2=Posted, 3=Error
- GeneralLedgerTransaction - Posted GL
  - Status: 0=Unreleased, 1=Released, 6=Posted, 7=Approved, 8=Rejected, 9=Suspended
- GLTransactionDetail - Transaction details (includes project/labor data)

**API Integration Methods**:

- Landmark (LM) - Ampersand-separated strings for simple CRUD, single records
- WebRun (WEBRN) - JSON payloads for complex operations, OAuth2

**Required Context Fields** (always include in API calls):

- FinanceEnterpriseGroup, AccountingEntity
- PostingDate (YYYYMMDD format)
- \_dataArea, \_module, \_objectName, \_actionName

**OAuth2 Authentication**:

- Credentials: `Projects/{ClientName}/Credentials/{TENANT}.ionapi`
- Token lifetime: 3600 seconds (1 hour)
- Username format: `{TENANT}#{encoded_username}`
- Client ID format: `{TENANT}~{client_id}`
- Always implement token refresh for long-running processes
- Security: NEVER commit .ionapi files, NEVER log tokens

**WorkUnit API Limitation**: WorkUnit business class (pfi module) is NOT exposed via API.
Use Process Server Administrator UI or log parsing instead.

## Compass SQL Essentials

**Critical Rules**:

- READ-ONLY: No INSERT, UPDATE, DELETE, CREATE
- CAST behavior: Returns NULL on failure (not error) - always check for NULL
- Date format: YYYYMMDD (no separators)
- Identifiers: Use double quotes for names with spaces/hyphens/numbers/reserved words

**Supported Features**:

- Clauses: SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT/OFFSET, UNION, WITH (CTE)
- Joins: INNER, LEFT OUTER, RIGHT, CROSS
- Functions: COUNT, SUM, AVG, MIN, MAX, ROUND, ABS
- Subqueries: WHERE, FROM, SELECT contexts

**Common Patterns**:

```sql
-- Pagination
LIMIT 1000 OFFSET 0     -- page 1
LIMIT 1000 OFFSET 1000  -- page 2

-- Safe conversion
WHERE CAST(column AS type) IS NOT NULL

-- Cross-format join
SELECT * FROM json_obj JOIN dsv_obj ON json_obj.id = dsv_obj.id
```

**Limitations**:

- Query timeout: 60 minutes max
- No window functions (limited support)
- No stored procedures or UDFs

## Data Fabric APIs

**Key APIs**:

- Compass API - SQL queries on Data Lake (100K rows/page, unlimited total)
- Data Lake API - Object metadata & payloads (10K max)
- Data Catalog API - Metadata registry (call FIRST before queries)
- Ingestion API - Direct data upload (ZLIB compressed, 200 calls/min)
- Metagraph API - Virtual joins (no data duplication)
- Orchestrator API - Workflow automation (API only, no UI)
- Data Warehouse API - Models, tables, views (incremental loading)
- ION OneView API - Raw BOD retrieval (troubleshooting)

**OAuth2 Authentication**:

- Credentials: `Projects/{ClientName}/Credentials/{TENANT}.ionapi`
- Token lifetime: 2 hours (7200 seconds)
- Security: NEVER commit .ionapi files, NEVER log tokens, always implement token refresh

## Testing Workflow

1. **Trigger IPAs**: Use Playwright to navigate FSM UI
   - Expand sidebar (☰) first, use Search bar, double-click to open
2. **Monitor Execution**: Track work unit IDs from Process Server Administrator,
   wait for completion
3. **Document Errors**: Document UI error messages only
   - Record work unit ID, timestamp, context - NO work unit log analysis
4. **Validate Data**: Check FSM data via UI or Compass SQL
   - Call Data Catalog API first, filter by RunGroup field for test records
5. **Report Results**: Clear pass/fail evidence, work unit IDs, UI error messages,
   expected vs actual behavior, screenshots

**Multi-Scenario Testing** (CRITICAL): Keep browser open across all scenarios - close only
when complete. Benefits: eliminates repeated logins (~2 min/scenario saved), maintains FSM
session state, faster navigation.

## Testing Patterns by Interface Type

### Inbound Interface Testing

**CRITICAL**: Execute ONE scenario at a time - NEVER upload all files simultaneously

**Why Sequential Execution**:

- Proper documentation - isolated screenshots for TES-070
- Data isolation - avoid duplicate records across test files
- Clean evidence - clear, isolated test results

**Custom IPA with File Channel (Automatic)**:

1. Upload ONE test file to SFTP
2. Wait for File Channel scan
   - Best: Active monitoring - refresh Work Units every 30s, timeout 10 min
   - Alternative: Wait 1 scan cycle + 30s buffer
   - Quick: Right-click channel > "Scan Now"
3. File Receiver auto-triggers IPA
4. Check work unit status
5. Open work unit > Variables tab to confirm filename
6. Validate data via UI or Compass SQL
7. Document UI errors
8. Complete scenario before next test

**CIS or Manual IPA (Manual/Scheduled)**:

1. Upload ONE test file
2. Manually trigger via Integration Architect (CIS) or Process Server Administrator (IPA)
3. Check work unit status
4. Validate data
5. Document UI errors
6. Complete scenario before next test

### Outbound Interface Testing

1. Trigger IPA manually or via schedule
2. IPA queries data (Compass API or Landmark)
3. IPA writes file to FSM File Storage
4. File Channel transfers to SFTP
5. Validate output file exists and contains expected data
6. Document UI errors

### Approval Flow Testing

1. Trigger IPA (release invoice, submit for approval)
2. IPA creates User Actions for approvers
3. Submit approval via FSM UI
4. Validate status change
5. Verify expected workflow behavior
6. Document UI errors

## Common Pitfalls to Avoid

1. Forgetting to expand sidebar before navigation
2. Using CSS zoom instead of browser zoom (Ctrl+Minus 3x)
3. Single-clicking records (use double-click to open)
4. Using homepage widgets instead of Search bar
5. Not calling Data Catalog API before Compass queries
6. Using IPA for >1M records (use Data Orchestrator/Warehouse)
7. Not implementing pagination for large datasets
8. Forgetting to clear variables in pagination loops
9. Using ES6 JavaScript in IPA (ES5 only)
10. Attempting to call WorkUnit API (not exposed)

## Key System Constraints

- No PFI module API - use browser automation for Work Units
- File Channels trigger IPAs at Process Server level (incompatible with CIS)
- CIS uses manual/scheduled triggers only (built-in scheduling)
- Work unit logs NOT analyzed - document UI errors only
- IPA memory limit: 100GB (use Data Orchestrator for >1M records)
- Focus on observable behavior, not internal logs

## CIS (Configurable Integration Solution)

**Overview**: Custom integration accelerator framework (LPL + IPA) deployed to each client
tenant. Configure instead of custom-code for faster delivery.

**Deployment**: Each tenant gets isolated CIS installation. Multi-tenant clients need CIS
per tenant (TRN, TST, PP1, PRD).

**When to Use CIS vs Custom IPA**:

- Use CIS: Standard outbound/inbound file interfaces, manual or scheduled triggering,
  standard formats
- Use Custom IPA: Automatic file-based triggering (File Channels), complex business logic,
  approval workflows

**Testing CIS Interfaces**:

1. Navigate to Integration Architect > Configurable Integration > Outbound/Inbound
2. Check Active status (must be Yes)
3. Right-click row > "Schedule Trigger" or "Trigger"
4. Monitor "Last Run Status" (Ready=success, Error=failed)
5. Click "Last Work Unit" link if errors
6. Validate output file or data changes

**Critical Rules**:

- Always use right-click context menu (columns can be personalized/hidden)
- Active=No interfaces must be activated first (right-click > "Activate")
- CIS is for Interfaces only (I in RICE)
- Uses pre-built generic IPAs - no custom development needed

## Related Steering Files

Load on-demand using discloseContext tool when needed:

- 01_FSM_Navigation_Guide.md - FSM UI, Playwright automation, Process Server Admin
- 02_RICE_Methodology_and_Specifications.md - RICE analysis, ANA-050/DES-020 specs,
  IPA vs LPL
- 03_IPA_and_IPD_Complete_Guide.md - IPA design, LPD files, activity nodes, S3 migration
- 04_FSM_Business_Classes_and_API.md - Business classes, Landmark/WebRun, GL/AP/AR
- 05_Compass_SQL_CheatSheet.md - Compass SQL queries, Data Fabric queries
- 06_Infor_OS_Data_Fabric_Guide.md - Data Fabric APIs, Compass, Data Lake, Orchestrator
- 07_CIS_Configurable_Integration_Solution.md - CIS interfaces, outbound/inbound testing
- 08_TES070_Standards_and_Generation.md - TES-070 standards, formatting, evidence
- 09_Work_Unit_Analysis.md - Work unit logs, error patterns, troubleshooting
- 11_Kiro_Agent_Automation_Guide.md - Kiro automation: hooks, skills, powers, steering,
  specs, subagents, web tools

**Steering File System**:

- 00_Index.md (this file) - inclusion: always - Automatically loaded
- 01-09, 11 - inclusion: auto - Loaded on-demand when keywords match task context

## Automated Testing Framework

**Location**: `ReusableTools/testing_framework/`

**Purpose**: Automates FSM interface testing with evidence collection and TES-070 generation.
Provides real-time progress reporting so you can see exactly what's happening during test execution.

**Key Features**:

- State management with `{{state.variable}}` interpolation
- Pluggable actions and validators
- Adaptive polling for work unit monitoring (10s → 30s → 60s)
- Real-time progress reporting (no more "stuck" feeling)
- Automatic screenshot capture
- Professional TES-070 Word document generation
- OAuth2 token management with auto-refresh
- Unique test identifiers: `AUTOTEST_<timestamp>_<random>`

**Architecture**:

- Engine: TestState, StepEngine, ValidatorEngine
- Integration: PlaywrightClient (Python Playwright), SFTPClient, FSMAPIClient, WorkUnitMonitor, CredentialManager
- Actions: fsm_login, fsm_payables, fsm_workunits, sftp_upload, wait, api_call
- Validators: file, workunit, api
- Orchestration: TestOrchestrator, ApprovalExecutor, InboundExecutor
- Evidence: ScreenshotManager, TES070Generator

**Execution Methods**:

1. **Via Hook** (Recommended - User-Friendly):
   - Click "Approval Step 2: Execute Approval Tests" hook
   - Select client and scenario file interactively
   - Enter FSM credentials when prompted
   - Watch real-time progress in console
   - Browser opens on 2nd screen (visible automation)

2. **Command Line** (Direct):
   ```bash
   python ReusableTools/run_approval_tests_v2.py --client ClientName --scenario path/to/scenario.json --environment ENV --url "FSM_URL" --username "USERNAME" --password "PASSWORD"
   ```

3. **Interactive Wrapper** (Prompts for credentials):
   ```bash
   python execute_approval_tests.py
   ```

**Real-Time Progress Reporting** (NEW):

The framework now shows exactly what's happening as tests execute:

```
================================================================================
SCENARIO 1/3: 3.1 - Valid Invoice Approval
================================================================================

  ⏳ Step 1.1: Login to FSM
     ✅ PASSED

  ⏳ Step 1.2: Navigate to Payables
     ✅ PASSED

  ⏳ Step 1.3: Create Invoice
     ❌ FAILED: Element not found
     ⚠️  Critical step failed - stopping scenario execution

❌ Scenario 3.1 FAILED
```

**Benefits**:
- See current scenario and step being executed
- Immediate pass/fail feedback (✅/❌)
- Error messages shown immediately with context
- Know when tests are complete
- No more wondering if it's stuck

**Framework Redesign (March 2026)**:

- ✅ Migrated from Playwright MCP to standard Python Playwright
- ✅ Standalone execution (no Kiro dependency)
- ✅ CSS selector-based navigation (no accessibility snapshots)
- ✅ Multi-selector fallback strategy for reliability
- ✅ Visible browser automation on 2nd screen
- ✅ Headless mode for CI/CD pipelines
- ✅ All FSM actions rewritten (fsm_login, fsm_payables, fsm_workunits)
- ✅ Real-time progress reporting to console

**State Variable Interpolation**:

- `{{state.run_group}}` - Unique test identifier
- `{{state.password}}` - FSM password from .env.passwords
- `{{state.work_unit_id}}` - Work unit ID from wait actions
- `{{state.uploaded_file}}` - Last uploaded filename
- `{{state.api_record_count}}` - Record count from API calls
- `{{TODAY_YYYYMMDD}}` - Current date (YYYYMMDD format)
- `{{TODAY_PLUS_7_YYYYMMDD}}` - Current date + 7 days
- `{{FSM_PORTAL_URL}}` - Mapped to `{{state.fsm_url}}`
- `{{FSM_USERNAME}}` - Mapped to `{{state.fsm_username}}`

**JSON Compatibility**:

Framework accepts both field names for flexibility:
- `interface_id` (for interface testing - INT_XXX)
- `extension_id` (for approval testing - EXT_XXX)

**Benefits**:

- Token Efficiency: Manual (~50-100 MCP calls) vs Framework (load once, minimal tokens)
- Speed: Manual (30-60 min) vs Framework (5-10 min)
- Consistency: 100% consistent logic every time
- Evidence: Automatic capture with proper naming
- TES-070: Automatic generation
- Visibility: Real-time progress reporting

**Security**:

- Credentials never logged or exposed
- OAuth2 tokens auto-refresh before expiration
- All credentials read from `Projects/{ClientName}/Credentials/` at runtime
- Test identifiers prevent data collision

## Hook Interactive Pattern

When creating hooks that need user input, use the **INTERACTIVE UI** pattern:

**What "Interactive UI" Means**:

- Kiro presents options in chat (numbered list, bullet points, etc.)
- User sees a UI with selectable items (radio buttons, checkboxes, dropdown)
- User clicks to select option(s) and clicks Submit button
- NOT a text-based question where user types an answer

**Correct Pattern**:

1. Use listDirectory, fileSearch, or grepSearch to discover options
2. Present options as formatted list in chat response
3. Interactive UI appears automatically with Submit button
4. User selects and submits

**Example Flow**:

```text
Kiro: "I found these clients:
1. SONH
2. ClientB
3. ClientC

Which client would you like to use?"

[User sees UI with radio buttons for each option + Submit button]
[User clicks option 2 (ClientB) and clicks Submit]
```

**Why This Works**:

- Listing options triggers automatic interactive UI
- UI shows as modal dialog with selectable items
- Users click to select rather than typing
- Submit button confirms selection

**Implementation Rules**:

- Always present options as a formatted list
- Never ask open-ended questions expecting typed answers
- Never use "userInput tool" in hook prompts
- Let Kiro's UI system handle the selection interface

## TES-070 Testing Workflows - CRITICAL DISTINCTION

**THERE ARE TWO COMPLETELY SEPARATE WORKFLOWS - DO NOT MIX THEM!**

### Workflow A: APPROVAL TESTING (3-Step Process) - For Enhancements (E in RICE)

**Use When**: Testing approval workflows (EXT_FIN_XXX) for regression testing from existing
TES-070 documents

**Hook Prefix**: "Approval Step X"

**Workflow**:

1. **Approval Step 1**: Parse existing TES-070 → Generate JSON scenarios
   - Input: Existing TES-070 document from `Projects/{Client}/TES-070/Approval_TES070s_For_Regression_Testing/`
   - Output: `Projects/{Client}/TestScripts/approval/{EXT_ID}_auto_approval_test.json`
   - Uses `extension_id` field (not `interface_id`)

2. **Approval Step 2**: Execute approval tests → Framework runs with real-time progress
   - Select client and scenario file interactively
   - Enter FSM credentials (URL, username, password)
   - Watch real-time progress in console:
     ```
     SCENARIO 1/3: 3.1 - Valid Invoice Approval
       ⏳ Step 1.1: Login to FSM
          ✅ PASSED
       ⏳ Step 1.2: Navigate to Payables
          ✅ PASSED
     ```
   - Browser opens on 2nd screen (visible automation)
   - TES-070 generated automatically
   - Output: `Projects/{Client}/TES-070/Generated_TES070s/TES-070_{timestamp}_{EXT_ID}.docx`

3. **Approval Step 3**: Review TES-070 → Document already generated
   - Locate generated TES-070 document
   - Verify evidence and screenshots
   - Open in Microsoft Word, press F9 to update TOC
   - Finalize and deliver

**Key Characteristics**:

- Starts with EXISTING TES-070 document (regression testing)
- Tests ENHANCEMENTS (approval workflows, IPA + LPL)
- Extension IDs start with "EXT_" (e.g., EXT_FIN_004)
- No test data generation needed (uses live FSM data)
- No GUI tool - direct JSON generation from TES-070 analysis
- Framework generates TES-070 automatically in Step 2
- Real-time progress reporting (no more "stuck" feeling)
- Immediate pass/fail feedback for each step

**File Locations**:

- Input: `Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/*.docx`
- Scenarios: `Projects/{ClientName}/TestScripts/approval/{extension_id}_auto_approval_test.json`
- Output: `Projects/{ClientName}/TES-070/Generated_TES070s/`

---

### Workflow B: INTERFACE TESTING (4-Step Process) - For Interfaces (I in RICE)

**Use When**: Testing inbound/outbound file interfaces (INT_FIN_XXX) from scratch

**Hook Prefix**: "Interface Step X"

**Workflow**:

1. **Interface Step 1**: Generate test data files
2. **Interface Step 2**: Define scenarios using GUI tool
3. **Interface Step 3**: Execute interface tests → Framework runs, generates TES-070
4. **Interface Step 4**: Review TES-070 → Document already generated

**Key Characteristics**:

- Starts from SCRATCH (no existing TES-070)
- Tests INTERFACES (file uploads, CIS, data exchange)
- Interface IDs start with "INT_" (e.g., INT_FIN_013)
- Requires test data generation (CSV/JSON files)
- Uses GUI tool (test_scenario_builder_modern.py) for scenario creation
- Framework generates TES-070 automatically in Step 3

**File Locations**:

- Test Data: `Projects/{ClientName}/TestScripts/test_data/`
- Scenarios: `Projects/{ClientName}/TestScripts/{inbound|outbound}/{interface_id}_test_scenarios.json`
- Output: `Projects/{ClientName}/TES-070/Generated_TES070s/`

---

## TES-070 Creation Workflow (5-Step Process)

Complete workflow for provisioning projects, generating test data, creating scenarios,
executing tests, and generating TES-070 documents.

**NOTE**: This section describes the INTERFACE workflow (Workflow B above). For APPROVAL
workflow, see "Workflow A" above.

### New Project Setup (One-Time)

**Hook**: "New Project Setup" (userTriggered)

**Purpose**: Provision new client project with complete folder structure and credential
templates

**When**: Before starting work on new client - run ONCE per client

**Workflow**:

1. Click "New Project Setup" hook
2. AI asks: "Do you want to create a new FSM testing project?"
3. If yes: AI runs `python ReusableTools/new_project_setup.py` and tells user to answer
   terminal questions
4. Script prompts for: Client name, Tenant ID, FSM credentials, SFTP details
   (optional defaults)
5. AI shows summary of what was created

**Output**: Fully provisioned project with Credentials/, TestScripts/, TES-070/, Temp/,
README.md

### Interface Step 1: Generate Test Data

**Hook**: "Interface Step 1: Generate Test Data" (userTriggered)

**Purpose**: Generate fresh test data files with current dates and correct FSM field names

**Workflow**:

1. Ask which client/interface and FSM business class name
2. Use fsm_field_discovery.py to query FSM API for valid field names
3. Kiro analyzes discovered fields and selects which to include
   (required fields + commonly used optional fields)
4. Use test_data_generator.py with Kiro's selected field list
5. Generate scenario files (valid, invalid, duplicate, empty, errors)
6. Save to Projects/{ClientName}/TestScripts/test_data/

**Output**: Fresh test data files with current dates and correct FSM field names

### Interface Step 2: Define Test Scenarios

**Hook**: "Interface Step 2: Define Test Scenarios" (userTriggered)

**Purpose**: Launch GUI for test scenario creation

**Workflow**:

1. Launch test_scenario_builder_modern.py GUI
2. User selects interface type (Inbound/Outbound/Approval)
3. 3 predefined scenarios auto-load from templates (.kiro/templates/)
4. User fills interface details and edits scenarios
5. Save JSON to Projects/{ClientName}/TestScripts/{interface_type}/{interface_id}_test_scenarios.json

**Output**: JSON file with test scenario definitions

### Interface Step 3: Execute Tests in FSM

**Hook**: "Interface Step 3: Execute Tests in FSM" (userTriggered) - v2.0.0

**Purpose**: Execute test scenarios using automated testing framework

**Workflow**:

1. Select client and test scenario JSON
2. Verify credentials in Credentials/
3. Framework executes automatically
   - Loads credentials, initializes run_group
   - Executes scenarios, captures screenshots
   - Monitors work units, validates results
   - Generates TES-070
4. Review execution summary

**Critical Rules**:

- Framework MUST run in Kiro's execution context (MCP tools only available here)
- Do NOT run as subprocess (`python run_tests.py` will fail)
- Browser stays open across scenarios for efficiency
- Sequential execution (one scenario at a time)

**Output**: Screenshots captured, results validated, TES-070 generated

### Interface Step 4: Review TES-070 Document

**Hook**: "Interface Step 4: Review TES-070 Document" (userTriggered) - v2.0.0

**Purpose**: Review and finalize TES-070 document (already generated by framework)

**Workflow**:

1. Locate TES-070 document in TES-070/Generated_TES070s/
2. Open in Microsoft Word
3. Press F9 to update Table of Contents
4. Review all sections (title page, test summary, scenario results, screenshots)
5. Add any missing screenshots manually if needed
6. Save and finalize

**Output**: Finalized TES-070 .docx document ready for delivery

### Complete Flow

```text
New Project Setup (One-Time) → Interface Step 1: Generate Test Data →
Interface Step 2: Define Test Scenarios → Interface Step 3: Execute Tests →
Interface Step 4: Review TES-070
```

**Usage**: Run "New Project Setup" once per client, then Steps 1-4 in sequence for each
interface.

## Test Evidence Requirements

Always provide:

- Clear pass/fail evidence
- Work unit IDs for reference
- UI error messages (not logs)
- Expected vs actual behavior
- Screenshots or snapshots
- Actionable recommendations
