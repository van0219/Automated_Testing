# FSM Role Switcher - Critical Learning

**Date**: 2026-03-10

## Key Discovery

FSM roles are NOT separate workspaces or applications. They are accessed via a **role switcher dropdown** within the FSM application interface.

## Role Switcher Location

- Located in the FSM header area (top of iframe)
- Appears as a dropdown/combobox showing current role
- Format: `[RoleName], [RoleName]` (e.g., "Payables, Payables")
- Element reference pattern: `combobox "[RoleName], [RoleName]"`

## Available Roles

Common FSM roles include:
- **Payables** - Invoice management, vendor payments
- **Staff Accountant** - Manual journal entry, GL transactions
- **Process Server Administrator** - IPA management, work units
- **Integration Architect** - CIS interfaces
- **Controller** - Financial oversight
- **Inventory Manager** - Inventory operations
- **Buyer** - Purchasing operations

## How to Switch Roles

1. Locate the role switcher dropdown in FSM header
2. Click the dropdown to open role list
3. Select desired role from list
4. FSM interface updates to show role-specific menus and functions

## Navigation Pattern

```
FSM Application (iframe)
  └── Role Switcher Dropdown (header)
      ├── Payables
      ├── Staff Accountant
      ├── Process Server Administrator
      └── [Other roles...]
```

## Important Notes

- Roles determine available menus and functions
- Each role has different navigation options
- Must switch to appropriate role before performing role-specific tasks
- Role switcher is WITHIN the FSM iframe, not in portal navigation

## Test Scenario Impact

For Manual Journal Entry approval testing (EXT_FIN_001):
- Test step says "Log In as Staff Accountant role"
- This means: Switch to Staff Accountant role using role switcher
- NOT: Login again or navigate to different application

## Browser Automation

When automating with Playwright:
- Work within FSM iframe
- Locate role switcher combobox
- Click to open dropdown
- Select target role from list
- Wait for interface to update
