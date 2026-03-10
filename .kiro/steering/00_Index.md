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
3. **FSM Navigation**: Use portal navigation menu (grid icon) for applications/roles, FSM sidebar (☰) for within-role navigation
4. **Role Switching**: Use role switcher dropdown in FSM header - do NOT navigate back to portal
5. **Snapshot First**: Always take snapshot before clicking - use refs, never guess selectors
6. **No run_code**: Never use run_code for navigation - use snapshot + click pattern
7. **Browser Zoom**: Use Ctrl+Minus 3x (NOT CSS zoom)
8. **Record Access**: Double-click to open, single-click only selects
9. **Data Queries**: Call Data Catalog API before writing Compass SQL
10. **Large Datasets**: >1M records → use Data Orchestrator/Warehouse (not IPA)
11. **JavaScript**: IPA uses ES5 only (Mozilla Rhino 1.7R4) - NO ES6 features
12. **File Systems**: FSM File Storage ≠ SFTP - use File Channels to bridge
13. **WorkUnit API**: Not exposed - use Process Server Administrator UI
14. **Date Format**: YYYYMMDD (no separators)
15. **Error Documentation**: Document UI error messages only - do NOT analyze work unit logs
16. **Credentials**: NEVER commit to git, NEVER log, ALWAYS read from Credentials/ at runtime
17. **Data Validation**: Filter by RunGroup field to identify test records
18. **Framework Execution**: Testing framework MUST run in Kiro's execution context
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

**CRITICAL**: Approval workflows are ASYNCHRONOUS - IPA runs in background after submission.

**Workflow**:

1. Create transaction (invoice, journal, cash transaction)
2. Submit for approval via FSM UI
3. **Wait for approval IPA to complete** (5-10 minutes)
4. Monitor work unit status (Process Server Administrator > Work Units)
5. Validate status change after work unit completes
6. Verify expected workflow behavior
7. Document UI errors

**Timeline**:
- 0-15 seconds: Submission confirmed, status shows "Pending Approval"
- 15 seconds - 5 minutes: Approval IPA running in background
- 5-10 minutes: Approval IPA completes, custom fields update
- After completion: Status changes (e.g., "Released"), custom fields populated

**Validation Steps**:
1. Navigate to Process Server Administrator > Work Units
2. Search for approval process (by process name or transaction number)
3. Monitor work unit status until "Completed" (use adaptive polling: 10s → 30s → 60s)
4. Return to transaction and refresh page
5. Verify status changed (e.g., "Pending Approval" → "Released")
6. Verify custom fields populated (e.g., SONH Approval Status, Work Unit Reference #)
7. Check Approval Tracking tab for approval actions

**Common Issue**: Custom fields show "Unsubmitted" immediately after submission - this is NORMAL. Fields update AFTER work unit completes (5-10 minutes). Always monitor work units before concluding test failed.

**Test Status**: ✅ Validated with Scenario 3.1 (EXT_FIN_004) - garnishment invoice submission successful, browser automation working end-to-end. See `SCENARIO_3.1_TEST_RESULTS.md` for details.

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

**DEPRECATED - DO NOT USE**

The Python-based testing framework in `ReusableTools/testing_framework/` is deprecated and should not be used for new testing workflows.

**Why Deprecated**:
- Not suitable for production testing workflows
- Does not align with modular subagent architecture vision
- Lacks flexibility for specialized approval types

**Current Testing Approach**:
- Manual execution using MCP Playwright tools directly
- Awaiting platform support for subagent tool inheritance

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

### Workflow A: APPROVAL TESTING (KIRO POWER SOLUTION) - For Enhancements (E in RICE)

**✅ SOLUTION: FSM Approval Testing Power**

A Kiro Power provides automated regression testing for FSM approval workflows using existing TES-070 documents.

**How It Works**:
- Power activates via keywords ("FSM approval testing", "TES-070", "approval workflow")
- Parent agent uses Kiro's built-in MCP Playwright tools (no subagent delegation)
- Power provides instructions and workflows via POWER.md and steering files
- Agent executes tests directly with full MCP tool access

**Why This Works**:
- ✅ Powers provide MCP tools to parent agent (not subagents)
- ✅ No tool inheritance problem (parent has direct access)
- ✅ Modular structure (power bundles everything)
- ✅ Dynamic activation (keywords trigger loading)

**Power Location**: `powers/fsm-approval-testing/`

**Power Structure**:
- `POWER.md` - Power metadata, instructions, workflows
- `steering/tes070-parsing.md` - TES-070 parsing workflow
- `steering/test-execution.md` - Test execution with browser automation
- `steering/evidence-collection.md` - Screenshot and evidence capture
- `README.md` - Installation and usage guide

**Installation**:
1. Open Powers panel (⚡ icon)
2. Click "Add power from Local Path"
3. Select `powers/fsm-approval-testing/`
4. Click Install

**Usage**:
Simply mention keywords in your request:
```
Test the expense invoice approval workflow using TES-070 document EXT_FIN_004
```

Power activates automatically and guides through workflow phases.

**Workflow Phases**:

**Note**: The following workflow applies to REGRESSION TESTING with existing TES-070 documents. For NET NEW TESTING (generic test scripts), adapt execution based on scenario objectives using your FSM knowledge.

1. **Phase 1: Parse TES-070 Document**
   - Run `python ReusableTools/tes070_analyzer.py "<tes070_path>"`
   - Extract document metadata, test summary, scenarios
   - Identify transaction type (ExpenseInvoice, ManualJournal, CashLedgerTransaction)
   - Output: `*_analysis.json`

2. **Phase 2: Create Test Instructions**
   - Run `python ReusableTools/create_test_instructions.py`
   - Extract executable scenarios (skip TOC entries)
   - Create simplified test instructions JSON
   - Validate JSON structure
   - Output: `Projects/{Client}/TestScripts/approval/{extension_id}_test_instructions.json`

3. **Phase 3: Execute Tests**
   - **REGRESSION TESTING**: Follow TES-070 test steps EXACTLY as written - DO NOT interpret, DO NOT deviate, DO NOT create your own steps
   - **NET NEW TESTING**: Use your knowledge and instincts to execute tests based on generic test script objectives
   - Load FSM credentials from `Projects/{Client}/Credentials/`
   - For each scenario:
     * Launch browser (keep open across scenarios)
     * Navigate to FSM portal and login
     * **REGRESSION**: Read each TES-070 step word-by-word and execute exactly what it says
       - If TES-070 says "Staff Accountant role" → Use "Staff Accountant" (NOT "Global Ledger" or similar)
       - If TES-070 says "Process Journals > Create" → Navigate to exactly "Process Journals" then "Create"
       - If TES-070 says "amount below $1,000" → Use $999.99 or $500.00 (NOT $1,000 or more)
     * **NET NEW**: Interpret scenario objectives and create appropriate test steps using FSM knowledge
     * Take snapshots before actions (find element refs)
     * Capture screenshots after critical steps
     * Validate results match expectations
     * If validation fails, STOP and document the issue (regression) or adapt approach (net new)
   - Close browser after all scenarios complete
   - Output: `Projects/{Client}/Temp/evidence/{scenario_id}/`

4. **Phase 4: Report Results**
   - Display summary (total, passed, failed, pass rate)
   - List evidence locations
   - Document any errors or issues

**Supported Approval Types**:
- Expense Invoice Approval (Payables) - EXT_FIN_004 and similar
- Manual Journal Approval (General Ledger) - EXT_FIN_001 and similar
- Cash Ledger Transaction Approval (Cash Management) - EXT_FIN_016 and similar

**MCP Playwright Tools Used**:
- `mcp_playwright_browser_navigate` - Navigate to URLs
- `mcp_playwright_browser_snapshot` - Capture page structure (find elements)
- `mcp_playwright_browser_click` - Click elements
- `mcp_playwright_browser_type` - Type text into fields
- `mcp_playwright_browser_fill_form` - Fill multiple form fields
- `mcp_playwright_browser_take_screenshot` - Capture evidence
- `mcp_playwright_browser_wait_for` - Wait for elements/text

**Note**: These tools are built into Kiro - no external MCP server needed.

**Key Characteristics**:
- ✅ Power-based solution (modular, shareable)
- ✅ Parent agent executes (full MCP tool access)
- ✅ Dynamic activation (keywords)
- ✅ Starts with EXISTING TES-070 document (regression testing)
- ✅ Tests ENHANCEMENTS (approval workflows, IPA + LPL)
- ✅ Extension IDs start with "EXT_" (e.g., EXT_FIN_004)
- ✅ No test data generation needed (uses live FSM data)

**File Locations**:
- Power: `powers/fsm-approval-testing/`
- Input TES-070: `Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/*.docx`
- TES-070 Analysis: `Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/*_analysis.json`
- Test Instructions: `Projects/{ClientName}/TestScripts/approval/{extension_id}_test_instructions.json`
- Evidence Screenshots: `Projects/{ClientName}/Temp/evidence/{scenario_id}/`

**Testing Status**: ✅ Validated - Successfully executed Scenario 3.1 (garnishment auto-approval) on 2026-03-10. Browser automation, FSM navigation, invoice creation, and submission all working correctly. See `SCENARIO_3.1_TEST_RESULTS.md` for complete test results.

**Key Learning**: Approval workflows are asynchronous. After submission, approval IPA runs in background (5-10 minutes). Always monitor work units to verify completion before validating approval status. Custom fields (SONH Approval Status, Work Unit Reference #) update AFTER work unit completes.

**Historical Context**:
- Previous attempts (Python framework, subagent routing) failed due to MCP tool access limitations
- Kiro Power solution solves this by providing tools to parent agent
- See `APPROVAL_TESTING_SOLUTIONS_HISTORY.md` for complete history

---

### Workflow B: INTERFACE TESTING (DEPRECATED) - For Interfaces (I in RICE)

**STATUS**: ⚠️ DEPRECATED - Hooks moved to `.kiro/hooks/backup/`

**Previous Workflow** (4-Step Process with Hooks):

The interface testing workflow used 4 hooks (Interface Steps 1-4) for testing inbound/outbound file interfaces (INT_FIN_XXX) from scratch. These hooks have been deprecated and moved to backup.

**Deprecated Hooks** (now in `.kiro/hooks/backup/`):
- `interface-step1-generate-test-data.kiro.hook.BACKUP`
- `interface-step2-define-test-scenarios.kiro.hook.BACKUP`
- `interface-step3-execute-tests-fsm.kiro.hook.BACKUP`
- `interface-step4-generate-tes070.kiro.hook.BACKUP`

**Why Deprecated**:
- Python-based testing framework not suitable for production workflows
- Does not align with modular power architecture
- Replaced by manual execution using MCP Playwright tools directly

**Current Approach for Interface Testing**:
- Manual test execution using MCP Playwright tools
- Direct browser automation without framework wrapper
- Custom test scripts per interface as needed
- Awaiting future power or improved framework solution

**Key Characteristics** (for reference):
- Started from SCRATCH (no existing TES-070)
- Tested INTERFACES (file uploads, CIS, data exchange)
- Interface IDs started with "INT_" (e.g., INT_FIN_013)
- Required test data generation (CSV/JSON files)
- Used GUI tool (test_scenario_builder_modern.py) for scenario creation

**File Locations** (still valid for manual testing):
- Test Data: `Projects/{ClientName}/TestScripts/test_data/`
- Scenarios: `Projects/{ClientName}/TestScripts/{inbound|outbound}/{interface_id}_test_scenarios.json`
- Output: `Projects/{ClientName}/TES-070/Generated_TES070s/`

---

## Active Hooks

### New Project Setup (One-Time)

**Hook**: "New Project Setup" (userTriggered)

**Purpose**: Provision new client project with complete folder structure and credential templates

**When**: Before starting work on new client - run ONCE per client

**Workflow**:

1. Click "New Project Setup" hook
2. AI asks: "Do you want to create a new FSM testing project?"
3. If yes: AI runs `python ReusableTools/new_project_setup.py` and tells user to answer terminal questions
4. Script prompts for: Client name, Tenant ID, FSM credentials, SFTP details (optional defaults)
5. AI shows summary of what was created

**Output**: Fully provisioned project with Credentials/, TestScripts/, TES-070/, Temp/, README.md

### Load Steering Files

**Hook**: "Load Steering Files" (userTriggered)

**Purpose**: Manually load specific steering files (01-11) into context when needed

**When**: When you need detailed guidance on specific topics (FSM navigation, RICE methodology, IPA design, etc.)

**Workflow**:

1. Click "Load Steering Files" hook
2. AI presents list of available steering files with descriptions
3. Select which steering file(s) to load
4. AI loads selected files using discloseContext tool

**Available Steering Files**:
- 01_FSM_Navigation_Guide.md - FSM UI, Playwright automation
- 02_RICE_Methodology_and_Specifications.md - RICE analysis, specs
- 03_IPA_and_IPD_Complete_Guide.md - IPA design, LPD files
- 04_FSM_Business_Classes_and_API.md - Business classes, APIs
- 05_Compass_SQL_CheatSheet.md - Compass SQL queries
- 06_Infor_OS_Data_Fabric_Guide.md - Data Fabric APIs
- 07_CIS_Configurable_Integration_Solution.md - CIS interfaces
- 08_TES070_Standards_and_Generation.md - TES-070 standards
- 09_Work_Unit_Analysis.md - Work unit logs, troubleshooting
- 10_JSON_Generation_Best_Practices.md - JSON generation
- 11_Kiro_Agent_Automation_Guide.md - Kiro automation features

## Test Evidence Requirements

Always provide:

- Clear pass/fail evidence
- Work unit IDs for reference
- UI error messages (not logs)
- Expected vs actual behavior
- Screenshots or snapshots
- Actionable recommendations
