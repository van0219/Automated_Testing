# FSM Role Switcher Learning - Documentation Updated

**Date**: 2026-03-10

## What Was Updated

### 1. Steering File: `.kiro/steering/01_FSM_Navigation_Guide.md`

Added **Rule 0: FSM Role Switcher (CRITICAL)** as the first rule in the Critical Rules section.

### Key Learning Documented

**FSM roles are NOT separate applications** - they are accessed via a dropdown switcher in the FSM header.

**Role Switcher Pattern**:
- Located in FSM iframe header
- Format: `combobox "[RoleName], [RoleName]"`
- Click to open dropdown showing all available roles
- Select desired role from listbox
- Wait for interface to update

**Common Roles**:
- Payables
- Global Ledger  
- Staff Accountant
- Process Server Administrator
- Integration Architect
- Receivables
- Cash
- Assets
- Purchasing
- Requester

### Critical Clarification

When TES-070 test steps say "Log in as [Role]":
- ✅ Use role switcher dropdown to change roles
- ❌ Do NOT logout and login again

## Browser Automation Pattern

```javascript
// 1. Snapshot to find role switcher
await mcp_playwright_browser_snapshot();

// 2. Click combobox (e.g., "Payables, Payables")
await mcp_playwright_browser_click({ ref: "role_switcher_ref" });

// 3. Wait for dropdown
await page.waitForTimeout(1000);

// 4. Snapshot to see roles
await mcp_playwright_browser_snapshot();

// 5. Click desired role
await mcp_playwright_browser_click({ ref: "target_role_ref" });

// 6. Wait for role to load
await mcp_playwright_browser_click({ ref: "target_role_ref" });

// 6. Wait for role to load
await page.waitForTimeout(3000);
```

## Impact on Testing

This learning is critical for:
- EXT_FIN_001 (Manual Journal Entry) - Requires Staff Accountant or Global Ledger role
- EXT_FIN_004 (Expense Invoice) - Requires Payables role
- Any test requiring role switching

## Next Steps

1. ✅ Steering file updated
2. ✅ Learning documented
3. ⏭️ Ready to proceed with Scenario 3.1 test execution
4. ⏭️ Switch to Global Ledger or Staff Accountant role
5. ⏭️ Navigate to Process Journals > Create
6. ⏭️ Create manual journal with amount < $1,000
7. ⏭️ Submit for approval

## Files Updated

- `.kiro/steering/01_FSM_Navigation_Guide.md` - Added Rule 0 about role switcher
- `FSM_ROLE_SWITCHER_LEARNING.md` - Initial learning capture
- `ROLE_SWITCHER_UPDATE_COMPLETE.md` - This summary document
