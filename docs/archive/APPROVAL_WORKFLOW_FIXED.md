# Approval Regression Testing Workflow - FIXED

## Overview

The approval regression testing workflow has been completely redesigned to work correctly with MCP Playwright and subagents.

## Fixed Components

### 1. Hook: `run-approval-regression-tests.kiro.hook`
**Location**: `.kiro/hooks/run-approval-regression-tests.kiro.hook`

**What it does**:
1. Asks user to select client and TES-070 document
2. Prompts for FSM credentials
3. Parses TES-070 using `tes070_analyzer.py` (creates `*_analysis.json`)
4. Detects transaction type (ExpenseInvoice, ManualJournal, CashLedgerTransaction)
5. Validates appropriate subagent exists
6. Creates test instructions JSON using `create_test_instructions.py`
7. Invokes the specialized subagent with test instructions

### 2. Script: `create_test_instructions.py`
**Location**: `ReusableTools/create_test_instructions.py`

**What it does**:
- Reads `*_analysis.json` from TES-070 analyzer
- Extracts scenarios that have `test_steps` (skips TOC entries)
- Creates simplified JSON with:
  - scenario_id
  - title
  - description
  - test_steps (number, description, result)
  - expected_results
- Saves to `Projects/{Client}/TestScripts/approval/{extension_id}_test_instructions.json`

### 3. Subagent: `invoice-approval-test-agent.md`
**Location**: `.kiro/agents/invoice-approval-test-agent.md`

**What it does**:
- Reads test instructions JSON
- For each scenario:
  - Reads test_steps
  - Interprets step descriptions (e.g., "Go to Payables", "Create Invoice")
  - Executes using MCP Playwright tools:
    - `mcp_playwright_browser_snapshot()` - BEFORE every action
    - `mcp_playwright_browser_click()` - Using refs from snapshot
    - `mcp_playwright_browser_type()` - Type into fields
    - `mcp_playwright_browser_fill_form()` - Fill multiple fields
    - `mcp_playwright_browser_take_screenshot()` - Capture evidence
  - Saves screenshots to `Projects/{Client}/Temp/evidence/`
- Reports pass/fail results

## Workflow Diagram

```
User triggers hook
    ↓
Hook asks: Which client? Which TES-070?
    ↓
Hook prompts: FSM credentials
    ↓
Hook runs: tes070_analyzer.py → creates *_analysis.json
    ↓
Hook detects: Transaction type (ExpenseInvoice)
    ↓
Hook validates: invoice-approval-test-agent exists
    ↓
Hook runs: create_test_instructions.py → creates *_test_instructions.json
    ↓
Hook invokes: invoice-approval-test-agent with JSON path + credentials
    ↓
Subagent reads: test_instructions.json
    ↓
Subagent executes: Each scenario using MCP Playwright
    ↓
Subagent reports: Pass/fail results + screenshot locations
```

## Key Differences from Before

### BEFORE (WRONG):
- Hook tried to create "executable scenarios" with predefined MCP actions
- Subagent expected fully-formed MCP commands in JSON
- Too rigid, didn't work

### AFTER (CORRECT):
- Hook creates simple test instructions with test_steps from TES-070
- Subagent reads test_steps and INTERPRETS them
- Subagent is AUTONOMOUS - makes decisions based on snapshots
- Flexible, works with any TES-070 format

## Test Instructions JSON Format

```json
{
  "extension_id": "EXT_FIN_004",
  "extension_name": "Expense Invoice Approval",
  "client": "SONH",
  "total_scenarios": 3,
  "scenarios": [
    {
      "scenario_id": "3.1",
      "title": "Requester submits garnishment expense invoice for approval – auto approved",
      "description": "Requester initiates expense invoice with vendor class = GHR...",
      "test_steps": [
        {
          "number": "1",
          "description": "Go to Payables > Vendors. Select Vendor with Vendor Class = GHR. Create an Expense Invoice...",
          "result": "PASS"
        },
        {
          "number": "2",
          "description": "Invoice Status is Released.",
          "result": "PASS"
        }
      ],
      "expected_results": [
        "Invoice auto-approved without routing to approvers",
        "Work unit status: Completed"
      ]
    }
  ]
}
```

## How Subagent Interprets Test Steps

The subagent reads the `description` field and interprets it:

**Example 1**: "Go to Payables > Vendors"
```
1. Take snapshot
2. Find "Payables" menu ref
3. Click it
4. Take snapshot
5. Find "Vendors" submenu ref
6. Click it
```

**Example 2**: "Create an Expense Invoice using the selected vendor"
```
1. Take snapshot
2. Find "Create Invoice" button ref
3. Click it
4. Take snapshot to see form
5. Fill form fields
6. Click Save
```

**Example 3**: "Submit for Approval"
```
1. Take snapshot
2. Find "Submit for Approval" button ref
3. Click it
4. Handle confirmation dialog
5. Take snapshot to verify status
```

## Critical Rules for Subagent

1. **ALWAYS snapshot before action** - See current page state
2. **Use refs from snapshot** - Don't guess selectors
3. **Interpret test steps** - Read description, decide what to do
4. **Be autonomous** - Make decisions based on what you see
5. **Capture screenshots** - After each critical action
6. **Document results** - Pass/fail for each scenario

## Usage

### Trigger the Hook
1. Click "Run FSM Approval Regression Tests" hook
2. Select client (e.g., SONH)
3. Select TES-070 document
4. Enter FSM credentials
5. Wait for subagent to execute tests
6. Review results

### Files Created
- `Projects/{Client}/TestScripts/approval/{extension_id}_test_instructions.json` - Test instructions
- `Projects/{Client}/Temp/evidence/scenario_*.png` - Screenshots
- `Projects/{Client}/Credentials/.env.fsm` - FSM credentials
- `Projects/{Client}/Credentials/.env.passwords` - Passwords

## Next Steps

1. Test the workflow with EXT_FIN_004
2. Create additional subagents for other transaction types:
   - `journal-approval-test-agent` for ManualJournal
   - `cash-approval-test-agent` for CashLedgerTransaction
3. Enhance subagent with more test step patterns
4. Add TES-070 report generation

## Status

✅ Hook fixed
✅ Script created (`create_test_instructions.py`)
✅ Subagent rewritten
✅ Workflow documented
✅ Ready for testing
