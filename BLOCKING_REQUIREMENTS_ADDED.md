# Blocking Requirements Added to Approval Hooks

## Summary

Added blocking requirements to all three approval workflow hooks to enforce complete execution without shortcuts or "simpler versions" for real-world automation testing.

## Updated Files

### Hooks Updated

1. **`.kiro/hooks/approval-step1-parse-tes070.kiro.hook`**
   - Added blocking requirement at the beginning of the prompt
   - Enforces: MUST generate COMPLETE JSON with ALL scenarios
   - Prohibits: "simpler versions", partial implementations, manual completion suggestions

2. **`.kiro/hooks/approval-step2-execute-tests.kiro.hook`**
   - Added blocking requirement at the beginning of the prompt
   - Enforces: MUST execute ALL scenarios from JSON file
   - Prohibits: Skipping scenarios, simplified execution, manual execution suggestions

3. **`.kiro/hooks/approval-step3-generate-tes070.kiro.hook`**
   - Added blocking requirement at the beginning of the prompt
   - Enforces: MUST provide complete review guidance
   - Prohibits: Simplified review steps, incomplete review suggestions

### Steering Files Updated

1. **`.kiro/steering/00_Index.md`**
   - Updated "Approval Testing (3 steps)" section
   - Added blocking requirement notes for each step
   - Clarifies expectations for complete execution

2. **`.kiro/steering/10_JSON_Generation_Best_Practices.md`**
   - Added new section: "Critical Rule: Complete Generation Required"
   - Explains why complete generation matters for automation
   - Provides clear guidance on what to do if completion is not possible

## Blocking Requirement Text

All hooks now include this critical requirement at the start:

```
**BLOCKING REQUIREMENT - MUST COMPLETE FULLY:**
This is REAL-WORLD automation testing. You MUST [complete the specific task]. 
DO NOT create "simpler versions" or [skip/partial implementations]. 
DO NOT suggest manual [completion/execution]. 
The entire purpose of this automation is to eliminate manual work. 
If you cannot complete the full task, STOP and explain why, 
but DO NOT proceed with incomplete solutions.
```

## Impact

### Before
- AI might generate partial JSON files with 5 scenarios instead of 21
- AI might suggest "you can add the rest manually"
- AI might skip scenarios during execution
- AI might provide simplified review guidance

### After
- AI MUST generate complete JSON files with all scenarios
- AI MUST execute all scenarios without skipping
- AI MUST provide complete review guidance
- AI will STOP and explain if it cannot complete, rather than providing incomplete solutions

## Purpose

These blocking requirements ensure that:
1. **Real-world automation** - Files are production-ready, not prototypes
2. **No manual work** - Automation eliminates manual completion
3. **Quality assurance** - Complete execution ensures thorough testing
4. **Consistency** - All scenarios tested every time
5. **Documentation** - Complete TES-070 documents generated

## Testing

To verify the blocking requirements work:
1. Run "Approval Step 1: Parse TES-070 Document"
2. Select a TES-070 with 21 scenarios
3. Verify AI generates complete JSON with all 21 scenarios
4. No suggestions for manual completion
5. Complete file ready for framework execution

## Date

March 5, 2026

## Related Documents

- `APPROVAL_HOOKS_UPDATED.md` - Original hook update documentation
- `FRAMEWORK_INTEGRATION_COMPLETE.md` - Framework integration details
- `.kiro/steering/00_Index.md` - Main steering file with workflow overview
