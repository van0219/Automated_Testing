# FSM Selectors Discovered

## Summary

Successfully logged into FSM and discovered the actual selectors for the Payables workflow.

## Key Findings

### 1. FSM Uses an Iframe

All FSM content loads inside an iframe with name pattern: `iframe[name^="fsm_"]`

This means all selectors must target elements within this iframe using Playwright's `frame_locator()`.

### 2. My Available Applications Page

The "My Available Applications" page contains many application tiles including:
- Application Administration
- Administration Console
- Approver
- Assets
- Billing
- Cash
- **Payables** ← Found it!
- Process Server Administrator
- And many more...

### 3. Payables Tile Selector

The Payables tile contains the text:
- **"Payables"** (heading)
- **"Setup, Process Invoices, Process Payments, Manage Vendors"** (description)

**Working selector:**
```python
iframe = page.frame_locator('iframe[name^="fsm_"]')
payables_tile = iframe.get_by_text("Payables Setup, Process", exact=False)
payables_tile.click()
```

### 4. Payables Page Elements

Once in Payables, the page shows:
- **"Create Invoice"** button (top right)
- **"Create and Release"** button
- Search filters (Company, Vendor, Invoice Number, etc.)
- Invoice grid/table

**Create Invoice button selector:**
```python
iframe = page.frame_locator('iframe[name^="fsm_"]')
create_button = iframe.get_by_role("button", name="Create Invoice")
```

## Updated Files

1. **pages/payables_page.py**
   - Updated `navigate_to_payables()` to use iframe and correct text selector
   - Updated `create_invoice()` to use iframe

## Testing

The selectors have been updated in the page objects. The test should now work correctly.

## Next Steps

Run the test again:
```bash
cd fsm-automation
python -m pytest tests/approvals/test_ext_fin_004.py -v
```

The test should now successfully:
1. ✅ Login to FSM
2. ✅ Navigate to Payables (using discovered selectors)
3. ⏳ Create invoice (needs form field selectors)
4. ⏳ Submit for approval
5. ⏳ Verify work unit

## Notes

- FSM loads content in iframes, so all interactions must use `frame_locator()`
- The iframe name changes per session, so use pattern matching: `iframe[name^="fsm_"]`
- Playwright's semantic selectors (`get_by_role`, `get_by_text`) work well within iframes
