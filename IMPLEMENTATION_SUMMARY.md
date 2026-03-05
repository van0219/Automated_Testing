# FSM Automation Layer - Implementation Complete

## Overview

The FSM automation layer has been successfully implemented, providing reusable Python modules for automating FSM (Financials & Supply Management) UI interactions via Playwright MCP. This layer enables automated testing of approval workflows, invoice creation, and work unit monitoring.

## Architecture

```
TES-070 Document
    ↓
JSON Test Scenarios
    ↓
run_tests.py (Test Orchestrator)
    ↓
StepEngine (Action Dispatcher)
    ↓
FSM Actions (Login, Payables, WorkUnits)
    ↓
Playwright MCP Client
    ↓
Browser (FSM UI)
    ↓
Evidence (Screenshots, TES-070)
```

## Implemented Components

### 1. Snapshot Parser Utility

**File**: `ReusableTools/testing_framework/utils/snapshot_parser.py`

**Purpose**: Parse Playwright MCP accessibility snapshots to find element references

**Key Functions**:
- `find_element_ref(snapshot, label, role)` - Find element ref by label and role
- `find_all_elements(snapshot, role)` - Find all elements matching role
- `_parse_string_snapshot()` - Parse YAML-format snapshots
- `_traverse_dict_snapshot()` - Parse dictionary-format snapshots
- `_extract_ref_from_line()` - Extract ref attribute from snapshot line

**Snapshot Format Support**:
- String/YAML format: `button "Create Invoice" [ref=abc123]`
- Dictionary format: `{"role": "button", "label": "Create Invoice", "ref": "abc123"}`

### 2. FSM Login Action

**File**: `ReusableTools/testing_framework/actions/fsm/fsm_login.py`

**Purpose**: Automate FSM authentication

**Capabilities**:
- Navigate to FSM portal
- Select authentication method (Cloud Identities, Windows, etc.)
- Enter username and password
- Verify successful login

**Configuration**:
```json
{
  "action": {
    "type": "fsm_login",
    "url": "https://fsm.example.com",
    "username": "user@example.com",
    "password": "{{state.password}}",
    "auth_method": "Cloud Identities"
  }
}
```

### 3. FSM Payables Action

**File**: `ReusableTools/testing_framework/actions/fsm/fsm_payables.py`

**Purpose**: Automate invoice creation and approval submission

**Operations**:
- `navigate_to_payables` - Navigate to Payables application
- `create_invoice` - Create expense invoice with header data
- `submit_for_approval` - Submit invoice for approval workflow

**Capabilities**:
- Fill invoice header fields (company, vendor, invoice number, dates)
- Set approval routing parameters
- Handle optional fields (amount, description)
- Capture screenshots at key steps
- Update test state with invoice number

**Configuration**:
```json
{
  "action": {
    "type": "fsm_payables",
    "operation": "create_invoice",
    "invoice_data": {
      "company": "100",
      "vendor": "V12345",
      "invoice_number": "INV-{{state.run_group}}",
      "invoice_date": "20260305",
      "due_date": "20260405",
      "invoice_amount": "1000.00",
      "description": "Test invoice",
      "routing_category": "APPROVAL_CAT_01"
    }
  }
}
```

### 4. FSM Work Units Action

**File**: `ReusableTools/testing_framework/actions/fsm/fsm_workunits.py`

**Purpose**: Automate work unit monitoring and validation

**Operations**:
- `navigate` - Navigate to Work Units page
- `search` - Search for work units by ID, process name, or title
- `verify_status` - Verify work unit status matches expected
- `wait_for_completion` - Wait for work unit to complete with adaptive polling

**Capabilities**:
- Navigate from any FSM application to Work Units
- Search using multiple criteria
- Extract work unit status from grid
- Adaptive polling (10s → 30s → 60s intervals)
- Capture screenshots for evidence
- Update test state with work unit status

**Configuration**:
```json
{
  "action": {
    "type": "fsm_workunits",
    "operation": "wait_for_completion",
    "work_unit_id": "{{state.work_unit_id}}",
    "timeout": 300,
    "poll_interval": 10
  }
}
```

### 5. UI Map Loader

**File**: `ReusableTools/testing_framework/integration/ui_map_loader.py`

**Purpose**: Load and provide access to UI element labels from JSON maps

**Capabilities**:
- Load UI maps from JSON files
- Cache loaded maps for performance
- Get element labels, types, roles
- Check element properties (has_lookup, required, etc.)

**UI Maps**:
- `fsm_payables_ui_map.json` - Payables screens (search, create invoice)
- `fsm_workunits_ui_map.json` - Work Units screens (search, grid)

### 6. FSM Action Registry

**File**: `ReusableTools/testing_framework/actions/fsm_action_registry.py`

**Purpose**: Register FSM actions with StepEngine

**Function**: `register_fsm_actions(step_engine, playwright_client, ui_map_loader, screenshot_manager, logger)`

**Registered Actions**:
- `fsm_login` → FSMLoginAction
- `fsm_payables` → FSMPayablesAction
- `fsm_workunits` → FSMWorkUnitsAction

## Integration Points

### StepEngine Integration

FSM actions integrate with the existing StepEngine through the action registry:

```python
from ReusableTools.testing_framework.actions.fsm_action_registry import register_fsm_actions

# In run_tests.py or orchestrator
register_fsm_actions(
    step_engine=step_engine,
    playwright_client=playwright_client,
    ui_map_loader=ui_map_loader,
    screenshot_manager=screenshot_manager,
    logger=logger
)
```

### TestState Integration

FSM actions support state variable interpolation:

```json
{
  "invoice_number": "INV-{{state.run_group}}",
  "work_unit_id": "{{state.work_unit_id}}"
}
```

Actions can update state:

```python
return ActionResult(
    status="success",
    message="Invoice created",
    state_updates={"invoice_number": "INV-12345"}
)
```

### Evidence Capture

FSM actions capture screenshots at key steps:

```python
screenshot_path = self.screenshot_manager.capture(
    step_number=1,
    description="invoice_created"
)
```

Evidence points:
1. `invoice_created` - After invoice is saved
2. `approval_submitted` - After submission for approval
3. `work_units_page` - Work Units page loaded
4. `work_unit_status` - Final work unit status

## Snapshot Parsing Strategy

The snapshot parser handles two formats:

### String/YAML Format (Most Common)

```
button "Create Invoice" [ref=abc123]
textbox "Company" [ref=def456]
combobox "Status" [ref=ghi789]
```

Parser extracts:
- Role (button, textbox, combobox)
- Label ("Create Invoice", "Company")
- Ref attribute (abc123, def456)

### Dictionary Format

```json
{
  "role": "button",
  "label": "Create Invoice",
  "ref": "abc123",
  "children": [...]
}
```

Parser traverses recursively to find matching elements.

## Error Handling

All FSM actions implement robust error handling:

1. **Element Not Found**: Raises `ActionError` with descriptive message
2. **Navigation Failures**: Returns `ActionResult` with failure status
3. **Timeout Handling**: Adaptive polling with configurable timeouts
4. **Logging**: Detailed logging at INFO, DEBUG, and ERROR levels

## Usage Example

### Complete Approval Flow Test

```json
{
  "interface_id": "EXT_FIN_004",
  "interface_type": "approval",
  "scenarios": [
    {
      "scenario_id": "S001",
      "title": "Invoice Approval - Manager Approval",
      "steps": [
        {
          "number": 1,
          "description": "Login to FSM",
          "action": {
            "type": "fsm_login",
            "url": "https://fsm.example.com",
            "username": "approver@example.com",
            "password": "{{state.password}}",
            "auth_method": "Cloud Identities"
          }
        },
        {
          "number": 2,
          "description": "Navigate to Payables",
          "action": {
            "type": "fsm_payables",
            "operation": "navigate_to_payables"
          }
        },
        {
          "number": 3,
          "description": "Create expense invoice",
          "action": {
            "type": "fsm_payables",
            "operation": "create_invoice",
            "invoice_data": {
              "company": "100",
              "vendor": "V12345",
              "invoice_number": "INV-{{state.run_group}}",
              "invoice_date": "20260305",
              "due_date": "20260405",
              "invoice_amount": "1000.00",
              "routing_category": "APPROVAL_CAT_01"
            }
          }
        },
        {
          "number": 4,
          "description": "Submit for approval",
          "action": {
            "type": "fsm_payables",
            "operation": "submit_for_approval"
          }
        },
        {
          "number": 5,
          "description": "Navigate to Work Units",
          "action": {
            "type": "fsm_workunits",
            "operation": "navigate"
          }
        },
        {
          "number": 6,
          "description": "Wait for approval workflow completion",
          "action": {
            "type": "fsm_workunits",
            "operation": "wait_for_completion",
            "process_name": "Invoice Approval",
            "timeout": 300
          }
        },
        {
          "number": 7,
          "description": "Verify work unit completed successfully",
          "action": {
            "type": "fsm_workunits",
            "operation": "verify_status",
            "expected_status": "Completed"
          }
        }
      ]
    }
  ]
}
```

## Next Steps

### 1. Framework Integration

Update `run_tests.py` or orchestrator to register FSM actions:

```python
from ReusableTools.testing_framework.actions.fsm_action_registry import register_fsm_actions

# After initializing step_engine
register_fsm_actions(
    step_engine=step_engine,
    playwright_client=playwright_client,
    ui_map_loader=ui_map_loader,
    screenshot_manager=screenshot_manager,
    logger=logger
)
```

### 2. Testing with Real FSM Environment

Test FSM actions with actual FSM environment:

```bash
python run_tests.py \
  --scenario Projects/SONH/TestScripts/approval/EXT_FIN_004_test_scenarios.json \
  --client SONH \
  --environment ACUITY_TST \
  --verbose
```

### 3. Validation and Refinement

- Validate snapshot parsing with real FSM snapshots
- Refine element discovery logic based on actual snapshot structure
- Add error handling for edge cases
- Optimize polling intervals based on real work unit completion times

### 4. Additional FSM Actions

Consider implementing additional actions:

- **FSM General Ledger**: GL transaction entry and validation
- **FSM Accounts Receivable**: Customer invoice management
- **FSM User Actions**: Approval action handling
- **FSM Reports**: Report generation and validation

### 5. Enhanced Grid Parsing

Implement robust grid parsing for Work Units:

- Parse grid structure from snapshot
- Extract column values by row
- Support pagination
- Handle sorting and filtering

## Benefits

1. **Reusability**: FSM actions work across all client projects
2. **Maintainability**: UI maps separate element labels from logic
3. **Testability**: Actions return structured results for validation
4. **Evidence**: Automatic screenshot capture at key steps
5. **Flexibility**: State variable interpolation for dynamic data
6. **Robustness**: Comprehensive error handling and logging

## Files Modified/Created

### Created Files
- `ReusableTools/testing_framework/utils/snapshot_parser.py`
- `ReusableTools/testing_framework/actions/fsm/__init__.py`
- `ReusableTools/testing_framework/actions/fsm/fsm_login.py`
- `ReusableTools/testing_framework/actions/fsm/fsm_payables.py`
- `ReusableTools/testing_framework/actions/fsm/fsm_workunits.py`
- `ReusableTools/testing_framework/actions/fsm/README.md`
- `ReusableTools/testing_framework/actions/fsm_action_registry.py`
- `ReusableTools/testing_framework/integration/ui_map_loader.py`

### Existing Files (Reference)
- `ReusableTools/testing_framework/ui_maps/fsm_payables_ui_map.json`
- `ReusableTools/testing_framework/ui_maps/fsm_workunits_ui_map.json`
- `ReusableTools/testing_framework/integration/playwright_client.py`
- `ReusableTools/testing_framework/engine/step_engine.py`
- `ReusableTools/testing_framework/actions/base.py`

## Documentation

Complete documentation available in:
- `ReusableTools/testing_framework/actions/fsm/README.md` - FSM actions usage guide
- `Projects/SONH/Temp/ui_discovery/UI_DISCOVERY_SUMMARY.md` - UI discovery results
- `docs/FSM_TESTING_FRAMEWORK_ARCHITECTURE_V2.md` - Framework architecture
- `docs/TESTING_FRAMEWORK_V2_QUICK_REFERENCE.md` - Quick reference guide

---

**Status**: Implementation complete, ready for integration testing with real FSM environment.

**Date**: March 5, 2026
