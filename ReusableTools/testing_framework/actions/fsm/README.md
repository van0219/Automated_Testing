# FSM Automation Actions

This directory contains reusable automation functions for FSM (Financials & Supply Management) using Playwright MCP.

## Architecture

```
TES-070 Document
    ↓
AI extracts scenarios
    ↓
JSON test scenario
    ↓
run_tests.py
    ↓
StepEngine
    ↓
FSM Action Handlers (this module)
    ↓
Playwright MCP Client
    ↓
Browser automation
    ↓
Evidence + TES-070 report
```

## Modules

### `fsm_login.py`

Handles FSM authentication and login.

**Operations**:
- Navigate to FSM portal
- Select authentication method (Cloud Identities)
- Enter credentials
- Verify login success

**Example JSON**:
```json
{
  "action": {
    "type": "fsm_login",
    "url": "https://mingle-portal.inforcloudsuite.com/...",
    "username": "user@example.com",
    "password": "{{state.password}}",
    "auth_method": "Cloud Identities"
  }
}
```

### `fsm_payables.py`

Handles Payables module automation.

**Operations**:
- `navigate_to_payables`: Navigate to Payables application
- `create_invoice`: Create expense invoice
- `submit_for_approval`: Submit invoice for approval

**Example JSON**:
```json
{
  "action": {
    "type": "fsm_payables",
    "operation": "create_invoice",
    "invoice_data": {
      "company": "10",
      "vendor": "176258",
      "invoice_number": "AUTO_TEST_001",
      "invoice_date": "2026-03-05",
      "due_date": "2026-03-12",
      "invoice_amount": "500.00",
      "description": "Test invoice for approval workflow",
      "routing_category": "GHR"
    }
  }
}
```

### `fsm_workunits.py`

Handles Work Units monitoring and verification.

**Operations**:
- `navigate`: Navigate to Work Units page
- `search`: Search for work unit by process name or ID
- `verify_status`: Verify work unit status
- `wait_for_completion`: Wait for work unit to complete with adaptive polling

**Example JSON**:
```json
{
  "action": {
    "type": "fsm_workunits",
    "operation": "wait_for_completion",
    "work_unit_id": "{{state.work_unit_id}}",
    "timeout": 120,
    "poll_interval": 10
  }
}
```

## UI Maps

FSM actions use UI maps to discover element labels and properties:

- `fsm_payables_ui_map.json`: Payables screens (search, create invoice)
- `fsm_workunits_ui_map.json`: Work Units page

UI maps are loaded via `UIMapLoader` and provide:
- Element labels for automation
- Element types (button, textbox, combobox)
- Element roles for Playwright selectors
- Field properties (required, has_lookup, has_datepicker)

## Integration with Testing Framework

### Registration

FSM actions are registered with `StepEngine` via `fsm_action_registry.py`:

```python
from ReusableTools.testing_framework.actions.fsm_action_registry import register_fsm_actions

# In test orchestrator setup
register_fsm_actions(
    step_engine=step_engine,
    playwright_client=playwright_client,
    ui_map_loader=ui_map_loader,
    screenshot_manager=screenshot_manager,
    logger=logger
)
```

### State Management

FSM actions integrate with `TestState` for variable interpolation:

**State Variables**:
- `run_group`: Unique test identifier (e.g., AUTOTEST_20260305_A7B9C2)
- `invoice_number`: Created invoice number
- `work_unit_id`: Work unit ID from IPA execution
- `work_unit_status`: Current work unit status

**Example**:
```json
{
  "action": {
    "type": "fsm_payables",
    "operation": "create_invoice",
    "invoice_data": {
      "invoice_number": "{{state.run_group}}_TEST_001"
    }
  }
}
```

### Evidence Capture

Screenshots are automatically captured at key steps:

1. **Invoice Created**: After saving invoice
2. **Approval Submitted**: After submitting for approval
3. **Work Unit Page**: When navigating to Work Units
4. **Work Unit Status**: When verifying status

Screenshots are managed by `ScreenshotManager` and saved to:
```
Projects/{ClientName}/Temp/evidence/{scenario_id}/
```

## Complete Approval Workflow Example

```json
{
  "interface_id": "EXT_FIN_004",
  "interface_type": "approval",
  "scenarios": [
    {
      "scenario_id": "3.1",
      "title": "Garnishment invoice auto approved",
      "steps": [
        {
          "number": 1,
          "description": "Login to FSM",
          "action": {
            "type": "fsm_login",
            "url": "{{state.fsm_url}}",
            "username": "{{state.fsm_username}}",
            "password": "{{state.fsm_password}}"
          }
        },
        {
          "number": 2,
          "description": "Create expense invoice",
          "action": {
            "type": "fsm_payables",
            "operation": "create_invoice",
            "invoice_data": {
              "company": "10",
              "vendor": "176258",
              "invoice_number": "{{state.run_group}}_3.1",
              "invoice_date": "2026-03-05",
              "due_date": "2026-03-12",
              "invoice_amount": "500.00",
              "description": "Garnishment invoice for auto approval test"
            }
          },
          "screenshot": "invoice_created"
        },
        {
          "number": 3,
          "description": "Submit invoice for approval",
          "action": {
            "type": "fsm_payables",
            "operation": "submit_for_approval"
          },
          "screenshot": "approval_submitted"
        },
        {
          "number": 4,
          "description": "Navigate to Work Units",
          "action": {
            "type": "fsm_workunits",
            "operation": "navigate"
          },
          "screenshot": "work_units_page"
        },
        {
          "number": 5,
          "description": "Wait for work unit completion",
          "action": {
            "type": "fsm_workunits",
            "operation": "wait_for_completion",
            "timeout": 120
          }
        },
        {
          "number": 6,
          "description": "Verify work unit status",
          "action": {
            "type": "fsm_workunits",
            "operation": "verify_status",
            "expected_status": "Completed"
          },
          "screenshot": "work_unit_final_status",
          "validation": {
            "type": "workunit",
            "expected_status": "Completed"
          }
        }
      ]
    }
  ]
}
```

## Implementation Status

### ✅ Completed

- Module structure created
- Base action classes implemented
- UI map loader implemented
- Action registration system implemented
- Integration with StepEngine prepared
- Evidence capture integration prepared

### 🚧 TODO (Snapshot Parsing)

The current implementation includes placeholder comments for snapshot parsing.
The actual implementation needs to:

1. **Parse Playwright MCP snapshots** to find element references
2. **Search snapshot tree** for elements by label and role
3. **Extract element refs** for click and type operations

**Example snapshot parsing function**:
```python
def _find_element_ref(snapshot: Dict[str, Any], label: str, role: str = None) -> Optional[str]:
    """
    Find element reference in snapshot by label and role.
    
    Args:
        snapshot: Snapshot data from Playwright MCP
        label: Element label to search for
        role: Optional element role to filter by
    
    Returns:
        Element reference string or None if not found
    """
    # TODO: Implement recursive snapshot tree traversal
    # Search for elements matching label and role
    # Return the 'ref' attribute when found
    pass
```

This parsing logic should be implemented in a separate utility module:
```
ReusableTools/testing_framework/utils/snapshot_parser.py
```

## Testing

To test FSM actions without running full scenarios:

```python
from ReusableTools.testing_framework.integration.playwright_client import PlaywrightMCPClient
from ReusableTools.testing_framework.integration.ui_map_loader import UIMapLoader
from ReusableTools.testing_framework.evidence.screenshot_manager import ScreenshotManager
from ReusableTools.testing_framework.actions.fsm_action_registry import create_fsm_action_handlers
from ReusableTools.testing_framework.engine.test_state import TestState

# Setup
playwright = PlaywrightMCPClient()
playwright.connect()

ui_map_loader = UIMapLoader()
screenshot_manager = ScreenshotManager(evidence_dir="test_evidence")
state = TestState()

# Create handlers
handlers = create_fsm_action_handlers(
    playwright_client=playwright,
    ui_map_loader=ui_map_loader,
    screenshot_manager=screenshot_manager
)

# Test login
login_config = {
    "url": "https://...",
    "username": "user@example.com",
    "password": "password"
}
result = handlers['fsm_login'].execute(login_config, state)
print(result.status, result.message)

# Cleanup
playwright.close()
```

## Next Steps

1. **Implement snapshot parsing utility** for element discovery
2. **Test FSM actions** with real FSM environment
3. **Refine element selectors** based on actual snapshot structure
4. **Add error handling** for common failure scenarios
5. **Extend operations** as needed for additional workflows

## Notes

- FSM actions use **Playwright MCP** (not traditional Playwright API)
- All browser operations go through `PlaywrightMCPClient`
- Element discovery uses **accessibility snapshots** (not DOM selectors)
- Screenshots are captured automatically at configured steps
- State variables enable dynamic test data (run_group, invoice_number, etc.)
