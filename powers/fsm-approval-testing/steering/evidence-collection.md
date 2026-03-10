# Evidence Collection Workflow

Guide for capturing screenshots and documenting test execution evidence.

## Overview

Evidence collection provides visual proof of test execution, validates results, and supports troubleshooting.

## Evidence Types

### Screenshots

**When to Capture:**
- After successful login
- After navigation to target module
- After form submission
- After approval actions
- After error messages
- After work unit status checks

**What to Include:**
- Full page or relevant section
- Clear visibility of key elements
- Timestamps (if available)
- Context (what action was just performed)

### Work Unit IDs

**When to Capture:**
- After invoice submission
- After approval submission
- From confirmation messages
- From work unit search results

**What to Record:**
- Work unit ID number
- Process name
- Work title
- Submission timestamp

### Error Messages

**When to Capture:**
- UI error dialogs
- Validation errors
- Submission failures
- Approval failures

**What to Record:**
- Full error message text
- Error code (if displayed)
- Context (what action triggered error)
- Screenshot of error

## Evidence Organization

### Folder Structure

```
Projects/{Client}/Temp/evidence/
├── {scenario_id}/
│   ├── 01_login.png
│   ├── 02_navigate_payables.png
│   ├── 03_create_invoice.png
│   ├── 04_filled_form.png
│   ├── 05_submit_confirmation.png
│   ├── 06_work_unit_status.png
│   └── results.json
```

### Naming Convention

**Format:** `{step_number}_{action_description}.png`

**Examples:**
- `01_login.png` - Login page after successful authentication
- `02_navigate_payables.png` - Payables homepage
- `03_create_invoice.png` - Invoice creation form
- `04_filled_form.png` - Completed invoice form
- `05_submit_confirmation.png` - Submission confirmation message
- `06_work_unit_status.png` - Work unit status page

**Benefits:**
- Sequential ordering (easy to follow)
- Descriptive names (understand context)
- Consistent format (easy to parse)

### Results JSON

**File:** `results.json` in scenario evidence folder

**Structure:**
```json
{
  "scenario_id": "3.1",
  "title": "Scenario title",
  "status": "passed",
  "execution_time": "2.5 minutes",
  "work_unit_id": "WU123456",
  "screenshots": [
    "01_login.png",
    "02_navigate_payables.png",
    "03_create_invoice.png",
    "04_filled_form.png",
    "05_submit_confirmation.png",
    "06_work_unit_status.png"
  ],
  "errors": [],
  "notes": "Invoice submitted successfully, approved by BOA"
}
```

## Screenshot Capture

### Using MCP Playwright

**Full Page Screenshot:**
```
mcp_playwright_browser_take_screenshot(
    filename="Projects/{Client}/Temp/evidence/{scenario_id}/01_login.png",
    fullPage=true,
    type="png"
)
```

**Element Screenshot:**
```
mcp_playwright_browser_take_screenshot(
    filename="Projects/{Client}/Temp/evidence/{scenario_id}/error_message.png",
    element="Error dialog",
    ref="element_ref_from_snapshot",
    type="png"
)
```

### Screenshot Quality

**Resolution:** Use default browser resolution (1920x1080 recommended)

**Format:** PNG (lossless, good for text)

**Size:** Full page for context, element for specific details

**Timing:** After action completes, before next action

## Evidence Validation

### Checklist

For each scenario, verify evidence includes:

- [ ] Login screenshot (proves authentication)
- [ ] Navigation screenshot (proves correct module)
- [ ] Form screenshot (proves data entry)
- [ ] Submission screenshot (proves action taken)
- [ ] Confirmation screenshot (proves success)
- [ ] Work unit screenshot (proves process triggered)
- [ ] Status screenshot (proves completion)

### Missing Evidence

**If screenshot missing:**
1. Document reason (error, timeout, skip)
2. Note in results.json
3. Continue with remaining evidence

**If critical evidence missing:**
1. Mark scenario as incomplete
2. Document what's missing
3. Consider re-running scenario

## Error Documentation

### UI Errors

**Capture:**
- Screenshot of error dialog
- Full error message text
- Error code (if displayed)
- Context (what action triggered)

**Document in results.json:**
```json
{
  "errors": [
    {
      "type": "UI Error",
      "message": "Vendor not found: V12345",
      "screenshot": "error_vendor_not_found.png",
      "context": "Creating expense invoice",
      "timestamp": "2026-03-06 14:23:45"
    }
  ]
}
```

### Work Unit Errors

**Capture:**
- Work unit ID
- Status (Failed, Canceled)
- Error message (if displayed)
- Screenshot of work unit page

**Document in results.json:**
```json
{
  "errors": [
    {
      "type": "Work Unit Error",
      "work_unit_id": "WU123456",
      "status": "Failed",
      "message": "No approver found for agency",
      "screenshot": "work_unit_failed.png",
      "timestamp": "2026-03-06 14:25:30"
    }
  ]
}
```

### Browser Errors

**Capture:**
- Error type (timeout, element not found, etc.)
- Action attempted
- Page URL
- Screenshot (if possible)

**Document in results.json:**
```json
{
  "errors": [
    {
      "type": "Browser Error",
      "message": "Element not found: Submit button",
      "action": "Click submit button",
      "url": "https://...",
      "screenshot": "element_not_found.png",
      "timestamp": "2026-03-06 14:27:15"
    }
  ]
}
```

## Evidence Review

### Post-Execution Review

After all scenarios complete:

1. **Count Evidence:**
   - Total screenshots captured
   - Screenshots per scenario
   - Missing evidence

2. **Verify Quality:**
   - Screenshots clear and readable
   - Key elements visible
   - Timestamps present (if applicable)

3. **Check Completeness:**
   - All critical steps documented
   - All errors captured
   - All work unit IDs recorded

4. **Organize Results:**
   - results.json files complete
   - Folder structure correct
   - Naming convention followed

### Evidence Summary

Create summary document:

```markdown
# Test Execution Evidence Summary

**Client:** SONH
**Extension:** EXT_FIN_004
**Date:** 2026-03-06
**Total Scenarios:** 21

## Evidence Statistics

- Total Screenshots: 126 (6 per scenario average)
- Total Errors: 3
- Missing Evidence: 0

## Scenario Results

### Scenario 3.1: Garnishment auto-approved
- Status: Passed ✅
- Screenshots: 6
- Work Unit: WU123456
- Evidence: Projects/SONH/Temp/evidence/3.1/

### Scenario 3.2: Employee invoice approved by BOA
- Status: Passed ✅
- Screenshots: 7
- Work Unit: WU123457
- Evidence: Projects/SONH/Temp/evidence/3.2/

[... continue for all scenarios ...]

## Errors Encountered

### Error 1: Vendor not found
- Scenario: 3.4
- Type: UI Error
- Message: "Vendor not found: V12345"
- Screenshot: Projects/SONH/Temp/evidence/3.4/error_vendor_not_found.png

[... continue for all errors ...]
```

## Evidence Retention

### Storage Duration

**Active Testing:** Keep evidence for duration of testing cycle

**Completed Testing:** Archive evidence for 90 days

**Failed Tests:** Keep evidence until issue resolved

### Cleanup

**After Successful Test Cycle:**
1. Archive evidence to compressed folder
2. Move to archive directory
3. Delete from Temp/ after archival

**After Failed Tests:**
1. Keep evidence in Temp/ for investigation
2. Don't delete until issue resolved
3. Archive after resolution

## Security Considerations

### Sensitive Data

**Screenshots may contain:**
- Vendor names
- Invoice amounts
- Employee information
- Account numbers
- Approval names

**Protection:**
- Don't commit evidence to git
- Store in Temp/ directory (gitignored)
- Limit access to authorized personnel
- Delete after retention period

### Credential Protection

**NEVER capture screenshots of:**
- Login credentials
- Password fields
- API keys
- Tokens
- Session IDs

**If accidentally captured:**
1. Delete screenshot immediately
2. Regenerate credentials
3. Document incident

## Best Practices

### Timing

- **Capture after action completes** - Don't capture mid-action
- **Wait for page load** - Ensure page fully rendered
- **Verify visibility** - Check key elements visible

### Quality

- **Clear screenshots** - Readable text, visible elements
- **Appropriate size** - Full page for context, element for details
- **Consistent format** - PNG for all screenshots

### Organization

- **Consistent naming** - Follow naming convention
- **Logical ordering** - Sequential step numbers
- **Complete documentation** - results.json for each scenario

### Efficiency

- **Capture only necessary** - Don't over-capture
- **Reuse evidence** - Don't duplicate screenshots
- **Clean up regularly** - Remove old evidence

## Common Issues

### Issue: Screenshot blank or incomplete

**Cause:** Page not fully loaded

**Solution:**
- Wait for page load before capturing
- Use `wait_for` to ensure elements present
- Increase wait time if needed

### Issue: Screenshot too large

**Cause:** Full page screenshot of long page

**Solution:**
- Capture element instead of full page
- Crop to relevant section
- Compress PNG if needed

### Issue: Evidence folder not created

**Cause:** Folder creation failed or path incorrect

**Solution:**
- Verify path is correct
- Check permissions
- Create folder manually if needed

### Issue: Screenshots not saving

**Cause:** Disk space, permissions, or path issues

**Solution:**
- Check disk space available
- Verify write permissions
- Check path exists and is writable

## Related Files

- `test-execution.md` - Test execution workflow
- `tes070-parsing.md` - TES-070 parsing workflow
- `fsm-navigation.md` - FSM navigation patterns
