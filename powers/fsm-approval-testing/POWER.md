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

### First-Time Setup

1. **Verify FSM Credentials**
   - Credentials stored in `Projects/{ClientName}/Credentials/`
   - `.env.fsm` - FSM URL, username, environment
   - `.env.passwords` - FSM password (NEVER commit to git)

2. **Verify TES-070 Documents**
   - Located in `Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/`
   - Must be Word documents (.docx format)
   - Should contain test scenarios with steps and expected results

3. **Verify Python Tools**
   - `ReusableTools/tes070_analyzer.py` - Parse TES-070 documents
   - `ReusableTools/create_test_instructions.py` - Generate test instructions JSON
   - `ReusableTools/validate_json.py` - Validate JSON files

4. **Verify MCP Playwright Tools**
   - Browser automation tools should be available
   - Test with simple navigation before full test execution

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

1. Power loads FSM credentials
2. For each scenario in test instructions:
   - Launch browser (if not already open)
   - Navigate to FSM portal
   - Login with credentials
   - Execute test steps using MCP Playwright tools
   - Take snapshots before each action (find element refs)
   - Capture screenshots after critical steps
   - Validate results against expected outcomes
3. Keep browser open across scenarios (efficiency)
4. Close browser after all scenarios complete

**Evidence**: `Projects/{Client}/Temp/evidence/{scenario_id}/`

### Phase 4: Report Results

1. Display summary:
   - Total scenarios executed
   - Passed count
   - Failed count
   - Pass rate percentage
2. List evidence locations
3. Document any errors or issues

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

1. Switch to "Process Server Administrator" role
2. Expand "Administration" menu
3. Click "Work Units"
4. Search by work unit ID or process name
5. Extract status from page
6. Refresh page to get updated status
7. Poll until terminal state (Completed, Failed, Canceled)

## Steering Files

Detailed workflow guides available in `steering/` directory:

- `tes070-parsing.md` - Parse TES-070 documents and extract scenarios
- `test-execution.md` - Execute test scenarios with browser automation
- `evidence-collection.md` - Capture screenshots and document results
- `fsm-navigation.md` - Navigate FSM UI (login, roles, modules)
- `work-unit-monitoring.md` - Monitor work unit status and completion

## Best Practices

### Browser Automation

- **Take snapshots before every action** - Find element refs dynamically
- **Keep browser open across scenarios** - Eliminates repeated logins (~2 min/scenario saved)
- **Use multi-selector fallback** - Try multiple selectors for reliability
- **Wait for elements** - Don't assume instant page loads
- **Handle iframes** - FSM uses iframes for application content

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
- Evidence Screenshots: `Projects/{ClientName}/Temp/evidence/{scenario_id}/`

### Python Tools

- `ReusableTools/tes070_analyzer.py` - Parse TES-070 documents
- `ReusableTools/create_test_instructions.py` - Generate test instructions
- `ReusableTools/validate_json.py` - Validate JSON files

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
5. Return to invoice and refresh page
6. Verify custom fields now populated (SONH Approval Status, Work Unit Reference #)

**Key Learning**: Always monitor work units for approval workflows. Custom fields update AFTER work unit completes, not immediately after submission.

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
