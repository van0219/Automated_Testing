---
name: "fsm-approval-testing"
displayName: "FSM Approval Testing"
description: "Automated regression testing for FSM approval workflows using existing TES-070 documents. Parses TES-070, executes test scenarios via browser automation, captures evidence, and validates results."
keywords: ["fsm", "approval", "testing", "tes-070", "regression", "expense", "invoice", "journal", "payables", "approval workflow", "test automation", "browser automation"]
---

# FSM Approval Testing Power

Automated regression testing for FSM (Financials & Supply Management) approval workflows using existing TES-070 test documents.

## Overview

This power enables automated testing of FSM approval workflows by:
1. Parsing existing TES-070 test documents
2. Extracting test scenarios and steps
3. Executing tests via browser automation (Playwright MCP)
4. Capturing evidence (screenshots)
5. Validating results against expected outcomes

## When to Use This Power

Use this power when:
- Testing FSM approval workflows (expense invoices, journals, cash transactions)
- Performing regression testing from existing TES-070 documents
- Validating approval routing logic (BOA, Agency, Payroll Manager)
- Testing approval workflows after FSM updates or configuration changes
- Documenting test execution with screenshots and evidence

## Supported Approval Types

- **Expense Invoice Approval** (Payables module) - EXT_FIN_004 and similar
- **Manual Journal Approval** (General Ledger module) - EXT_FIN_001 and similar
- **Cash Ledger Transaction Approval** (Cash Management module) - EXT_FIN_016 and similar

## Onboarding

### Automatic Workspace Discovery (CRITICAL)

**When power activates, ALWAYS perform these steps FIRST:**

1. **Scan Projects Folder**
   - List all directories in `Projects/` folder
   - Identify available client projects (e.g., SONH, ClientB, ClientC)

2. **For Each Project, Check:**
   - TES-070 documents in `Projects/{Client}/TES-070/Approval_TES070s_For_Regression_Testing/`
   - Credentials configured in `Projects/{Client}/Credentials/`
   - List available test documents with extension IDs

3. **Present Contextual Summary to User:**
   ```
   ## FSM Approval Testing Power - Ready to Use!
   
   ### Your Current Setup
   
   **Available Projects:**
   - SONH (3 TES-070 documents, credentials configured)
   - ClientB (1 TES-070 document, credentials missing)
   
   **SONH - Available TES-070 Documents:**
   1. EXT_FIN_001 - Manual Journal Entry Approval
   2. EXT_FIN_004 - Expense Invoice Approval ✅ Previously tested
   3. EXT_FIN_016 - Cash Ledger Transaction Approval
   
   ### How to Use
   
   **Test Existing Workflows:**
   "Test EXT_FIN_001 for SONH"
   "Run all SONH approval tests"
   
   **Add New Client Project:**
   1. Trigger "New Project Setup" hook (userTriggered)
   2. Add FSM credentials to Projects/{NewClient}/Credentials/
   3. Add TES-070 documents to Projects/{NewClient}/TES-070/Approval_TES070s_For_Regression_Testing/
   4. Run approval tests - power will discover new project automatically
   
   What would you like to test?
   ```

4. **If No Projects Found:**
   - Explain that no client projects exist yet
   - Guide user to trigger "New Project Setup" hook
   - Explain folder structure and file requirements

### First-Time Setup (For New Projects)

1. **Create New Project**
   - Trigger "New Project Setup" hook (userTriggered)
   - Provides complete folder structure and credential templates

2. **Add FSM Credentials**
   - `.env.fsm` - FSM URL, username, environment
   - `.env.passwords` - FSM password (NEVER commit to git)
   - Location: `Projects/{ClientName}/Credentials/`

3. **Add TES-070 Documents**
   - Must be Word documents (.docx format)
   - Should contain test scenarios with steps and expected results
   - Extension IDs should start with "EXT_" (e.g., EXT_FIN_004)
   - Location: `Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/`

4. **Verify Python Tools** (one-time check)
   - `ReusableTools/tes070_analyzer.py` - Parse TES-070 documents
   - `ReusableTools/create_test_instructions.py` - Generate test instructions JSON
   - `ReusableTools/validate_json.py` - Validate JSON files

5. **Verify MCP Playwright Tools** (one-time check)
   - Browser automation tools should be available (built into Kiro)
   - Test with simple navigation before full test execution

## Testing Modes: Regression vs Net New

This power supports TWO distinct testing modes with different adherence requirements:

### Mode 1: Regression Testing (EXACT ADHERENCE REQUIRED) ⚠️

**When**: Testing existing functionality using completed TES-070 documents with detailed test steps

**Rule**: **YOU MUST FOLLOW TES-070 TEST STEPS EXACTLY AS WRITTEN. DO NOT INTERPRET. DO NOT DEVIATE. DO NOT CREATE YOUR OWN STEPS.**

The TES-070 document contains the EXACT test steps that must be executed. Every word is a requirement, not a suggestion.

### Examples of Exact Adherence:

- If TES-070 says "Log In as Staff Accountant role" → Switch to "Staff Accountant" role (NOT "Global Ledger" or any other role)
- If TES-070 says "Process Journals > Create" → Navigate to exactly "Process Journals" then "Create" (NOT "Journals" or similar menu)
- If TES-070 says "amount below $1,000" → Use amount like $999.99 or $500.00 (NOT $1,000 or $1,500)
- If TES-070 says "event code not equal to TR and BOA" → Use event code like "GE" or "AD" (NOT "TR" or "BOA")
- If TES-070 says "Release the transaction" → Click "Release" button (NOT "Submit" or "Save")

### What This Means:

1. **Read the TES-070 step word-by-word** - Every detail matters
2. **Execute exactly what it says** - No interpretation, no assumptions
3. **Use exact values specified** - Amounts, codes, roles, navigation paths
4. **Follow exact order** - Don't skip steps, don't reorder steps
5. **Verify exact results** - Check that outcome matches TES-070 expectation

### What NOT to Do:

- ❌ Substitute similar roles (e.g., "Global Ledger" instead of "Staff Accountant")
- ❌ Use similar navigation (e.g., "Journals" instead of "Process Journals")
- ❌ Change values (e.g., $1,000 instead of < $1,000)
- ❌ Skip steps or combine steps
- ❌ Add extra steps not in TES-070
- ❌ Interpret what you think the step means

### Validation After Each Step:

After executing each TES-070 step:
1. Verify action completed successfully
2. Verify result matches TES-070 expectation
3. Take screenshot for evidence
4. If validation fails, STOP and document the issue

**The TES-070 document is the source of truth. Follow it exactly.**

### Mode 2: Net New Testing (ADAPTIVE EXECUTION)

**When**: Testing new functionality using generic test scripts from functional consultants with:
- High-level scenarios (no detailed TES-070)
- Few or incomplete test steps
- General test objectives without exact navigation paths

**Rule**: **Use your knowledge and instincts to execute tests based on the generic test script provided.**

In this mode:
- ✅ Interpret scenario descriptions and create appropriate test steps
- ✅ Use FSM navigation knowledge to find appropriate paths
- ✅ Make reasonable assumptions about values (amounts, codes, etc.)
- ✅ Adapt to FSM UI structure and available options
- ✅ Create comprehensive test coverage based on scenario intent
- ✅ Document your approach and decisions

**Example - Net New Test Script:**
```
Scenario: Test manual journal approval for amounts under $1,000
Expected: Journal should route to Agency approver and be approved
```

**Your Approach:**
1. Determine appropriate role (Staff Accountant or Global Ledger)
2. Navigate to journal creation (Process Journals or similar)
3. Create journal with reasonable amount (e.g., $500)
4. Choose appropriate event code (not TR or BOA)
5. Submit for approval
6. Monitor work unit and verify approval routing
7. Document all steps taken

**Key Difference:**
- **Regression**: Follow exact steps from TES-070 (e.g., "Staff Accountant role", "Process Journals > Create")
- **Net New**: Use judgment to achieve scenario objective (e.g., "create journal under $1,000 and verify approval")

### How to Identify Testing Mode

**Regression Testing Indicators:**
- Existing TES-070 document with detailed steps
- Each step has specific navigation paths, values, and expected results
- Document shows "PASS" results from previous testing
- Purpose is to verify existing functionality still works

**Net New Testing Indicators:**
- Generic test script or scenario description
- High-level objectives without detailed steps
- No previous test results or TES-070 document
- Purpose is to test new functionality or create initial test documentation

**When in doubt**: Ask the user which mode to use or check if a TES-070 document exists.

---

## Workflow

### Phase 1: Parse TES-070 Document

1. User selects client project
2. User selects TES-070 document
3. Power runs `tes070_analyzer.py` to extract:
   - Document metadata (title, version, author)
   - Test summary (total tests, passed, failed)
   - Test scenarios with steps and expected results
   - Transaction type (ExpenseInvoice, ManualJournal, etc.)

**Output**: `{TES070_filename}_analysis.json`

### Phase 2: Create Test Instructions

1. Power runs `create_test_instructions.py` with analysis JSON
2. Extracts executable scenarios (skips TOC entries)
3. Creates simplified test instructions with:
   - Scenario title and description
   - Test steps (human-readable)
   - Expected results
4. Validates JSON structure

**Output**: `Projects/{Client}/TestScripts/approval/{extension_id}_test_instructions.json`

### Phase 3: Execute Tests

**CRITICAL: Load Client Metadata First**

Before executing tests, load client metadata from the project README:

```python
from ReusableTools.read_client_metadata import get_client_metadata

metadata = get_client_metadata("SONH")
client_code = metadata['client_code']        # "SONH"
client_name = metadata['client_name']        # "State of New Hampshire"
tenant_id = metadata['tenant_id']            # "NMR2N66J9P445R7P_AX4"
```

This ensures the test results JSON has the correct `client` (short code) and `client_name` (full name) for TES-070 generation.

**CRITICAL: Use TES-070 Values - Don't Ask User**

For regression testing, the TES-070 document contains ALL the values you need (accounts, vendors, amounts, codes, etc.). Use these values directly without asking the user.

**ONLY ask the user if:**
- A TES-070 value causes an FSM error (e.g., "Account 12345 is invalid")
- A required field is not specified in TES-070
- You encounter an unexpected validation error

**Execution Steps:**

1. Load client metadata using `read_client_metadata.py`
2. Load FSM credentials from `Projects/{client}/Credentials/`
3. For each scenario in test instructions:
   - Launch browser (if not already open)
   - Navigate to FSM portal
   - Login with credentials
   - Execute test steps using MCP Playwright tools
   - **Use exact values from TES-070** (accounts, vendors, amounts, codes)
   - Take snapshots before each action (find element refs)
   - Capture screenshots after critical steps
   - Validate results against expected outcomes
3. Keep browser open across scenarios (efficiency)
4. Close browser after all scenarios complete

**Output**: `Projects/{Client}/Temp/test_results_{extension_id}.json`

**Test Results JSON Structure:**
```json
{
  "extension_id": "EXT_FIN_004",
  "client": "SONH",                    // Short code for folder paths
  "client_name": "State of New Hampshire",  // Full name for TES-070 display
  "test_date": "2026-03-10",
  "tester": "Automated Testing (Kiro)",
  "environment": "NMR2N66J9P445R7P_AX4",
  "scenarios": [...]
}
```

**CRITICAL**: Always load client metadata from README using `read_client_metadata.py` to get the correct `client_name`.

### Phase 4: Report Results

1. Display summary:
   - Total scenarios executed
   - Passed count
   - Failed count
   - Pass rate percentage
2. List evidence locations
3. Document any errors or issues

### Phase 5: Generate Updated TES-070 Document

1. Prepare test results JSON from Phase 3 execution data
2. Run `generate_regression_tes070.py` with test results
3. Generate Word document with:
   - Updated test summary (Pass/Fail statistics)
   - All test scenarios with current results
   - Embedded evidence screenshots
   - Expected vs Actual comparisons
   - Work unit references
   - Execution metadata (date, tester, environment)
4. Validate document completeness
5. Report generation results to user

**Output**: `Projects/{Client}/TES-070/Generated_TES070s/{client}_{extension_id}_Regression_{timestamp}.docx`

**Purpose**: Provide stakeholders with updated TES-070 document showing current state of approval workflow testing. Even though original TES-070 exists, it may be outdated - this creates fresh documentation with latest test results.

**Note**: For interface testing (INT_FIN_XXX), use `generate_tes070_from_json.py` instead. For approval testing regression (EXT_FIN_XXX), use `generate_regression_tes070.py`.

## MCP Playwright Tools

This power uses MCP Playwright tools that are **built into Kiro** (no external MCP server needed):

- `mcp_playwright_browser_navigate` - Navigate to URLs
- `mcp_playwright_browser_snapshot` - Capture page structure (find elements)
- `mcp_playwright_browser_click` - Click elements
- `mcp_playwright_browser_type` - Type text into fields
- `mcp_playwright_browser_fill_form` - Fill multiple form fields
- `mcp_playwright_browser_take_screenshot` - Capture evidence
- `mcp_playwright_browser_wait_for` - Wait for elements/text
- `mcp_playwright_browser_evaluate` - Execute JavaScript

**Note**: These tools are provided by Kiro's built-in Playwright MCP server. No additional installation or configuration required.

## FSM Navigation Patterns

### Login Flow

1. Navigate to FSM portal URL
2. Select authentication method (Cloud Identities/Azure)
3. Enter email/username
4. Click Next
5. Enter password
6. Click Sign In
7. Handle "Stay signed in?" prompt
8. Wait for portal to load

### Payables Navigation

1. Expand sidebar menu (☰)
2. Click "Applications"
3. Scroll to "Financials & Supply Management"
4. Click FSM application
5. Wait for iframe to load
6. Switch to iframe context
7. Select "Payables" role
8. Navigate to invoice management

### Work Unit Monitoring

**Accessing Process Server Administrator:**

**Method 1: From Portal (First Time)**
1. Click "Open navigation menu" button (grid icon at top)
2. Take snapshot to see navigation menu
3. Click "See more" under Applications section
4. Click "Financials & Supply Management"
5. Click "Process Server Administrator" role

**Method 2: Role Switcher (Already in FSM)**
1. Take snapshot to find role switcher combobox
2. Click combobox (e.g., "Payables, Payables")
3. Wait 1 second for dropdown
4. Take snapshot to see roles
5. Click "Process Server Administrator"
6. Wait 3 seconds for role to load

**Method 3: User Settings (Preferred Application)**
1. Click "More" menu → "Settings"
2. Change "Preferred Application" to "Process Server Administrator"
3. Click "Save"

**Navigating to Work Units:**
1. Once in Process Server Administrator role
2. Expand "Administration" menu
3. Click "Work Units"
4. Search by work unit ID or process name
5. Extract status from page
6. Refresh page to get updated status
7. Poll until terminal state (Completed, Failed, Canceled)

**CRITICAL**: Use snapshot + click pattern for all navigation. Never use run_code for clicking elements.

## Steering Files

Detailed workflow guides available in `steering/` directory:

- `tes070-parsing.md` - Parse TES-070 documents and extract scenarios
- `test-execution.md` - Execute test scenarios with browser automation
- `evidence-collection.md` - Capture screenshots and document results
- `tes070-generation.md` - Generate updated TES-070 documents with test results

## Best Practices

### Browser Automation

- **Take snapshots before every action** - Find element refs dynamically
- **Keep browser open across scenarios** - Eliminates repeated logins (~2 min/scenario saved)
- **Use multi-selector fallback** - Try multiple selectors for reliability
- **Wait for elements** - Don't assume instant page loads
- **Handle iframes** - FSM uses iframes for application content
- **Skip read-only fields** - Never attempt to populate disabled/read-only fields
- **Use lookup buttons** - For editable fields with lookups, use the lookup button instead of typing directly
- **Monitor approval workflows** - Approval IPAs are asynchronous, always monitor work units before validating results

### Evidence Collection

- **Screenshot after critical steps** - Invoice creation, submission, approval
- **Organize by scenario** - Separate folders per scenario
- **Clear naming** - `{scenario_id}_{step_number}_{action}.png`
- **Capture errors** - Screenshot error messages for debugging

### Error Handling

- **Document UI errors only** - Don't analyze work unit logs
- **Record work unit IDs** - For reference and troubleshooting
- **Continue on non-critical failures** - Don't stop entire test run
- **Clear error messages** - Explain what went wrong and why

### Performance

- **Sequential execution** - One scenario at a time (clear evidence)
- **Adaptive polling** - 10s → 30s → 60s intervals for work units
- **Timeout limits** - 10 minutes max for work unit completion
- **Browser efficiency** - Reuse browser session across scenarios

## File Locations

### Input Files

- TES-070 Documents: `Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/*.docx`
- FSM Credentials: `Projects/{ClientName}/Credentials/.env.fsm` and `.env.passwords`

### Generated Files

- TES-070 Analysis: `Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/*_analysis.json`
- Test Instructions: `Projects/{ClientName}/TestScripts/approval/{extension_id}_test_instructions.json`
- Test Results JSON: `Projects/{ClientName}/Temp/test_results_{extension_id}.json`
- Evidence Screenshots: `Projects/{ClientName}/Temp/evidence/{scenario_id}/`
- Updated TES-070 Document: `Projects/{ClientName}/TES-070/Generated_TES070s/{client}_{extension_id}_Regression_{timestamp}.docx`

### Python Tools

- `ReusableTools/tes070_analyzer.py` - Parse TES-070 documents
- `ReusableTools/create_test_instructions.py` - Generate test instructions
- `ReusableTools/validate_json.py` - Validate JSON files
- `ReusableTools/read_client_metadata.py` - Read client metadata from project README
- `ReusableTools/generate_regression_tes070.py` - Generate updated TES-070 documents from test results

## Security Notes

- **NEVER commit credentials** - `.env.fsm` and `.env.passwords` in `.gitignore`
- **NEVER log credentials** - Don't print passwords or tokens
- **Read credentials at runtime** - Load from Credentials/ directory
- **Secure evidence** - Screenshots may contain sensitive data

## Troubleshooting

### Power Not Activating

- Check keywords in your request match power keywords
- Try explicit activation: mention "FSM approval testing" or "TES-070"
- Verify power is installed (check Powers panel)

### MCP Tools Not Available

- Playwright MCP tools are **built into Kiro** - no separate server needed
- If tools not showing up, restart Kiro
- Check that you're using latest Kiro version with Playwright support

### Browser Automation Fails

- Check FSM credentials are correct
- Verify FSM URL is accessible
- Check for FSM UI changes (selectors may need updates)
- Review browser console for JavaScript errors
- **Use snapshot + click pattern** - Never use run_code for navigation
- **Handle modal states** - run_code doesn't handle beforeunload dialogs
- **Wait between actions** - Give UI time to update (1-3 seconds)

### Test Execution Slow

- Keep browser open across scenarios (don't close between tests)
- Reduce wait times where possible
- Use adaptive polling for work units
- Consider running fewer scenarios per session

### Approval Status Not Updating (CRITICAL)

**Symptom**: Invoice shows "Pending Approval" but SONH fields not populated

**Cause**: Approval IPA is ASYNCHRONOUS - runs in background after submission

**Timeline**:
- 0-15 seconds: Submission confirmed, invoice shows "Pending Approval"
- 15 seconds - 5 minutes: Approval IPA running in background
- 5-10 minutes: Approval IPA completes, custom fields update
- After completion: Status changes to "Released", SONH fields populated

**Solution**:
1. **DO NOT assume failure immediately**
2. Navigate to Process Server Administrator > Work Units
3. Search for approval process (by process name or invoice number)
4. Monitor work unit status until "Completed" (use adaptive polling)
5. Return to invoice form
6. Click "Refresh" button in form toolbar (do NOT refresh entire browser)
7. Verify custom fields now populated (SONH Approval Status, Work Unit Reference #)

**Key Learning**: Always monitor work units for approval workflows. Custom fields update AFTER work unit completes, not immediately after submission. Fields showing "Unsubmitted" or blank immediately after submission is NORMAL behavior.

### Read-Only Field Errors (CRITICAL)

**Symptom**: Errors when trying to populate certain fields, or fields don't accept input

**Cause**: Attempting to populate read-only or disabled fields

**Common Read-Only Fields**:
- **Voucher** - Auto-generated by FSM
- **Status** - Controlled by workflow
- **Total Distributions** - Calculated from distribution lines
- **Total Payments** - Calculated from payment lines
- **Balance** - Calculated field
- **Work Unit Reference #** - Populated by approval IPA

**Solution**:
1. Take snapshot before attempting to populate field
2. Check field attributes in snapshot:
   - `[disabled]` attribute = read-only
   - `paragraph` element = display-only (not editable)
   - `textbox` or `combobox` = editable
3. Skip read-only fields entirely - do NOT attempt to populate
4. For editable fields with lookups, use lookup button instead of typing directly

**Key Learning**: If a field is read-only, skip it entirely. Check snapshot for field type before attempting to populate. Use lookup buttons for editable fields.

### Invoice Out of Balance

**Symptom**: Warning "total distribution amount is not equal to invoice amount"

**Impact**: May prevent auto-approval depending on business rules

**Solution**:
- Add distributions before submitting for approval
- Ensure distribution total equals invoice amount
- Verify Out Of Balance = 0.00 before submission

### Auto-Approval Not Working

**Symptom**: Invoice remains "Pending Approval" with manual approval buttons

**Possible Causes**:
- Vendor class rule not configured (e.g., GHR auto-approval)
- Invoice out of balance (distributions required)
- Authority code doesn't match rule
- Additional conditions not met (amount threshold, cost center)
- Auto-approval workflow not active in environment

**Solution**:
- Verify business rules for auto-approval
- Check vendor class, authority code, amount, balance
- Confirm auto-approval configuration is active
- May need manual approval if conditions not met

### Navigation to Process Server Administrator Fails

**Symptom**: Can't find Process Server Administrator in navigation, stuck on Payables page

**Common Mistakes**:
- Trying to navigate using FSM sidebar (☰) - PSA is accessed via portal or role switcher
- Using run_code instead of snapshot + click pattern
- Not waiting for dropdowns to load before taking snapshot

**Solution - Portal Navigation (First Time)**:
1. Click "Open navigation menu" button (grid icon at top of portal)
2. Take snapshot to see navigation menu structure
3. Click "See more" under Applications section
4. Take snapshot to see all applications
5. Click "Financials & Supply Management"
6. Click "Process Server Administrator" role

**Solution - Role Switcher (Already in FSM)**:
1. Take snapshot to find role switcher combobox
2. Look for pattern: `combobox "[CurrentRole], [CurrentRole]"`
3. Click combobox using ref from snapshot
4. Wait 1 second for dropdown to load
5. Take snapshot to see available roles
6. Find "Process Server Administrator" option
7. Click using ref from snapshot
8. Wait 3 seconds for role to load

**Solution - User Settings**:
1. Click "More" menu in FSM header
2. Click "Settings"
3. Change "Preferred Application" to "Process Server Administrator"
4. Click "Save"
5. Refresh or navigate to FSM home

**Key Learning**: Portal navigation menu (grid icon) is DIFFERENT from FSM sidebar menu (☰). Use portal menu to access applications/roles, use FSM sidebar to navigate within a role.

## Example Usage

**User Request:**
```
Test the expense invoice approval workflow using TES-070 document EXT_FIN_004
```

**Power Activates:**
1. Keywords match: "approval workflow", "TES-070"
2. Power loads instructions and steering files
3. Agent follows workflow phases
4. Tests execute with browser automation
5. Evidence collected and results reported

## Related Documentation

- `.kiro/steering/00_Index.md` - Workspace overview and testing workflows
- `.kiro/steering/01_FSM_Navigation_Guide.md` - FSM UI navigation patterns
- `.kiro/steering/08_TES070_Standards_and_Generation.md` - TES-070 standards

## Version History

- **1.1.2** (2026-03-10) - Client metadata management
  - Added `read_client_metadata.py` utility to read client info from project README
  - Fixed root cause: client_name now loaded from README during test execution (Phase 3)
  - Updated SONH README with Client Information section (client code + full name)
  - Phase 3 now loads metadata before test execution to ensure correct TES-070 generation
  - Prevents "State of New Hampshire" folder creation issue (use short code for paths)
  - Test results JSON now correctly populates both `client` (short) and `client_name` (full)

- **1.1.1** (2026-03-10) - Test execution learnings and best practices
  - Added Rule 8: Approval Workflows Are Asynchronous (CRITICAL)
  - Added Rule 6: Skip Read-Only Fields (CRITICAL) to FSM Navigation Guide
  - Added read-only field troubleshooting section
  - Documented approval workflow timeline (0-15s submission, 5-10min completion)
  - Added validation steps for approval workflows
  - Clarified custom field update behavior (updates AFTER work unit completes)
  - Added common read-only fields list (Voucher, Status, calculated totals)
  - Improved best practices for browser automation
  - Validated with Scenario 3.1 (garnishment invoice auto-approval)

- **1.1.0** (2026-03-10) - TES-070 generation capability added
  - Added Phase 5: Generate Updated TES-070 Document
  - Created `tes070-generation.md` steering file with complete workflow
  - Captures test results JSON during execution (Phase 3)
  - Generates Word document with embedded screenshots and Pass/Fail status
  - Provides stakeholders with updated regression test documentation
  - Output: `Projects/{Client}/TES-070/Generated_TES070s/{client}_{extension_id}_Regression_{timestamp}.docx`

- **1.0.2** (2026-03-10) - Navigation improvements and troubleshooting
  - Added detailed Process Server Administrator navigation methods (portal, role switcher, settings)
  - Added troubleshooting section for navigation failures
  - Documented portal navigation menu vs FSM sidebar menu distinction
  - Added guidance on snapshot + click pattern vs run_code
  - Added modal state handling notes
  - Improved work unit monitoring navigation steps
  
- **1.0.1** (2026-03-10) - Test execution validation and improvements
  - Validated Scenario 3.1 execution (garnishment invoice auto-approval)
  - Added work unit monitoring guidance (CRITICAL for approval workflows)
  - Added approval status validation steps
  - Added common issues: approval status not updating, out of balance, auto-approval
  - Documented async approval workflow behavior
  - Added validation timeline (0-15s submission, 5-10min approval completion)
  - Improved troubleshooting section with real-world scenarios
  
- **1.0.0** (2026-03-06) - Initial release
  - TES-070 parsing
  - Test instruction generation
  - Browser automation execution
  - Evidence collection
  - Support for ExpenseInvoice, ManualJournal, CashLedgerTransaction

## License

Proprietary - For internal use only

## Support

For issues or questions:
1. Check steering files for detailed workflows
2. Review troubleshooting section
3. Check APPROVAL_TESTING_SOLUTIONS_HISTORY.md for known issues
4. Contact development team
