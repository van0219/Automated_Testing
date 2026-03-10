# Test Execution Workflow

Guide for executing FSM approval test scenarios using browser automation.

## Overview

Execute test scenarios from test instructions JSON using MCP Playwright tools for browser automation.

## Prerequisites

- Test instructions JSON created (from `create_test_instructions.py`)
- FSM credentials configured in `Projects/{Client}/Credentials/`
- MCP Playwright tools available (built into Kiro)
- Browser automation capability

**IMPORTANT**: This workflow executes tests for ANY approval TES-070 document. The test execution adapts to different:
- Client projects (SONH, ClientB, ClientC, etc.)
- Approval types (ExpenseInvoice, ManualJournal, CashLedgerTransaction, etc.)
- Test scenarios (auto-approval, manual approval, rejection, etc.)
- Business rules (vendor class, authority code, amount thresholds, etc.)

## Testing Modes

This workflow supports TWO distinct testing modes:

### Mode 1: Regression Testing (EXACT ADHERENCE)

**When**: Testing with existing TES-070 documents that have detailed test steps

**Rule**: Follow TES-070 steps EXACTLY as written - no interpretation, no deviation

**Characteristics**:
- Detailed TES-070 document exists
- Each step has specific navigation, values, expected results
- Document shows previous "PASS" results
- Purpose: Verify existing functionality still works

### Mode 2: Net New Testing (ADAPTIVE EXECUTION)

**When**: Testing new functionality with generic test scripts from functional consultants

**Rule**: Use your knowledge and instincts to execute tests based on generic test script

**Characteristics**:
- Generic test script or scenario description
- High-level objectives without detailed steps
- No previous TES-070 document
- Purpose: Test new functionality or create initial documentation

**Example - Net New:**
```
Scenario: Test manual journal approval for amounts under $1,000
Expected: Journal should route to Agency approver
```

Your approach:
- Determine appropriate role and navigation
- Create journal with reasonable values
- Submit and monitor approval
- Document your approach

**When in doubt**: Ask user which mode or check if TES-070 document exists.

---

## Workflow Steps (Mode 1: Regression Testing)

The following workflow applies to REGRESSION TESTING with existing TES-070 documents.

### Step 1: Load Client Metadata and Test Instructions

**CRITICAL: Load Client Metadata First**

Before loading test instructions, read client metadata from project README:

```python
from ReusableTools.read_client_metadata import get_client_metadata

metadata = get_client_metadata("SONH")
client_code = metadata['client_code']        # "SONH" (for folder paths)
client_name = metadata['client_name']        # "State of New Hampshire" (for TES-070 display)
tenant_id = metadata['tenant_id']            # "NMR2N66J9P445R7P_AX4"
```

**Why This Matters:**
- `client_code` is used for folder paths (e.g., `Projects/SONH/`)
- `client_name` is used for TES-070 document display (e.g., "State of New Hampshire")
- Prevents folder creation issues (e.g., creating `Projects/State of New Hampshire/` instead of `Projects/SONH/`)
- Ensures test results JSON has correct metadata for TES-070 generation

Read test instructions JSON:

```bash
Projects/{client_code}/TestScripts/approval/{extension_id}_test_instructions.json
```

**JSON Structure:**
```json
{
  "extension_id": "EXT_FIN_004",
  "transaction_type": "ExpenseInvoice",
  "client": "SONH",
  "scenarios": [
    {
      "scenario_id": "3.1",
      "title": "Scenario title",
      "description": "Scenario description",
      "test_steps": [
        "Step 1 description",
        "Step 2 description"
      ],
      "expected_results": [
        "Expected result 1",
        "Expected result 2"
      ]
    }
  ]
}
```

### Step 2: Load FSM Credentials

Read credentials from files:

**`.env.fsm`:**
```
FSM_PORTAL_URL=https://mingle-portal.inforcloudsuite.com/v2/...
FSM_USERNAME=user@example.com
ENVIRONMENT=Other
```

**`.env.passwords`:**
```
FSM_PASSWORD=password123
```

**Security:**
- NEVER log credentials
- NEVER commit credential files
- Read at runtime only

### Step 3: Initialize Browser

**First Scenario Only:**

1. Use `mcp_playwright_browser_navigate` to open FSM portal
2. Browser stays open for all scenarios
3. Reuse session across tests

**Benefits:**
- Eliminates repeated logins (~2 min/scenario saved)
- Maintains FSM session state
- Faster navigation

### Step 4: Execute Each Scenario

For each scenario in test instructions:

#### 4.1 Prepare Evidence Folder

Create folder for scenario evidence:
```
Projects/{Client}/Temp/evidence/{scenario_id}/
```

#### 4.2 Follow Test Steps EXACTLY (REGRESSION TESTING MODE)

**This section applies to REGRESSION TESTING with existing TES-070 documents.**

For NET NEW TESTING (generic test scripts without detailed TES-070), use adaptive execution based on scenario objectives.

---

**CRITICAL: Use TES-070 Values - Don't Ask User**

When executing regression tests, the TES-070 document contains ALL the values you need:
- Account numbers
- Vendor IDs
- Authority codes
- Amounts
- Dates
- Descriptions
- Any other field values

**DO NOT ask the user for these values. Use what's in the TES-070 document.**

**ONLY ask the user if:**
- A value from TES-070 causes an error (e.g., "Account 12345 is invalid")
- FSM rejects a value (e.g., "Vendor V001 not found")
- A field is required but not specified in TES-070
- You encounter an unexpected validation error

**Example - CORRECT:**

TES-070 says: "Create invoice with Vendor V12345, Amount $500.00, Account 6010-100-1000"

Agent does:
1. Use Vendor = "V12345" (from TES-070)
2. Use Amount = "$500.00" (from TES-070)
3. Use Account = "6010-100-1000" (from TES-070)
4. Execute without asking user

**Example - INCORRECT:**

TES-070 says: "Create invoice with Vendor V12345, Amount $500.00, Account 6010-100-1000"

Agent does:
1. Ask user: "What vendor should I use?" ❌ WRONG - Use V12345 from TES-070
2. Ask user: "What amount?" ❌ WRONG - Use $500.00 from TES-070
3. Ask user: "What account?" ❌ WRONG - Use 6010-100-1000 from TES-070

**Example - CORRECT (Error Handling):**

TES-070 says: "Create invoice with Account 6010-100-1000"

Agent tries to use account, FSM shows error: "Account 6010-100-1000 is invalid"

Agent does:
1. Take screenshot of error
2. Ask user: "TES-070 specifies account 6010-100-1000, but FSM says it's invalid. Should I use a different account?"
3. Wait for user response

---

**DO NOT interpret or translate test steps. Follow them EXACTLY as written in the TES-070 document.**

The TES-070 document provides the exact test steps that must be executed. You are NOT allowed to:
- Interpret what you think the step means
- Substitute similar values or navigation paths
- Skip steps or combine steps
- Add extra steps not specified
- Deviate in any way from the written steps

**TES-070 Step Example:**
```
Step 1: Log In as Staff Accountant role. 
Process Journals>Create
Create Manual Journal with total functional debit amount below $1,000 and release the transaction.

The status of the transaction turns to Pending Approval.
```

**How to Execute (CORRECT):**

1. **Parse the step into atomic actions:**
   - "Log In as Staff Accountant role" → Switch to "Staff Accountant" role using role dropdown
   - "Process Journals>Create" → Navigate to "Process Journals" menu, then click "Create"
   - "Create Manual Journal" → Fill form with required fields
   - "total functional debit amount below $1,000" → Use amount like $999.99 or $500.00
   - "release the transaction" → Click "Release" button
   - "status turns to Pending Approval" → Verify status field shows "Pending Approval"

2. **Execute each atomic action in exact order:**
   - Take snapshot (find elements)
   - Execute action with exact parameters from TES-070
   - Wait for completion
   - Verify result matches TES-070 expectation
   - Take screenshot (evidence)
   - Move to next action

3. **DO NOT:**
   - Substitute similar roles (e.g., "Global Ledger" instead of "Staff Accountant") ❌
   - Use similar navigation paths (e.g., "Journals" instead of "Process Journals") ❌
   - Change amounts or values (e.g., $1,000 instead of < $1,000) ❌
   - Skip steps or combine steps ❌
   - Add extra steps not in TES-070 ❌
   - Interpret or assume what the step means ❌

**Example - CORRECT Execution:**

TES-070 says: "Log In as Staff Accountant role"

Agent does: 
1. Take snapshot
2. Find role dropdown (combobox showing current role)
3. Click role dropdown to open options
4. Find "Staff Accountant" option in dropdown
5. Click "Staff Accountant" option
6. Wait for role to load
7. Verify "Staff Accountant" is now selected
8. Take screenshot (evidence of Staff Accountant role active)

**Example - INCORRECT Execution:**

TES-070 says: "Log In as Staff Accountant role"

Agent does:
1. Take snapshot
2. See "Global Ledger" role is already selected
3. Assume "Global Ledger" has journal functionality
4. Continue without switching roles ❌ WRONG - Must switch to "Staff Accountant"

OR

Agent does:
1. Take snapshot
2. Don't see "Staff Accountant" in visible options
3. Assume it doesn't exist and try "Global Ledger" instead ❌ WRONG - Must search/scroll to find "Staff Accountant"

**The TES-070 document is the source of truth. Every word matters. Follow it exactly.**

#### 4.3 Validate Step Completion

After executing each TES-070 step, verify:

1. **Action completed successfully** - No errors, expected element appeared
2. **Result matches TES-070 expectation** - Status changed, form saved, role switched, etc.
3. **Ready for next step** - Page loaded, elements visible, correct state

**If validation fails:**
- Take screenshot of current state
- Document what was expected (from TES-070) vs what actually happened
- Reference TES-070 step number
- STOP scenario execution (don't continue with invalid state)
- Report failure with evidence

**Validation Examples:**

TES-070 says: "The status of the transaction turns to Pending Approval"
Validation:
1. Take snapshot
2. Find status field on page
3. Extract status value
4. Verify status = "Pending Approval" (exact match)
5. If not matching, STOP and document failure

TES-070 says: "Log In as Staff Accountant role"
Validation:
1. Take snapshot
2. Find role indicator (combobox or header showing current role)
3. Extract current role name
4. Verify role = "Staff Accountant" (exact match)
5. If not matching, STOP and document failure

#### 4.3 Execute Browser Actions

Use MCP Playwright tools:

**Navigation:**
```
mcp_playwright_browser_navigate(url="...")
```

**Find Elements:**
```
mcp_playwright_browser_snapshot()
```
Returns page structure with element refs.

**Click Elements:**
```
mcp_playwright_browser_click(
    ref="element_ref_from_snapshot",
    element="Human-readable description"
)
```

**Type Text:**
```
mcp_playwright_browser_type(
    ref="element_ref_from_snapshot",
    text="Text to type",
    element="Field description"
)
```

**Fill Forms:**
```
mcp_playwright_browser_fill_form(
    fields=[
        {"name": "Company", "type": "textbox", "ref": "...", "value": "100"},
        {"name": "Vendor", "type": "textbox", "ref": "...", "value": "V12345"}
    ]
)
```

**Wait for Elements:**
```
mcp_playwright_browser_wait_for(text="Expected text")
```

**Capture Evidence:**
```
mcp_playwright_browser_take_screenshot(
    filename="Projects/{Client}/Temp/evidence/{scenario_id}/step_{n}.png"
)
```

#### 4.4 Critical Action Pattern

**Before Every Action:**
1. Take snapshot to find element refs
2. Identify target element
3. Execute action with ref
4. Wait for completion

**After Critical Steps:**
1. Take screenshot for evidence
2. Verify expected state
3. Document any errors

#### 4.5 Validate Results

Compare actual results with expected results:

**Expected:** "Invoice submitted for approval"
**Actual:** Check page for confirmation message

**Expected:** "Work unit status: Completed"
**Actual:** Navigate to Work Units, search by ID, verify status

#### 4.6 Handle Errors

**UI Errors:**
- Capture screenshot of error message
- Document error text
- Record work unit ID (if applicable)
- Continue to next scenario (don't stop entire run)

**Browser Errors:**
- Log error details
- Attempt recovery (refresh page, re-login)
- If unrecoverable, skip scenario and continue

### Step 5: Monitor Work Units (CRITICAL for Approval Workflows)

For scenarios that trigger IPA processes (approval workflows):

**IMPORTANT**: Approval workflows are ASYNCHRONOUS. After submitting an invoice for approval:
- The submission returns immediately (within seconds)
- The approval IPA runs in the background (can take 5-10 minutes)
- Custom fields (SONH Approval Status, Work Unit Reference #) update when IPA completes
- You MUST monitor work units to verify approval completion

#### 5.1 Navigate to Work Units

1. Switch to "Process Server Administrator" role
2. Expand "Administration" menu
3. Click "Work Units"

#### 5.2 Search for Work Unit

Search by:
- Work unit ID (if known from submission confirmation)
- Process name (e.g., "SONH_AP_ExpenseInvoiceApproval")
- Work title (contains invoice number, e.g., "TEST-GHR-001")
- Status: All or Pending/Running

**Search Tips**:
- Use partial matches (e.g., "Approval" finds all approval processes)
- Sort by "Created" date descending (newest first)
- Filter by date range (Today, Last 7 Days)

#### 5.3 Extract Status

Take snapshot and extract status from page:
- Look for status column
- Common statuses: Pending, Running, Completed, Failed, Canceled

**Status Meanings**:
- **Pending**: Work unit queued, not started yet
- **Running**: IPA currently executing
- **Completed**: IPA finished successfully
- **Failed**: IPA encountered error
- **Canceled**: Work unit manually canceled

#### 5.4 Adaptive Polling

Poll work unit status with adaptive intervals:

**0-2 minutes:** Poll every 10 seconds (fast initial check)
**2-5 minutes:** Poll every 30 seconds (moderate check)
**5+ minutes:** Poll every 60 seconds (slow check)
**Timeout:** 10 minutes (600 seconds) - if not complete, document and continue

**Polling Actions**:
1. Refresh page (F5 or reload button)
2. Take snapshot
3. Extract status from page
4. Check if terminal state (Completed, Failed, Canceled)
5. If not terminal, wait interval and repeat
6. If timeout reached, document current status and continue

**Example Polling Code**:
```
Wait 10 seconds
Refresh page
Take snapshot
Extract status
If status = "Completed": Success, continue to validation
If status = "Running" or "Pending": Continue polling
If status = "Failed": Document error, continue testing
If timeout (10 minutes): Document timeout, continue testing
```

#### 5.5 Terminal States

**Completed:** ✅ Success - scenario passed, proceed to validation
**Failed:** ❌ Error - document error message, continue testing
**Canceled:** ⚠️ Canceled - document reason, continue testing
**Timeout:** ⏱️ Timeout - document current status, may need manual follow-up

#### 5.6 Validate Approval Results (After Work Unit Completes)

Once work unit reaches terminal state (Completed), navigate back to invoice and verify:

1. **Invoice Status**: Should change from "Pending Approval" to "Released" (if auto-approved)
2. **SONH Approval Status**: Should change from "Unsubmitted" to "Approved"
3. **SONH Work Unit Reference #**: Should be populated with work unit ID
4. **Approval Tracking**: Should show "Approved" action with timestamp

**Validation Steps**:
```
1. Navigate back to Payables > Invoices
2. Search for invoice by number (e.g., "TEST-GHR-001")
3. Open invoice
4. Take snapshot
5. Check Status field (should be "Released" if auto-approved)
6. Check SONH Approval Status field (should be "Approved")
7. Check SONH Work Unit Reference # (should have work unit ID)
8. Click "Approval Information" tab
9. Check Approval Tracking (should show "Approved" action)
10. Take screenshot (evidence of approval)
```

**Expected Results for Auto-Approval**:
- Status: Released
- SONH Approval Status: Approved
- SONH Work Unit Reference #: Populated (e.g., "12345")
- Approval Tracking: Shows "Submitted" followed by "Approved"

**If Not Auto-Approved**:
- Status: Pending Approval
- SONH Approval Status: Pending or Unsubmitted
- Approval Tracking: Shows "Submitted" only or "Pending" with approver name
- This may be expected behavior depending on business rules

### Step 6: Document Results

For each scenario:

**Passed:**
- Scenario ID
- Title
- Evidence screenshots
- Work unit ID (if applicable)
- Execution time

**Failed:**
- Scenario ID
- Title
- Error message
- Error screenshot
- Work unit ID (if applicable)
- Expected vs actual results

### Step 7: Close Browser

**After All Scenarios Complete:**

Close browser to clean up resources.

**Don't Close Between Scenarios:**
- Wastes time (repeated logins)
- Loses session state
- Slower execution

## FSM Navigation Patterns

### Login Flow

```
1. Navigate to FSM portal URL
2. Take snapshot
3. Click "Cloud Identities" (or authentication method)
4. Wait for login form
5. Type email/username
6. Click "Next"
7. Wait for password field
8. Type password
9. Click "Sign In"
10. Handle "Stay signed in?" (click "Yes" or "No")
11. Wait for portal to load (look for "Applications" text)
12. Take screenshot (evidence of successful login)
```

### Payables Navigation

```
1. Take snapshot
2. Click sidebar menu (☰)
3. Wait for menu to expand
4. Click "Applications"
5. Scroll to "Financials & Supply Management"
6. Click FSM application
7. Wait for iframe to load
8. Switch to iframe context
9. Take snapshot (inside iframe)
10. Click "Payables" role
11. Wait for Payables homepage
12. Take screenshot (evidence of successful navigation)
```

### Invoice Creation

```
1. Take snapshot
2. Click "Create Invoice" button
3. Wait for form to load
4. Fill form fields:
   - Company
   - Vendor
   - Invoice Number
   - Invoice Date
   - Amount
   - Description
   - Authority Code (if applicable)
5. Take screenshot (filled form)
6. Click "Save" button
7. Wait for save confirmation
8. Take screenshot (saved invoice)
```

### Submit for Approval

```
1. Take snapshot
2. Click "Submit for Approval" button (or "More Actions" > "Submit for Approval")
3. Wait for confirmation dialog
4. Click "Confirm" or "OK"
5. Wait for submission confirmation
6. Take screenshot (confirmation message)
7. Extract work unit ID from message (if displayed)
```

## Multi-Selector Fallback

For reliability, try multiple selectors for each element:

**Example - Next Button:**
```
Selectors to try:
1. input[type="submit"]
2. #idSIButton9
3. button:has-text("Next")
4. [aria-label="Next"]
```

**Pattern:**
1. Take snapshot
2. Try first selector
3. If not found, try second selector
4. Continue until element found or all selectors exhausted
5. If all fail, log error and skip action

## Error Recovery

### Page Not Loading

**Symptoms:** Timeout waiting for element

**Recovery:**
1. Refresh page
2. Wait for page load
3. Retry action

### Element Not Found

**Symptoms:** Snapshot doesn't contain expected element

**Recovery:**
1. Take new snapshot
2. Try alternative selectors
3. Check if page structure changed
4. Document issue and skip action

### Session Expired

**Symptoms:** Redirected to login page

**Recovery:**
1. Re-login with credentials
2. Navigate back to previous location
3. Retry action

### Iframe Issues

**Symptoms:** Elements not found inside FSM application

**Recovery:**
1. Verify iframe loaded
2. Switch to iframe context
3. Take snapshot inside iframe
4. Retry action

## Performance Tips

1. **Keep browser open** - Don't close between scenarios
2. **Reuse sessions** - Maintain login state
3. **Adaptive polling** - Start fast, slow down over time
4. **Parallel snapshots** - Take snapshot once, use multiple times
5. **Efficient waits** - Wait for specific elements, not arbitrary delays

## Common Issues

### Issue: Login fails

**Cause:** Incorrect credentials or authentication method

**Solution:**
- Verify credentials in `.env.fsm` and `.env.passwords`
- Check authentication method (Cloud Identities vs Azure)
- Try manual login to verify credentials work

### Issue: Elements not found

**Cause:** Page structure changed or selectors outdated

**Solution:**
- Take snapshot and review page structure
- Update selectors to match current page
- Use multi-selector fallback

### Issue: Iframe not loading

**Cause:** FSM application slow to load or network issues

**Solution:**
- Increase wait time for iframe
- Check network connectivity
- Verify FSM URL is accessible

### Issue: Work unit not found

**Cause:** Work unit ID not captured or search criteria incorrect

**Solution:**
- Verify work unit ID from submission confirmation
- Try searching by process name or work title
- Check if work unit created in different environment

### Issue: Approval status not updating (COMMON)

**Cause:** Approval IPA still running (async process)

**Symptoms:**
- Invoice status: "Pending Approval"
- SONH Approval Status: "Unsubmitted"
- SONH Work Unit Reference #: Empty
- Approval Tracking: Shows "Submitted" only

**Solution:**
- **DO NOT assume failure immediately**
- Wait 5-10 minutes for approval IPA to complete
- Navigate to Work Units and search for approval process
- Monitor work unit status until "Completed"
- Return to invoice and refresh to see updated status
- Custom fields update AFTER work unit completes

**Validation Timeline:**
- 0-15 seconds: Submission confirmed, invoice shows "Pending Approval"
- 15 seconds - 5 minutes: Approval IPA running in background
- 5-10 minutes: Approval IPA completes, custom fields update
- After completion: Status changes to "Released", SONH fields populated

### Issue: Invoice out of balance

**Cause:** No distributions created, invoice amount doesn't match distribution total

**Symptoms:**
- Warning: "total distribution amount of 0.000 is not equal to invoice amount of 100.000"
- Out Of Balance: Shows negative amount (e.g., -100.00)
- Can still submit for approval (warning, not error)

**Impact:**
- May prevent auto-approval (depends on business rules)
- Invoice may require manual approval even if vendor class = GHR
- Approval workflow may have additional validation

**Solution:**
- Add distributions before submitting for approval
- Ensure distribution total equals invoice amount
- Use Distribution Code or manual distribution entry
- Verify Out Of Balance = 0.00 before submission

### Issue: Custom fields not populated

**Cause:** Custom approval IPA not triggered or still running

**Symptoms:**
- SONH Approval Status: "Unsubmitted" (should be "Approved" or "Pending")
- SONH Work Unit Reference #: Empty (should have work unit ID)
- Approval Tracking: Shows "Submitted" only

**Solution:**
- Check if custom approval workflow is configured
- Verify approval code (e.g., AP-EXP-INV) routes to custom IPA
- Search Work Units for approval process
- Wait for work unit to complete
- Refresh invoice page to see updated custom fields

### Issue: Auto-approval not working

**Cause:** Business rule conditions not met or configuration issue

**Symptoms:**
- Invoice remains in "Pending Approval" status
- Manual approval buttons appear (Manual Approve, Manual Reject)
- Approval Tracking shows "Pending" with approver name

**Possible Reasons:**
- Vendor class rule not configured (e.g., GHR auto-approval)
- Invoice out of balance (distributions required)
- Authority code doesn't match rule (e.g., needs AP1 or PR1)
- Additional conditions not met (amount threshold, cost center, etc.)
- Auto-approval workflow not active in environment

**Solution:**
- Verify business rules for auto-approval
- Check vendor class, authority code, amount, etc.
- Ensure invoice is balanced (distributions match amount)
- Confirm auto-approval configuration is active
- May need manual approval if conditions not met

## Next Steps

After test execution:

1. **Review Evidence** - Check screenshots in `Temp/evidence/`
2. **Document Results** - Create summary report
3. **Follow Up** - Investigate any failures

## Related Files

- `tes070-parsing.md` - Previous step (parse TES-070)
- `evidence-collection.md` - Evidence capture details
- `fsm-navigation.md` - FSM UI navigation patterns
- `work-unit-monitoring.md` - Work unit monitoring details
