# TES-070 Value Usage Update

**Date**: 2026-03-10
**Purpose**: Clarify that regression testing should use TES-070 values directly without asking user

## Problem

During regression testing, the agent was asking users for values that were already specified in the TES-070 document (accounts, vendors, amounts, codes, etc.). This created unnecessary friction and slowed down testing.

## Solution

Updated power and steering files to clarify:
- **Use TES-070 values directly** - Don't ask user for values that are in the document
- **ONLY ask user if there's an issue** - FSM error, invalid value, missing required field

## Files Updated

### 1. .kiro/powers/fsm-approval-testing/steering/test-execution.md

Added new section "CRITICAL: Use TES-070 Values - Don't Ask User" in section 4.2:

```markdown
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
```

**Examples Added:**
- ✅ CORRECT: Use values from TES-070 without asking
- ❌ INCORRECT: Ask user for values that are in TES-070
- ✅ CORRECT (Error Handling): Ask user only when FSM rejects a value

### 2. .kiro/powers/fsm-approval-testing/POWER.md

Updated Phase 3 section to include:

```markdown
**CRITICAL: Use TES-070 Values - Don't Ask User**

For regression testing, the TES-070 document contains ALL the values you need 
(accounts, vendors, amounts, codes, etc.). Use these values directly without 
asking the user.

**ONLY ask the user if:**
- A TES-070 value causes an FSM error (e.g., "Account 12345 is invalid")
- A required field is not specified in TES-070
- You encounter an unexpected validation error
```

### 3. .kiro/steering/00_Index.md

Updated Phase 3 workflow to include:

```markdown
- **CRITICAL**: Use TES-070 values directly (accounts, vendors, amounts, codes) 
  - ONLY ask user if FSM rejects a value or shows an error
```

Added specific examples:
- If TES-070 says "Account 6010-100-1000" → Use that exact account (don't ask user)
- If TES-070 says "Vendor V12345" → Use that exact vendor (don't ask user)

## Impact

**Before:**
- Agent asks: "What account should I use?"
- Agent asks: "What vendor should I use?"
- Agent asks: "What amount should I use?"
- User has to provide values that are already in TES-070

**After:**
- Agent reads TES-070: "Account 6010-100-1000"
- Agent uses: Account = "6010-100-1000"
- Agent only asks if FSM shows error: "Account 6010-100-1000 is invalid"

## Benefits

1. **Faster testing** - No unnecessary user interaction
2. **True regression testing** - Uses exact values from original test
3. **Better user experience** - User doesn't have to repeat what's in document
4. **Clear error handling** - User only involved when there's an actual issue

## Testing Mode Distinction

This guidance applies to **REGRESSION TESTING** mode only:
- Existing TES-070 document with detailed steps
- Use exact values from document
- Only ask user if FSM rejects a value

For **NET NEW TESTING** mode:
- Generic test scripts without detailed TES-070
- Agent uses judgment to create appropriate values
- May ask user for guidance on business rules

## Related Files

- `.kiro/powers/fsm-approval-testing/steering/test-execution.md` - Test execution workflow (UPDATED)
- `.kiro/powers/fsm-approval-testing/POWER.md` - Power documentation (UPDATED)
- `.kiro/steering/00_Index.md` - Workspace overview (UPDATED)

## Next Steps

When executing regression tests:
1. Read TES-070 document carefully
2. Extract all values (accounts, vendors, amounts, codes)
3. Use these values directly in test execution
4. Only ask user if FSM shows an error or validation issue
5. Document any issues encountered

## Summary

The power now clearly distinguishes between:
- **Using TES-070 values** (default behavior for regression testing)
- **Asking user** (only when there's an actual issue)

This makes regression testing more efficient and aligns with the principle that TES-070 documents are the source of truth for test execution.
