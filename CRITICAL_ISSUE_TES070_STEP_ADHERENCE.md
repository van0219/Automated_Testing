# CRITICAL ISSUE: Not Following TES-070 Steps Exactly

## Date: 2026-03-10

## Issue Description

The agent is NOT following the exact test steps provided in TES-070 documents. Instead, the agent is:
- Interpreting steps and creating its own actions
- Deviating from the specified workflow
- Making assumptions about what steps mean
- Not executing steps in the exact order specified

## Example Failure

**TES-070 Document**: EXT_FIN_001 - Manual Journal Entry Approval
**Scenario**: 3.1

**TES-070 Step 1 Says:**
```
Log In as Staff Accountant role. 
Process Journals>Create
Create Manual Journal with total functional debit amount below $1,000 and release the transaction.

The status of the transaction turns to Pending Approval.
```

**What Agent Did:**
1. Logged into FSM portal ✅
2. Switched to "Global Ledger" role ❌ (WRONG - should be "Staff Accountant")
3. Started trying to navigate without following exact path ❌

**What Agent Should Have Done:**
1. Log into FSM portal ✅
2. Switch to "Staff Accountant" role (use role dropdown) ✅
3. Navigate to "Process Journals" > "Create" (exact path from TES-070) ✅
4. Create Manual Journal with amount < $1,000 ✅
5. Release the transaction ✅
6. Verify status = "Pending Approval" ✅

## Root Cause

The power steering file `test-execution.md` says:

> "Read test step descriptions (human-readable) and translate to browser actions"

This instruction is TOO VAGUE and gives the agent permission to INTERPRET rather than FOLLOW EXACTLY.

## Impact

- Test execution does not match TES-070 document
- Evidence collected does not match expected workflow
- Test results are invalid
- Cannot be used for regression testing
- Wastes time with incorrect navigation
- User has to stop and correct agent repeatedly

## Required Fix

### 1. Update Power POWER.md

Add CRITICAL RULE at the top of workflow section:

```markdown
## CRITICAL RULE: EXACT TES-070 ADHERENCE

**YOU MUST FOLLOW TES-070 TEST STEPS EXACTLY AS WRITTEN. DO NOT INTERPRET. DO NOT DEVIATE.**

- If TES-070 says "Log In as Staff Accountant role" → Switch to "Staff Accountant" role (NOT "Global Ledger" or any other role)
- If TES-070 says "Process Journals > Create" → Navigate to exactly "Process Journals" then "Create" (NOT "Journals" or similar)
- If TES-070 says "amount below $1,000" → Use amount like $999.99 or $500.00 (NOT $1,000 or $1,500)
- If TES-070 says "event code not equal to TR and BOA" → Use event code like "GE" or "AD" (NOT "TR" or "BOA")

**Every word in the TES-070 step is a requirement. Follow it exactly.**
```

### 2. Update Steering File test-execution.md

Replace section "4.2 Interpret Test Steps" with:

```markdown
#### 4.2 Follow Test Steps EXACTLY

**CRITICAL**: DO NOT interpret or translate test steps. Follow them EXACTLY as written in the TES-070 document.

**TES-070 Step Format:**
```
Step 1: Log In as Staff Accountant role. 
Process Journals>Create
Create Manual Journal with total functional debit amount below $1,000 and release the transaction.

The status of the transaction turns to Pending Approval.
```

**How to Execute:**

1. **Parse the step into atomic actions:**
   - "Log In as Staff Accountant role" → Switch to "Staff Accountant" role using role dropdown
   - "Process Journals>Create" → Navigate to "Process Journals" menu, then click "Create"
   - "Create Manual Journal" → Fill form with required fields
   - "total functional debit amount below $1,000" → Use amount like $999.99 or $500.00
   - "release the transaction" → Click "Release" button
   - "status turns to Pending Approval" → Verify status field shows "Pending Approval"

2. **Execute each atomic action in order:**
   - Take snapshot (find elements)
   - Execute action with exact parameters from TES-070
   - Verify result matches TES-070 expectation
   - Take screenshot (evidence)
   - Move to next action

3. **DO NOT:**
   - Substitute similar roles (e.g., "Global Ledger" instead of "Staff Accountant")
   - Use similar navigation paths (e.g., "Journals" instead of "Process Journals")
   - Change amounts or values (e.g., $1,000 instead of < $1,000)
   - Skip steps or combine steps
   - Add extra steps not in TES-070

**Example - CORRECT Execution:**

TES-070 says: "Log In as Staff Accountant role"
Agent does: 
1. Take snapshot
2. Find role dropdown (combobox showing current role)
3. Click role dropdown
4. Find "Staff Accountant" option
5. Click "Staff Accountant"
6. Wait for role to load
7. Take screenshot (evidence of Staff Accountant role)

**Example - INCORRECT Execution:**

TES-070 says: "Log In as Staff Accountant role"
Agent does:
1. Take snapshot
2. See "Global Ledger" role is already selected
3. Assume "Global Ledger" has journal functionality
4. Continue without switching roles ❌ WRONG

**The TES-070 document is the source of truth. Every word matters. Follow it exactly.**
```

### 3. Add Validation Checkpoint

After each step execution, add validation:

```markdown
#### 4.3 Validate Step Completion

After executing each step, verify:

1. **Action completed successfully** - No errors, expected element appeared
2. **Result matches TES-070 expectation** - Status changed, form saved, etc.
3. **Ready for next step** - Page loaded, elements visible

If validation fails:
- Take screenshot of current state
- Document what was expected vs what happened
- Reference TES-070 step number
- Stop scenario execution (don't continue with invalid state)
```

## Testing After Fix

1. Re-run EXT_FIN_001 Scenario 3.1 from beginning
2. Verify agent switches to "Staff Accountant" role (not "Global Ledger")
3. Verify agent navigates to "Process Journals" > "Create" (exact path)
4. Verify agent creates journal with amount < $1,000
5. Verify agent releases transaction
6. Verify status = "Pending Approval"
7. Complete all 6 steps from Scenario 3.1

## Lessons Learned

1. **Vague instructions lead to interpretation** - "Translate to browser actions" gave agent too much freedom
2. **TES-070 is the contract** - Every word is a requirement, not a suggestion
3. **Exact adherence is critical** - Regression testing requires exact reproduction of test steps
4. **Validation checkpoints prevent drift** - Verify each step before continuing
5. **Clear examples prevent mistakes** - Show correct vs incorrect execution patterns

## Related Files

- `powers/fsm-approval-testing/POWER.md` - Power documentation (needs update)
- `powers/fsm-approval-testing/steering/test-execution.md` - Test execution workflow (needs update)
- `.kiro/steering/00_Index.md` - Workspace overview (may need update)

## Status

- [ ] Update POWER.md with CRITICAL RULE
- [ ] Update test-execution.md with exact adherence instructions
- [ ] Add validation checkpoint section
- [ ] Test with EXT_FIN_001 Scenario 3.1
- [ ] Verify agent follows exact steps
- [ ] Document successful test execution

## Priority

**CRITICAL** - This issue prevents the power from being usable for regression testing. Must be fixed before any further test execution.


---

## Testing Modes Clarification

### Mode 1: Regression Testing (EXACT ADHERENCE)

**When**: Testing with existing TES-070 documents that have detailed test steps

**Rule**: Follow TES-070 steps EXACTLY - no interpretation, no deviation

**Example**: TES-070 says "Log In as Staff Accountant role" → Must use "Staff Accountant" role

### Mode 2: Net New Testing (ADAPTIVE EXECUTION)

**When**: Testing new functionality with generic test scripts from functional consultants

**Rule**: Use knowledge and instincts to execute tests based on scenario objectives

**Example**: Test script says "Test journal approval under $1,000" → Agent determines appropriate role, navigation, values

### Key Difference

- **Regression**: TES-070 provides exact steps → Follow exactly
- **Net New**: Test script provides objectives → Use judgment to achieve objectives

The fix ensures agent distinguishes between these modes and applies appropriate execution strategy.
