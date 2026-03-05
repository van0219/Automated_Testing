# FSM Automated Testing Framework Architecture

## Executive Summary

This document defines a **modular, extensible testing framework** for FSM (Financials & Supply Management) that supports all RICE objects (Reports, Interfaces, Conversions, Enhancements).

**Key Features:**
- Type-agnostic test orchestration (approval, inbound, outbound)
- Real-time FSM API validation (not Data Lake/Compass)
- MCP Playwright automation for UI interactions
- Work unit monitoring for IPA process validation
- Automated evidence collection for TES-070 generation

**Design Principles:**
1. **Modularity**: Pluggable executors for different test types
2. **Extensibility**: Easy to add new test types and validations
3. **Reusability**: Common components shared across test types
4. **Maintainability**: Clear separation of concerns
5. **Real-time Validation**: FSM APIs only (no Data Lake dependency)

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Test Scenario Definition](#test-scenario-definition)
3. [Module Structure](#module-structure)
4. [Core Modules](#core-modules)
5. [Integration Modules](#integration-modules)
6. [Evidence Collection](#evidence-collection)
7. [TES-070 Generation](#tes-070-generation)
8. [Potential Risks](#potential-risks)
9. [Implementation Roadmap](#implementation-roadmap)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     TEST DEFINITION LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Approval   │  │   Inbound    │  │   Outbound   │             │
│  │   Template   │  │   Template   │  │   Template   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         ↓                  ↓                  ↓                      │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │         JSON Test Scenario Definition                     │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    TEST ORCHESTRATION LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │              TestOrchestrator (Main Engine)               │      │
│  └──────────────────────────────────────────────────────────┘      │
│         ↓                  ↓                  ↓                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Approval   │  │   Inbound    │  │   Outbound   │             │
│  │   Executor   │  │   Executor   │  │   Executor   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      INTEGRATION LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ FSM API      │  │ Playwright   │  │ Work Unit    │             │
│  │ Validator    │  │ Automation   │  │ Monitor      │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ SFTP         │  │ Evidence     │  │ Credential   │             │
│  │ Manager      │  │ Collector    │  │ Manager      │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      REPORTING LAYER                                 │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │              TES-070 Generator                            │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Layer | Component | Responsibility |
|-------|-----------|----------------|
| **Definition** | JSON Templates | Define test scenarios, steps, validations |
| **Orchestration** | TestOrchestrator | Parse scenarios, route to executors, manage lifecycle |
| **Orchestration** | Executors | Execute test type-specific logic |
| **Integration** | FSM API Validator | Real-time FSM data validation |
| **Integration** | Playwright Automation | UI interactions via MCP |
| **Integration** | Work Unit Monitor | Poll and validate IPA execution |
| **Integration** | SFTP Manager | File upload/download operations |
| **Integration** | Evidence Collector | Aggregate screenshots, logs, API responses |
| **Integration** | Credential Manager | Secure credential loading |
| **Reporting** | TES-070 Generator | Generate formatted test results documents |

---

## Test Scenario Definition

### Unified JSON Schema

All test types (approval, inbound, outbound) use a unified JSON schema with type-specific action and validation configurations.

**File Location**: `Projects/{ClientName}/TestScripts/{interface_type}/{interface_id}_test_scenarios.json`


### Schema Structure

```json
{
  "interface_id": "INT_FIN_013",
  "interface_name": "GL Transaction Interface",
  "interface_type": "inbound|outbound|approval",
  "client_name": "State of New Hampshire",
  "environment": "ACUITY_TST",
  "test_metadata": {
    "author": "Test Engineer Name",
    "created_date": "2026-03-05",
    "version": "1.0"
  },
  "prerequisites": {
    "user_roles": ["Process Server Administrator", "Financials Processor"],
    "test_data_requirements": "Sample GL transaction files",
    "configuration_prerequisites": "File Channel configured and active"
  },
  "scenarios": [
    {
      "scenario_id": "scenario_1",
      "title": "Successful Import",
      "description": "Verify valid data is successfully imported",
      "test_type": "happy_path|error_validation|business_rule_error",
      "test_steps": [
        {
          "step_number": "1",
          "description": "Upload valid CSV file to SFTP server",
          "action": {
            "type": "sftp_upload|ui_action|api_call|wait|validate",
            "target": "sftp://server/path/file.csv",
            "parameters": {
              "test_data_file": "GLTRANSREL_valid.csv",
              "source_path": "Projects/SONH/TestScripts/test_data/",
              "destination_path": "/Infor_FSM/GLTransactionInterface/Inbound/"
            }
          },
          "validation": {
            "type": "file_exists|api_query|ui_check|work_unit_status",
            "expected_result": "File uploaded successfully",
            "validation_query": null
          },
          "screenshot": "01_file_upload",
          "result": "PENDING"
        }
      ],
      "expected_results": [
        "Data successfully imported",
        "All records processed"
      ]
    }
  ]
}
```

### Action Types

| Action Type | Description | Required Parameters |
|-------------|-------------|---------------------|
| `sftp_upload` | Upload file to SFTP | `test_data_file`, `source_path`, `destination_path` |
| `sftp_download` | Download file from SFTP | `remote_path`, `local_path` |
| `ui_action` | Playwright UI interaction | `navigation_path`, `element_ref`, `action` |
| `api_call` | FSM API operation | `business_class`, `action`, `filters`, `payload` |
| `wait` | Wait for condition | `target`, `timeout_seconds`, `poll_interval_seconds` |
| `validate` | Validation check | `type`, `expected_result`, `validation_query` |

### Validation Types

| Validation Type | Description | Query Structure |
|-----------------|-------------|-----------------|
| `file_exists` | Check file presence | `{"path": "/path/to/file"}` |
| `api_query` | FSM API validation | `{"business_class": "...", "filters": {...}}` |
| `ui_check` | UI element validation | `{"element_ref": "...", "expected_text": "..."}` |
| `work_unit_status` | Work unit completion | `{"process_name": "...", "status": "Completed"}` |


---

## Module Structure

### Recommended Directory Structure

```
ReusableTools/
├── testing_framework/
│   ├── __init__.py
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── test_orchestrator.py          # Main orchestration engine
│   │   ├── approval_executor.py          # Approval workflow executor
│   │   ├── inbound_executor.py           # Inbound interface executor
│   │   ├── outbound_executor.py          # Outbound interface executor
│   │   └── base_executor.py              # Base class for executors
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── fsm_api_validator.py          # FSM API validation module
│   │   ├── playwright_automation.py      # Playwright MCP wrapper
│   │   ├── work_unit_monitor.py          # Work unit polling/monitoring
│   │   ├── sftp_manager.py               # SFTP operations
│   │   └── credential_manager.py         # Credential loading/management
│   ├── evidence/
│   │   ├── __init__.py
│   │   ├── evidence_collector.py         # Evidence collection coordinator
│   │   ├── screenshot_manager.py         # Screenshot capture/organization
│   │   └── log_collector.py              # Log aggregation
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── tes070_generator.py           # TES-070 document generation
│   │   └── report_formatter.py           # Evidence formatting
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                     # Structured logging
│       ├── config.py                     # Configuration management
│       └── exceptions.py                 # Custom exceptions
```

### Module Dependencies

```
TestOrchestrator
    ├── BaseExecutor (abstract)
    │   ├── ApprovalExecutor
    │   ├── InboundExecutor
    │   └── OutboundExecutor
    ├── FSMAPIValidator
    ├── PlaywrightAutomation
    ├── WorkUnitMonitor
    ├── SFTPManager
    ├── EvidenceCollector
    ├── CredentialManager
    └── TES070Generator
```

---

## Core Modules

### 1. TestOrchestrator

**Purpose**: Main engine that coordinates test execution

**Responsibilities**:
- Parse JSON test scenarios
- Route to appropriate executor based on interface_type
- Manage test lifecycle (setup/execute/teardown)
- Collect evidence
- Generate TES-070 documents

**Key Methods**:
- `execute()` - Execute all scenarios
- `_get_executor()` - Route to appropriate executor
- `_setup_environment()` - Environment validation
- `_teardown_environment()` - Cleanup
- `_generate_tes070()` - Generate test results document


### 2. BaseExecutor (Abstract)

**Purpose**: Abstract base class for all test executors

**Responsibilities**:
- Provide common functionality for all test types
- Execute individual test steps
- Route actions to appropriate handlers
- Perform validations
- Capture evidence

**Key Methods**:
- `execute_scenario()` - Execute single scenario (abstract)
- `execute_step()` - Execute single test step
- `_handle_sftp_upload()` - SFTP upload handler
- `_handle_ui_action()` - UI interaction handler
- `_handle_api_call()` - API call handler
- `_handle_wait()` - Wait condition handler
- `_validate_step()` - Step validation

### 3. InboundExecutor

**Purpose**: Execute inbound interface tests

**Workflow**:
1. Upload test file to SFTP
2. Wait for File Channel trigger
3. Monitor work unit execution
4. Validate data in FSM via API
5. Collect evidence

**Key Characteristics**:
- Sequential execution (one file at a time)
- File Channel monitoring
- Staging data validation
- Work unit tracking

### 4. ApprovalExecutor

**Purpose**: Execute approval workflow tests

**Workflow**:
1. Trigger approval (release invoice, submit journal)
2. Monitor work unit for User Action creation
3. Navigate to approval UI
4. Submit approval
5. Validate status change via API
6. Collect evidence

**Key Characteristics**:
- User Action monitoring
- Multi-step approval flows
- Status transition validation
- Email notification verification

### 5. OutboundExecutor

**Purpose**: Execute outbound interface tests

**Workflow**:
1. Trigger outbound interface (manual or scheduled)
2. Monitor work unit execution
3. Validate file generation in FSM File Storage
4. Verify file transfer to SFTP
5. Validate file content
6. Collect evidence

**Key Characteristics**:
- File generation validation
- SFTP transfer verification
- File content validation
- Email remittance verification (if applicable)

---

## Integration Modules

### 1. FSM API Validator

**Purpose**: Real-time validation using FSM APIs (NOT Data Lake/Compass)

**Critical Constraint**: Compass queries Data Lake (not real-time). Must use FSM APIs for immediate validation.

**Key Methods**:
- `validate_business_class_data()` - Query and validate FSM data
- `_ensure_token()` - OAuth token management
- `_refresh_token()` - Token refresh logic

**API Pattern**:
```
GET {base_url}/FSM/fsm/soap/classes/{BusinessClass}/lists/_generic
  ?_fields=_all
  &_limit=1000
  &_out=JSON
  &{BusinessClass}.{FilterField}={FilterValue}

Headers:
  Authorization: Bearer {token}
  Accept: application/json
```

**Validation Logic**:
1. Ensure OAuth token is valid (refresh if needed)
2. Build API URL with filters
3. Execute GET request
4. Parse JSON response
5. Validate record count
6. Validate field values (e.g., Status)
7. Return ValidationResult


### 2. Work Unit Monitor

**Purpose**: Poll and validate Process Server work unit execution

**Critical Constraint**: WorkUnit API not exposed. Must use UI automation via Playwright.

**Key Methods**:
- `wait_for_work_unit_creation()` - Poll for work unit creation
- `wait_for_work_unit_completion()` - Poll for work unit completion
- `get_work_unit_status()` - Get current status
- `get_work_unit_details()` - Get work unit details (ID, elapsed time, etc.)

**Polling Strategy**:
1. Navigate to Process Server Administrator > Work Units
2. Search by process name
3. Get most recent work unit
4. Check status (Running, Completed, Failed)
5. Wait poll_interval_seconds
6. Repeat until completion or timeout

**Timeout Handling**:
- Default timeout: 600 seconds (10 minutes)
- Default poll interval: 30 seconds
- Configurable per test step
- Raise TimeoutError if exceeded

### 3. Playwright Automation

**Purpose**: Wrapper for MCP Playwright tools with FSM-specific patterns

**Key Methods**:
- `login()` - Authenticate to FSM
- `navigate_to_work_units()` - Navigate to Work Units page
- `search_work_units()` - Search for work units by process
- `get_work_unit_status()` - Get work unit status
- `navigate_to_business_class()` - Navigate to business class list
- `take_screenshot()` - Capture screenshot with naming convention

**FSM Navigation Patterns**:
1. Always take snapshot before actions
2. Expand sidebar (☰) before navigation
3. Use browser zoom (Ctrl+Minus 3x)
4. Double-click for record details
5. Use Search bar for comprehensive lists

**MCP Tool Usage**:
- `mcp_playwright_browser_navigate` - Navigate to URLs
- `mcp_playwright_browser_snapshot` - Capture page state
- `mcp_playwright_browser_click` - Click elements using refs
- `mcp_playwright_browser_type` - Type text
- `mcp_playwright_browser_take_screenshot` - Capture screenshots

### 4. SFTP Manager

**Purpose**: Handle SFTP file operations

**Key Methods**:
- `upload()` - Upload file to SFTP
- `download()` - Download file from SFTP
- `list_files()` - List files in directory
- `file_exists()` - Check file existence
- `delete_file()` - Delete file (cleanup)

**Credential Management**:
- Read from `Credentials/.env.passwords`
- Parse SFTP credentials (host, username, password, paths)
- Establish secure connection
- Handle connection errors with retry logic

### 5. Credential Manager

**Purpose**: Secure credential loading and management

**Key Methods**:
- `get_fsm_credentials()` - Get FSM login credentials
- `get_ionapi_config()` - Get ION API OAuth credentials
- `get_sftp_credentials()` - Get SFTP credentials

**Security Rules**:
- NEVER commit credential files to git
- NEVER log credentials or tokens
- ALWAYS read from `Credentials/` folder at runtime
- Implement token refresh before expiration

**Credential Files**:
- `Credentials/.env.fsm` - FSM URLs and usernames
- `Credentials/.env.passwords` - Passwords (gitignored)
- `Credentials/{TENANT}.ionapi` - ION API OAuth credentials


---

## Evidence Collection

### Evidence Collector

**Purpose**: Aggregate all test evidence for TES-070 generation

**Evidence Types**:
1. **Screenshots** - UI state at each step
2. **API Responses** - FSM API query results
3. **Work Unit Details** - Work unit ID, status, elapsed time
4. **Logs** - Structured test execution logs
5. **Test Data** - Input files used
6. **Error Messages** - UI error messages, API errors

**Collection Strategy**:
```
For each test step:
  1. Execute action
  2. Capture screenshot (before/after)
  3. Log action details
  4. Perform validation
  5. Capture validation result
  6. Log validation details
  7. Store all evidence with step reference
```

**Evidence Organization**:
```
Projects/{ClientName}/Temp/{interface_id}_{timestamp}/
├── screenshots/
│   ├── 01_file_upload.png
│   ├── 02_work_unit_completed.png
│   └── 03_data_verification.png
├── api_responses/
│   ├── step_3_validation.json
│   └── step_4_status_check.json
├── logs/
│   ├── test_execution.log
│   └── work_unit_637305.log
└── test_data/
    └── GLTRANSREL_valid.csv
```

### Screenshot Manager

**Purpose**: Capture and organize screenshots

**Naming Convention**:
```
{step_number:02d}_{screenshot_name}.png

Examples:
- 01_file_upload.png
- 02_work_unit_completed.png
- 03_data_verification.png
```

**Capture Strategy**:
- Capture at every critical step
- Before and after state changes
- Error messages and validation failures
- Email notifications
- Work unit status
- Final results/output

### Log Collector

**Purpose**: Aggregate structured logs

**Log Levels**:
- DEBUG: Detailed execution information
- INFO: Test progress, step completion
- WARNING: Non-critical issues
- ERROR: Test failures, exceptions

**Log Format**:
```
2026-03-05 10:30:15.123 | INFO | TestOrchestrator | Starting test execution: INT_FIN_013
2026-03-05 10:30:16.456 | INFO | InboundExecutor | Executing scenario: Successful Import
2026-03-05 10:30:17.789 | INFO | SFTPManager | Uploaded GLTRANSREL_valid.csv to /Infor_FSM/GLTransactionInterface/Inbound/
2026-03-05 10:30:18.012 | INFO | WorkUnitMonitor | Waiting for work unit creation (timeout: 600s)
2026-03-05 10:35:20.345 | INFO | WorkUnitMonitor | Work unit created: 637305
2026-03-05 10:35:21.678 | INFO | FSMAPIValidator | Validating GLTransactionInterface records
2026-03-05 10:35:22.901 | INFO | FSMAPIValidator | Validated 10 records with Status=2
2026-03-05 10:35:23.234 | INFO | InboundExecutor | Scenario completed: PASS
```

---

## TES-070 Generation

### TES-070 Generator

**Purpose**: Generate formatted test results documents

**Input**:
- Test scenario JSON
- Test execution results
- Evidence collection (screenshots, logs, API responses)
- Work unit IDs
- Timestamps

**Output**:
- Formatted Word document (.docx)
- Location: `Projects/{ClientName}/TES-070/Generated_TES070s/`
- Filename: `{Client}_TES-070_{InterfaceID}_{InterfaceName}_Test_Results_Document.docx`

**Document Structure**:
1. Title Page
2. Document Control
3. Table of Contents (auto-generated)
4. Test Summary (statistics)
5. Prerequisites
6. Test Scenarios (with embedded screenshots)
7. Appendix (optional)


### Generation Process

```
1. Load test scenario JSON
2. Load test execution results
3. Create Word document from template
4. Populate metadata (title, author, date)
5. Generate test summary table
   - Total tests
   - Passed/Failed counts
   - Pass rate percentage
6. Add prerequisites section
7. For each scenario:
   a. Add scenario title and description
   b. Create test steps table
   c. Embed screenshots in order
   d. Add expected vs actual results
   e. Add pass/fail status
8. Generate table of contents
9. Apply formatting standards (Arial font, colors, spacing)
10. Save to TES-070/Generated_TES070s/
```

### Formatting Standards

**Font**: Arial (NOT Calibri)
- Title: 18pt bold
- Heading 1: 14pt bold, ALL CAPS
- Heading 2: 14pt bold, Title Case
- Body: 11pt
- Table: 10pt

**Colors**:
- Infor Blue: #13A3F7
- Black: #000000
- White: #FFFFFF
- Gray: #F2F2F2

**Tables**:
- Header row: Black background, white text, bold
- Body rows: Alternating white/light gray
- Borders: 1pt solid black

---

## Potential Risks

### 1. Playwright MCP Stability

**Risk**: MCP Playwright server may disconnect or timeout during long test executions

**Mitigation**:
- Implement connection health checks
- Add automatic reconnection logic
- Break long tests into smaller scenarios
- Save state between scenarios

### 2. FSM API Rate Limiting

**Risk**: Excessive API calls may trigger rate limiting

**Mitigation**:
- Implement exponential backoff
- Cache API responses when appropriate
- Batch validation queries
- Monitor API usage

### 3. Work Unit Polling Overhead

**Risk**: Frequent polling may impact FSM performance

**Mitigation**:
- Use reasonable poll intervals (30s default)
- Implement adaptive polling (increase interval over time)
- Set appropriate timeouts
- Consider webhook alternatives if available

### 4. Test Data Isolation

**Risk**: Tests may interfere with each other or leave orphaned data

**Mitigation**:
- Use unique RunGroup identifiers per test execution
- Implement cleanup in teardown phase
- Add data validation before tests
- Use test-specific prefixes (e.g., "AUTOTEST_")

### 5. Screenshot Storage

**Risk**: Large number of screenshots may consume significant disk space

**Mitigation**:
- Compress screenshots
- Archive old test results
- Implement retention policy
- Clean up after TES-070 generation

### 6. Credential Security

**Risk**: Credentials may be exposed in logs or committed to git

**Mitigation**:
- NEVER log credentials or tokens
- Verify .gitignore includes Credentials/
- Use environment variables for CI/CD
- Implement credential rotation

### 7. Browser State Management

**Risk**: Browser state may become inconsistent between tests

**Mitigation**:
- Keep browser open across scenarios (efficiency)
- Implement state validation before each scenario
- Add browser restart capability
- Clear cookies/cache between test suites

### 8. Timeout Tuning

**Risk**: Fixed timeouts may be too short or too long for different environments

**Mitigation**:
- Make timeouts configurable per environment
- Implement adaptive timeouts based on historical data
- Provide timeout override in JSON scenarios
- Log timeout events for analysis


### 9. Error Handling Complexity

**Risk**: Complex error scenarios may not be handled gracefully

**Mitigation**:
- Implement comprehensive exception hierarchy
- Add error recovery strategies
- Log full context on failures
- Provide clear error messages

### 10. Test Execution Time

**Risk**: Long-running tests may timeout or block other work

**Mitigation**:
- Implement parallel execution for independent scenarios
- Optimize wait strategies (polling vs webhooks)
- Break large test suites into smaller batches
- Provide progress indicators

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)

**Goal**: Core framework structure and basic functionality

**Deliverables**:
- Module structure created
- TestOrchestrator implemented
- BaseExecutor abstract class
- CredentialManager module
- StructuredLogger utility
- Basic JSON schema validation

**Success Criteria**:
- Can parse JSON test scenarios
- Can load credentials securely
- Can log test execution

### Phase 2: Integration Modules (Weeks 3-4)

**Goal**: Implement integration layer

**Deliverables**:
- FSMAPIValidator with OAuth token management
- PlaywrightAutomation wrapper for MCP tools
- WorkUnitMonitor with polling logic
- SFTPManager for file operations
- EvidenceCollector coordinator

**Success Criteria**:
- Can authenticate to FSM API
- Can navigate FSM UI via Playwright
- Can monitor work units
- Can upload/download SFTP files
- Can collect evidence

### Phase 3: Executors (Weeks 5-6)

**Goal**: Implement test type-specific executors

**Deliverables**:
- InboundExecutor with File Channel monitoring
- ApprovalExecutor with User Action handling
- OutboundExecutor with file generation validation
- Action handlers (sftp_upload, ui_action, api_call, wait, validate)
- Validation handlers (file_exists, api_query, ui_check, work_unit_status)

**Success Criteria**:
- Can execute inbound interface tests end-to-end
- Can execute approval workflow tests end-to-end
- Can execute outbound interface tests end-to-end

### Phase 4: Evidence & Reporting (Weeks 7-8)

**Goal**: Complete evidence collection and TES-070 generation

**Deliverables**:
- ScreenshotManager with naming conventions
- LogCollector with structured logging
- TES070Generator with formatting standards
- ReportFormatter for evidence organization
- Template integration

**Success Criteria**:
- Can capture screenshots at each step
- Can aggregate logs and API responses
- Can generate formatted TES-070 documents
- Documents match formatting standards

### Phase 5: Testing & Refinement (Weeks 9-10)

**Goal**: Test framework with real scenarios and refine

**Deliverables**:
- Test with existing INT_FIN_013 scenario
- Test with approval workflow scenario
- Test with outbound interface scenario
- Performance optimization
- Error handling improvements
- Documentation updates

**Success Criteria**:
- Successfully execute 3+ different test types
- Generate valid TES-070 documents
- Handle errors gracefully
- Meet performance targets

### Phase 6: Production Readiness (Weeks 11-12)

**Goal**: Prepare for production use

**Deliverables**:
- Comprehensive error handling
- Retry logic and resilience
- Configuration management
- User documentation
- Training materials
- CI/CD integration

**Success Criteria**:
- Framework is stable and reliable
- Documentation is complete
- Team is trained
- Ready for production use


---

## Design Improvements Over Current Framework

### 1. Unified JSON Schema

**Current**: Separate templates for each interface type
**Improved**: Single unified schema with type-specific configurations
**Benefit**: Easier to maintain, consistent structure, extensible

### 2. Modular Executors

**Current**: Monolithic test scripts
**Improved**: Pluggable executors for different test types
**Benefit**: Easy to add new test types, reusable components

### 3. Real-Time Validation

**Current**: No validation or Compass queries (not real-time)
**Improved**: FSM API validation with OAuth token management
**Benefit**: Immediate validation, accurate results

### 4. Work Unit Monitoring

**Current**: Manual checking or fixed waits
**Improved**: Intelligent polling with configurable timeouts
**Benefit**: Faster tests, reliable completion detection

### 5. Evidence Collection

**Current**: Manual screenshot capture
**Improved**: Automated evidence collection with organization
**Benefit**: Complete audit trail, easier TES-070 generation

### 6. Structured Logging

**Current**: Console output only
**Improved**: Structured logs with levels and context
**Benefit**: Easier debugging, audit trail, analysis

### 7. Credential Management

**Current**: Hardcoded or scattered
**Improved**: Centralized, secure credential loading
**Benefit**: Security, maintainability, environment flexibility

### 8. Error Handling

**Current**: Basic try-catch
**Improved**: Comprehensive exception hierarchy with recovery
**Benefit**: Graceful degradation, clear error messages

### 9. Test Isolation

**Current**: Tests may interfere
**Improved**: Unique identifiers, cleanup, validation
**Benefit**: Reliable results, repeatable tests

### 10. Extensibility

**Current**: Hard to add new test types
**Improved**: Plugin architecture with base classes
**Benefit**: Easy to extend, maintainable

---

## Usage Examples

### Example 1: Execute Inbound Interface Test

```bash
# Command line
python ReusableTools/testing_framework/run_tests.py \
  --scenario Projects/SONH/TestScripts/inbound/INT_FIN_013_test_scenarios.json \
  --environment ACUITY_TST

# Python API
from testing_framework.orchestrator import TestOrchestrator

orchestrator = TestOrchestrator(
    scenario_file='Projects/SONH/TestScripts/inbound/INT_FIN_013_test_scenarios.json',
    environment='ACUITY_TST'
)

results = orchestrator.execute()

print(f"Test Results: {results.passed}/{results.total} passed")
```

### Example 2: Execute Approval Workflow Test

```bash
python ReusableTools/testing_framework/run_tests.py \
  --scenario Projects/SONH/TestScripts/approval/APIA_ManualJournal_test_scenarios.json \
  --environment ACUITY_TST
```

### Example 3: Execute Outbound Interface Test

```bash
python ReusableTools/testing_framework/run_tests.py \
  --scenario Projects/SONH/TestScripts/outbound/INT_FIN_127_test_scenarios.json \
  --environment ACUITY_TST
```

---

## Summary

This architecture provides a **robust, extensible framework** for FSM automated testing that:

✅ Supports all RICE object types (approval, inbound, outbound)
✅ Uses real-time FSM API validation (not Data Lake)
✅ Leverages MCP Playwright for UI automation
✅ Monitors work units intelligently
✅ Collects comprehensive evidence
✅ Generates formatted TES-070 documents
✅ Handles errors gracefully
✅ Maintains security best practices
✅ Scales to support multiple clients and interfaces

**Next Steps**:
1. Review and approve architecture
2. Begin Phase 1 implementation
3. Iterate based on feedback
4. Test with real scenarios
5. Deploy to production

---

**Document Version**: 1.0
**Created**: 2026-03-05
**Author**: Kiro AI Assistant
**Status**: Draft - Pending Review
