# FSM Automation Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Test Scenario (JSON)                      │
│  - Interface metadata                                            │
│  - Test scenarios with steps                                     │
│  - Action configurations                                         │
│  - State variable interpolation: {{state.variable}}             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      run_tests.py (CLI)                          │
│  - Parse command line arguments                                  │
│  - Load credentials from Projects/{Client}/Credentials/          │
│  - Initialize framework components                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TestOrchestrator                              │
│  - Coordinate test execution                                     │
│  - Manage test state                                             │
│  - Generate TES-070 documents                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       StepEngine                                 │
│  - Dispatch actions based on type                                │
│  - Interpolate state variables                                   │
│  - Collect action results                                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ FSMLogin    │  │ FSMPayables │  │ FSMWorkUnits│
│  Action     │  │   Action    │  │   Action    │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │      UIMapLoader              │
        │  - Load element labels        │
        │  - Cache UI maps              │
        │  - Provide element properties │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   PlaywrightMCPClient         │
        │  - Navigate to URLs           │
        │  - Take snapshots             │
        │  - Click elements             │
        │  - Type text                  │
        │  - Capture screenshots        │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │    SnapshotParser             │
        │  - Parse YAML snapshots       │
        │  - Find element refs          │
        │  - Extract element properties │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │  Playwright MCP Server        │
        │  - Browser automation         │
        │  - Accessibility snapshots    │
        │  - Element interactions       │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │      Browser (FSM UI)         │
        │  - Payables application       │
        │  - Work Units page            │
        │  - Process Server Admin       │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   ScreenshotManager           │
        │  - Capture screenshots        │
        │  - Save to Temp/ directory    │
        │  - Organize by step number    │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │    TES070Generator            │
        │  - Generate Word documents    │
        │  - Embed screenshots          │
        │  - Format test results        │
        └───────────────────────────────┘
```

## Data Flow

### 1. Test Scenario Loading

```
JSON File → TestOrchestrator → Parse scenarios → Initialize TestState
```

### 2. Action Execution

```
Step Config → StepEngine → Interpolate {{state.vars}} → Dispatch to Action
```

### 3. FSM Interaction

```
Action → UIMapLoader (get labels) → PlaywrightMCP (snapshot) → 
SnapshotParser (find refs) → PlaywrightMCP (click/type) → Browser
```

### 4. Evidence Collection

```
Action → ScreenshotManager → Capture PNG → Save to Temp/ → 
Update TestState → TES070Generator
```

## State Management

```
TestState (Dictionary)
├── run_group: "AUTOTEST_20260305103045_A7B9C2"
├── work_unit_id: "12345"
├── invoice_number: "INV-AUTOTEST_20260305103045_A7B9C2"
├── work_unit_status: "Completed"
└── [custom variables from actions]
```

State variables are interpolated in action configs:
- `{{state.run_group}}` → Unique test identifier
- `{{state.work_unit_id}}` → Work unit ID from previous step
- `{{state.invoice_number}}` → Invoice number from creation step

## Snapshot Parsing Flow

```
1. PlaywrightMCP.snapshot() → Returns snapshot data
                              ↓
2. SnapshotParser.find_element_ref(snapshot, "Create Invoice", "button")
                              ↓
3. Parse snapshot format (YAML or Dict)
                              ↓
4. Search for matching label and role
                              ↓
5. Extract ref attribute → "abc123"
                              ↓
6. Return ref to action
                              ↓
7. PlaywrightMCP.click(ref="abc123", element="Create Invoice")
```

## UI Map Structure

```json
{
  "screen_name": {
    "elements": {
      "element_name": {
        "label": "Display Label",
        "type": "button|textbox|combobox",
        "role": "button|textbox|combobox",
        "required": true|false,
        "has_lookup": true|false
      }
    }
  }
}
```

## Action Result Flow

```
Action.execute() → ActionResult
                      ↓
                   status: "success"|"failure"
                   message: "Description"
                   data: {...}
                   state_updates: {"key": "value"}
                      ↓
                   StepEngine
                      ↓
                   Update TestState
                      ↓
                   Continue to next step
```

## Error Handling

```
Action encounters error
    ↓
Log error with logger.error()
    ↓
Return ActionResult(status="failure", message="Error details")
    ↓
StepEngine marks step as failed
    ↓
TestOrchestrator decides: continue or abort
    ↓
Generate TES-070 with failure evidence
```

## Integration Points

### 1. StepEngine Registration

```python
from ReusableTools.testing_framework.actions.fsm_action_registry import register_fsm_actions

register_fsm_actions(
    step_engine=step_engine,
    playwright_client=playwright_client,
    ui_map_loader=ui_map_loader,
    screenshot_manager=screenshot_manager,
    logger=logger
)
```

### 2. Action Configuration

```json
{
  "action": {
    "type": "fsm_payables",
    "operation": "create_invoice",
    "invoice_data": {
      "company": "100",
      "vendor": "V12345",
      "invoice_number": "INV-{{state.run_group}}"
    }
  }
}
```

### 3. State Updates

```python
return ActionResult(
    status="success",
    state_updates={"invoice_number": "INV-12345"}
)
```

## File Organization

```
ReusableTools/testing_framework/
├── actions/
│   ├── fsm/
│   │   ├── __init__.py
│   │   ├── fsm_login.py          # FSM authentication
│   │   ├── fsm_payables.py       # Invoice creation/approval
│   │   ├── fsm_workunits.py      # Work unit monitoring
│   │   └── README.md             # FSM actions documentation
│   ├── fsm_action_registry.py    # Registration system
│   └── base.py                   # BaseAction class
├── integration/
│   ├── playwright_client.py      # Playwright MCP wrapper
│   └── ui_map_loader.py          # UI map loader
├── utils/
│   └── snapshot_parser.py        # Snapshot parsing utilities
├── ui_maps/
│   ├── fsm_payables_ui_map.json  # Payables UI elements
│   └── fsm_workunits_ui_map.json # Work Units UI elements
└── evidence/
    ├── screenshot_manager.py     # Screenshot capture
    └── tes070_generator.py       # TES-070 generation
```

## Execution Flow Example

### Approval Flow Test

```
1. Load JSON scenario
   ↓
2. Initialize TestState with run_group
   ↓
3. Step 1: FSMLoginAction
   - Navigate to FSM
   - Find auth method button
   - Enter credentials
   - Verify login
   ↓
4. Step 2: FSMPayablesAction (navigate)
   - Find Payables link
   - Click and wait
   ↓
5. Step 3: FSMPayablesAction (create_invoice)
   - Click Create Invoice
   - Fill header fields
   - Set routing
   - Save invoice
   - Capture screenshot
   - Update state: invoice_number
   ↓
6. Step 4: FSMPayablesAction (submit_for_approval)
   - Find Submit button
   - Click and wait
   - Capture screenshot
   ↓
7. Step 5: FSMWorkUnitsAction (navigate)
   - Switch to PSA
   - Navigate to Work Units
   - Capture screenshot
   ↓
8. Step 6: FSMWorkUnitsAction (wait_for_completion)
   - Search for work unit
   - Poll status every 10s
   - Wait for Completed/Failed
   - Update state: work_unit_status
   ↓
9. Step 7: FSMWorkUnitsAction (verify_status)
   - Extract status from grid
   - Compare with expected
   - Capture screenshot
   ↓
10. Generate TES-070 document
    - Embed all screenshots
    - Format test results
    - Save to TES-070/Generated_TES070s/
```

---

**Architecture Status**: Complete and ready for integration testing
**Date**: March 5, 2026
