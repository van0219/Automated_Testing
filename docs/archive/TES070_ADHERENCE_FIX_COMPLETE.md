# TES-070 Exact Adherence Fix - Complete

## Date: 2026-03-10

## Problem Identified

Agent was NOT following TES-070 test steps exactly as written. Instead:
- Interpreting steps and creating own actions
- Substituting similar values (e.g., "Global Ledger" instead of "Staff Accountant")
- Deviating from specified workflow
- Making assumptions about what steps mean

## Root Cause

Power steering file `test-execution.md` said:
> "Read test step descriptions (human-readable) and translate to browser actions"

This instruction was TOO VAGUE and gave agent permission to INTERPRET rather than FOLLOW EXACTLY.

## Files Updated

### 1. .kiro/powers/fsm-approval-testing/POWER.md

Added CRITICAL RULE section at top of Workflow:

```markdown
## CRITICAL RULE: EXACT TES-070 ADHERENCE ⚠️

**YOU MUST FOLLOW TES-070 TEST STEPS EXACTLY AS WRITTEN. DO NOT INTERPRET. DO NOT DEVIATE. DO NOT CREATE YOUR OWN STEPS.**

The TES-070 document contains the EXACT test steps that must be executed. Every word is a requirement, not a suggestion.
```

Includes:
- Examples of exact adherence
- What this means (5 rules)
- What NOT to do (6 anti-patterns)
- Validation after each step

### 2. .kiro/powers/fsm-approval-testing/steering/test-execution.md

Replaced section "4.2 Interpret Test Steps" with "4.2 Follow Test Steps EXACTLY (CRITICAL)":

Key changes:
- Removed "interpret" and "translate" language
- Added explicit "DO NOT interpret" instruction
- Added detailed examples of CORRECT vs INCORRECT execution
- Added atomic action parsing instructions
- Added validation checkpoint section (4.3)

### 3. .kiro/steering/00_Index.md

Updated Phase 3 workflow description:
- Added CRITICAL note about exact adherence
- Added specific examples (Staff Accountant, Process Journals, amounts)
- Added validation requirement
- Added "STOP if validation fails" instruction

### 4. Documentation Files Created

- `CRITICAL_ISSUE_TES070_STEP_ADHERENCE.md` - Detailed issue analysis
- `TES070_ADHERENCE_FIX_COMPLETE.md` - This summary document

## Key Changes Summary

### Before:
- "Interpret test steps"
- "Translate to browser actions"
- Agent had freedom to substitute similar values
- No validation checkpoints

### After:
- "Follow test steps EXACTLY"
- "DO NOT interpret"
- Agent must use exact values from TES-070
- Validation after each step
- STOP if validation fails

## Examples Added

### Example 1: Role Selection

**TES-070 says:** "Log In as Staff Accountant role"

**CORRECT:**
1. Take snapshot
2. Find role dropdown
3. Click dropdown
4. Find "Staff Accountant" option
5. Click "Staff Accountant"
6. Verify "Staff Accountant" is selected
7. Take screenshot

**INCORRECT:**
- Assume "Global Ledger" is similar enough ❌
- Skip role switch because already logged in ❌
- Use any role that has journal access ❌

### Example 2: Navigation Path

**TES-070 says:** "Process Journals > Create"

**CORRECT:**
- Navigate to "Process Journals" menu
- Click "Create" option

**INCORRECT:**
- Navigate to "Journals" menu ❌
- Navigate to "Create Journal" directly ❌
- Use any menu that creates journals ❌

### Example 3: Amount Values

**TES-070 says:** "amount below $1,000"

**CORRECT:**
- Use $999.99 or $500.00 or $750.00

**INCORRECT:**
- Use $1,000 (not below) ❌
- Use $1,500 (not below) ❌
- Use any amount that seems reasonable ❌

## Validation Checkpoints Added

After each TES-070 step:
1. Verify action completed successfully
2. Verify result matches TES-070 expectation
3. Take screenshot for evidence
4. If validation fails, STOP and document

Example validation:
- TES-070 says: "status turns to Pending Approval"
- Agent must: Extract status value, verify = "Pending Approval", STOP if not matching

## Testing Required

Before considering this fix complete:

1. ✅ Documentation updated
2. ✅ Power POWER.md updated
3. ✅ Steering file test-execution.md updated
4. ✅ Workspace index 00_Index.md updated
5. ⏳ Re-run EXT_FIN_001 Scenario 3.1 from beginning
6. ⏳ Verify agent switches to "Staff Accountant" role (not "Global Ledger")
7. ⏳ Verify agent navigates to "Process Journals" > "Create" (exact path)
8. ⏳ Verify agent creates journal with amount < $1,000
9. ⏳ Verify agent releases transaction
10. ⏳ Verify status = "Pending Approval"
11. ⏳ Complete all 6 steps from Scenario 3.1

## Impact

### Positive:
- Agent will now follow TES-070 steps exactly
- Test execution will match documented workflow
- Evidence will be valid for regression testing
- Reduced need for user intervention
- Clear validation checkpoints prevent drift

### Potential Issues:
- Agent may fail if TES-070 steps are ambiguous
- Agent may fail if FSM UI doesn't match TES-070 expectations
- Agent may need more explicit instructions for complex steps

## Lessons Learned

1. **Vague instructions enable interpretation** - "Translate" gave too much freedom
2. **Explicit constraints prevent deviation** - "DO NOT interpret" is clear
3. **Examples clarify expectations** - CORRECT vs INCORRECT patterns help
4. **Validation checkpoints catch errors early** - Stop before cascading failures
5. **TES-070 is the contract** - Every word is a requirement, not a suggestion

## Next Steps

1. User should re-run EXT_FIN_001 Scenario 3.1 from beginning
2. Monitor agent behavior for exact adherence
3. Verify all validation checkpoints work
4. Document any remaining issues
5. If successful, proceed with remaining scenarios

## Related Files

- `.kiro/powers/fsm-approval-testing/POWER.md` - Power documentation (UPDATED)
- `.kiro/powers/fsm-approval-testing/steering/test-execution.md` - Test execution workflow (UPDATED)
- `.kiro/steering/00_Index.md` - Workspace overview (UPDATED)
- `CRITICAL_ISSUE_TES070_STEP_ADHERENCE.md` - Detailed issue analysis (NEW)

## Status

**COMPLETE** - Documentation and power files updated with exact adherence requirements.

**READY FOR TESTING** - User can now re-run EXT_FIN_001 Scenario 3.1 to verify fix.

## Priority

**CRITICAL** - This was a blocking issue that prevented the power from being usable for regression testing. Fix is now in place and ready for validation.


---

## IMPORTANT CLARIFICATION: Testing Modes

### User Feedback (2026-03-10)

The TES-070 exact adherence requirement applies ONLY to **REGRESSION TESTING** with existing TES-070 documents.

For **NET NEW TESTING** (testing new functionality with generic test scripts from functional consultants):
- No detailed TES-070 document exists
- Test scripts have high-level scenarios and few/incomplete steps
- Agent SHOULD use knowledge and instincts to execute tests
- Agent SHOULD interpret scenario objectives and create appropriate test steps
- Agent SHOULD adapt to FSM UI and make reasonable decisions

### Two Testing Modes

**Mode 1: Regression Testing (EXACT ADHERENCE)**
- Existing TES-070 with detailed steps
- Follow steps exactly as written
- No interpretation, no deviation
- Purpose: Verify existing functionality still works

**Mode 2: Net New Testing (ADAPTIVE EXECUTION)**
- Generic test script with objectives
- Use FSM knowledge to achieve objectives
- Interpret and adapt as needed
- Purpose: Test new functionality, create initial documentation

### Documentation Updated

All files now distinguish between these two modes:
- `.kiro/powers/fsm-approval-testing/POWER.md` - Added "Testing Modes" section
- `.kiro/powers/fsm-approval-testing/steering/test-execution.md` - Added mode distinction
- `.kiro/steering/00_Index.md` - Added mode notes in workflow

### Key Takeaway

The fix ensures agent:
1. Follows TES-070 exactly for regression testing
2. Uses judgment and adaptation for net new testing
3. Distinguishes between these modes appropriately
