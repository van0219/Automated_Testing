# FSM Automation Layer Validation Tests

## Overview

These validation tests verify that the FSM automation layer works correctly before running full approval workflow tests.

## Test Sequence

### TEST 1: FSM Login Validation
**File**: `test_01_fsm_login.py`

**Goal**: Verify Playwright MCP functions and FSM login automation work

**What it tests**:
- Playwright MCP browser navigation
- Page load waiting
- Snapshot capture
- Screenshot capture
- Browser close

**Expected output**:
- `Projects/SONH/Temp/evidence/login_test/01_login_page_snapshot_*.txt`
- `Projects/SONH/Temp/evidence/login_test/01_login_page_*.png`

**Success criteria**:
- ✓ Browser navigates to FSM login page
- ✓ Snapshot is captured and saved
- ✓ Screenshot is captured and saved
- ✓ "Cloud Identities" button is found in snapshot
- ✓ Browser closes without errors

---

### TEST 2: Payables Navigation Validation
**File**: `test_02_payables_navigation.py`

**Goal**: Verify that UI discovery labels and snapshot parsing work

**What it tests**:
- Snapshot parser functionality
- Element reference discovery
- Snapshot format analysis
- Button pattern detection

**Expected output**:
- `Projects/SONH/Temp/evidence/payables_navigation_test/01_login_page_*.png`
- `Projects/SONH/Temp/evidence/payables_navigation_test/02_current_page_snapshot_*.txt`
- `Projects/SONH/Temp/evidence/payables_navigation_test/03_final_state_*.png`

**Success criteria**:
- ✓ Snapshot parser finds element refs
- ✓ Button patterns are detected
- ✓ Snapshot format is understood
- ✓ Element discovery works

---

### TEST 3: Create Invoice Screen Validation
**File**: `test_03_create_invoice_button.py`

**Goal**: Verify that the Create Invoice button can be located and clicked

**What it tests**:
- Complete button discovery workflow
- Multiple button detection
- Partial matching
- Full page snapshots

**Expected output**:
- `Projects/SONH/Temp/evidence/create_invoice_test/01_initial_page_*.png`
- `Projects/SONH/Temp/evidence/create_invoice_test/02_page_snapshot_*.txt`
- `Projects/SONH/Temp/evidence/create_invoice_test/03_final_state_*.png`

**Success criteria**:
- ✓ All buttons on page are discovered
- ✓ "Create Invoice" button is found
- ✓ Common buttons (Search, Refresh) are found
- ✓ Snapshot parser works reliably

---

## Running the Tests

### Prerequisites

1. Playwright MCP server must be running
2. FSM credentials must be configured in `Projects/SONH/Credentials/`
3. Python environment with required packages

### Execution

Run tests in sequence:

```bash
# TEST 1: Login validation
python ReusableTools/validation_tests/test_01_fsm_login.py

# TEST 2: Payables navigation (after TEST 1 passes)
python ReusableTools/validation_tests/test_02_payables_navigation.py

# TEST 3: Create Invoice button (after TEST 2 passes)
python ReusableTools/validation_tests/test_03_create_invoice_button.py
```

### Expected Behavior

Each test will:
1. Print progress messages to console
2. Save snapshots and screenshots to evidence directory
3. Display validation results
4. Return exit code 0 on success, 1 on failure

## Troubleshooting

### Common Issues

**Issue**: `name 'mcp_playwright_browser_navigate' is not defined`
- **Cause**: Playwright MCP functions not available in Python scope
- **Solution**: These functions are provided by Kiro's environment. Run tests through Kiro, not standalone Python.

**Issue**: Snapshot parser returns None
- **Cause**: Snapshot format doesn't match expected pattern
- **Solution**: Review snapshot file to understand actual format, update parser if needed

**Issue**: Browser doesn't close
- **Cause**: Error occurred before close statement
- **Solution**: Tests include try/except to close browser on error

## Validation Checklist

After running all three tests, verify:

- [ ] TEST 1: Login page loads and snapshot is captured
- [ ] TEST 1: "Cloud Identities" button is found in snapshot
- [ ] TEST 2: Snapshot parser successfully finds element refs
- [ ] TEST 2: Button patterns are detected correctly
- [ ] TEST 3: All buttons on page are discovered
- [ ] TEST 3: "Create Invoice" button is found
- [ ] All screenshots are clear and show expected pages
- [ ] All snapshots are saved and readable

## Next Steps

### If All Tests Pass ✓

The FSM automation layer is validated and ready for:
1. Full approval workflow testing
2. Invoice creation automation
3. Work unit monitoring
4. Complete end-to-end scenarios

### If Tests Fail ✗

1. Review error messages and stack traces
2. Examine snapshot files to understand format
3. Update snapshot parser if needed
4. Fix Playwright MCP integration issues
5. Re-run failed tests

## Important Notes

- **Do not run approval workflows yet** - These are validation tests only
- **Do not create invoices** - We're only testing navigation and discovery
- **Do not submit approvals** - Focus is on browser automation validation
- Tests are designed to be safe and non-destructive
- Each test is independent and can be run separately
- Evidence is saved for manual review and debugging

## Evidence Review

After running tests, review evidence files:

1. **Snapshots** (*.txt files):
   - Check format (YAML vs dict)
   - Verify element refs are present
   - Look for button patterns
   - Understand structure

2. **Screenshots** (*.png files):
   - Verify page loaded correctly
   - Check if UI elements are visible
   - Confirm browser zoom level
   - Validate image quality

## Success Criteria Summary

All three tests must pass before proceeding to full approval workflow automation:

1. ✓ Playwright MCP functions work
2. ✓ Snapshot capture works
3. ✓ Snapshot parser finds elements
4. ✓ Button discovery works
5. ✓ Screenshots are captured
6. ✓ Browser automation is stable

---

**Last Updated**: March 5, 2026
**Status**: Ready for validation
