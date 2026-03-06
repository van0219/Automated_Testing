# FSM Iframe Navigation Fix

## Date: March 6, 2026

## Problem

The approval testing framework was getting stuck on "My Available Applications" page and couldn't navigate to Payables or interact with FSM content.

## Root Cause

ALL FSM content is embedded inside an **iframe**, not in the main page DOM. The framework was trying to interact with elements on the main page, which failed because the elements were actually inside the iframe.

## Solution

Updated `ReusableTools/testing_framework/actions/fsm/fsm_payables.py` to:

### 1. Iframe Detection and Access

```python
# Get iframe using frame_locator
iframe = self.playwright.page.frame_locator('iframe[name^="fsm_"]')
```

### 2. Two Navigation Scenarios

**Scenario A: Payables NOT Preferred (First Time)**
- User sees "My Available Applications" page
- Must click "More - Payables" button
- Optional confirmation dialog appears
- Payables loads after 10 seconds

**Scenario B: Payables IS Preferred**
- Payables loads automatically after login
- No navigation needed
- Detect by looking for "Create Invoice" button

### 3. Detection Logic

```python
# Check if already on Payables (Scenario B)
try:
    create_invoice_btn = iframe.get_by_role('button', name='Create Invoice')
    if create_invoice_btn.is_visible(timeout=3000):
        # Already on Payables - no navigation needed
        return success
except:
    pass

# Check if on "My Available Applications" (Scenario A)
try:
    my_apps_heading = iframe.get_by_role('heading', name='My Available Applications')
    if my_apps_heading.is_visible(timeout=3000):
        # Navigate to Payables
        payables_btn = iframe.get_by_role('button', name='More - Payables')
        payables_btn.click()
        
        # Handle optional confirmation dialog
        try:
            ok_btn = iframe.get_by_role('button', name='Ok')
            if ok_btn.is_visible(timeout=5000):
                ok_btn.click()
        except:
            pass  # Dialog didn't appear
        
        # Wait for Payables to load
        wait_for_timeout(10000)
except:
    raise ActionError("Unknown FSM page state")
```

### 4. Updated All FSM Interactions

All methods now use iframe locator:

- `navigate_to_payables()` - Iframe-aware navigation with dual scenario support
- `create_expense_invoice()` - Gets iframe, passes to helper methods
- `_fill_invoice_header()` - Uses iframe.get_by_label() for fields
- `_set_approval_routing()` - Uses iframe.get_by_label()
- `_save_invoice()` - Uses iframe.get_by_role('button', name='Save')
- `submit_for_approval()` - Uses iframe.get_by_role('button', name='Submit for Approval')

### 5. Changed to Role-Based Selectors

Replaced CSS selectors with role-based selectors (more reliable):

**Before:**
```python
self.playwright.click('button:has-text("Create Invoice")')
```

**After:**
```python
create_btn = iframe.get_by_role('button', name='Create Invoice')
create_btn.click()
```

### 6. Proper Wait Times

- After login: 8 seconds (wait for iframe to load)
- After clicking Payables: 10 seconds (wait for Payables to load)
- After form actions: 3 seconds (wait for save/submit)

## Files Modified

- `ReusableTools/testing_framework/actions/fsm/fsm_payables.py` - Complete rewrite with iframe support

## Testing

The framework should now:

1. Login successfully
2. Wait for FSM iframe to load (8 seconds)
3. Detect which scenario (A or B)
4. Navigate to Payables if needed (Scenario A)
5. Interact with all FSM elements inside iframe
6. Create invoices, submit for approval, etc.

## Next Steps

1. Test the updated framework with approval scenarios
2. Verify both navigation scenarios work (A and B)
3. Update `fsm_workunits.py` if it also needs iframe support
4. Document any additional FSM pages that need iframe support

## Key Takeaways

- ALWAYS check if content is in an iframe before trying to interact
- Use `page.frame_locator()` to access iframe content
- Use role-based selectors (more reliable than CSS)
- Handle multiple navigation scenarios (tenant-specific settings)
- Use proper wait times (FSM is slow to load)
