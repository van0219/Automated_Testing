# Consolidated Approval Regression Testing Workflow

## Date: March 6, 2026
## Updated: March 6, 2026 - Added Intelligent Agent Routing

## Overview

Replaced the 3-step approval workflow with ONE consolidated hook that uses **intelligent agent routing** to automatically select the appropriate specialized subagent based on transaction type detected in the TES-070 document.

## Architecture

### Universal Hook
**Hook**: "Run FSM Approval Regression Tests"
- Single entry point for ALL FSM approval workflows
- Parses TES-070 to detect transaction type
- Routes to appropriate specialized subagent
- Validates subagent exists before execution

### Intelligent Agent Routing
The hook automatically detects the transaction type and routes to the correct agent:

| Transaction Type | FSM Module | Subagent | Status |
|-----------------|------------|----------|--------|
| ExpenseInvoice | Payables | invoice-approval-test-agent | ✅ Created |
| ManualJournal | General Ledger | journal-approval-test-agent | ❌ Not yet created |
| CashLedgerTransaction | Cash Management | cash-approval-test-agent | ❌ Not yet created |

## Old Workflow (3 Hooks)

1. **Approval Step 1**: Parse TES-070 → Generate JSON
2. **Approval Step 2**: Execute tests → Generate TES-070
3. **Approval Step 3**: Review TES-070

**Problems:**
- User must click 3 separate hooks
- Context lost between steps
- Credentials prompted multiple times
- Fragmented user experience

## New Workflow (1 Hook with Intelligent Routing)

**Hook**: "Run FSM Approval Regression Tests"

**Single Click Workflow:**
1. Select client (interactive)
2. Select TES-070 document (interactive)
3. Parse TES-070 and detect transaction type
4. Map transaction type to specialized subagent
5. Validate subagent exists (error if missing)
6. Check for existing JSON scenarios (reuse or regenerate)
7. Check for existing credentials (reuse or re-enter)
8. Invoke appropriate specialized subagent
9. Subagent executes tests autonomously
10. Subagent generates TES-070 report
11. Display final summary

## Intelligent Routing Logic

### Transaction Type Detection
The hook parses the TES-070 document and extracts:
- Transaction type (ExpenseInvoice, ManualJournal, CashLedgerTransaction)
- FSM module (Payables, General Ledger, Cash Management)
- Business class information

### Agent Mapping
```
ExpenseInvoice → invoice-approval-test-agent
ManualJournal → journal-approval-test-agent
CashLedgerTransaction → cash-approval-test-agent
```

### Validation
Before invoking the agent, the hook:
1. Checks if agent file exists in `.kiro/agents/`
2. If missing: Displays error with available agents
3. If exists: Proceeds with invocation

### Error Handling
If required agent doesn't exist:
```
ERROR: Transaction type 'ManualJournal' requires 'journal-approval-test-agent' 
which is not yet created.

Available agents:
- invoice-approval-test-agent (ExpenseInvoice)

Suggestions:
1. Create journal-approval-test-agent for ManualJournal workflows
2. Use a different TES-070 document (ExpenseInvoice type)
```

## Benefits

### User Experience
- ✅ One click instead of three
- ✅ Single conversation thread
- ✅ Context maintained throughout
- ✅ Credentials reused if available
- ✅ JSON scenarios reused if available
- ✅ Clear progress reporting
- ✅ Automatic agent routing based on transaction type
- ✅ Clear error messages if agent missing

### Technical
- ✅ Agent maintains full context
- ✅ No context loss between phases
- ✅ Autonomous execution
- ✅ Intelligent credential management
- ✅ Scenario reuse for efficiency
- ✅ Transaction type detection
- ✅ Specialized agents for each approval type
- ✅ Extensible architecture (add agents without changing hook)

### Workflow
- ✅ Interactive selection (client, document)
- ✅ Smart reuse (JSON, credentials)
- ✅ Intelligent routing (transaction type → agent)
- ✅ Validation (agent exists before execution)
- ✅ Autonomous testing (agent handles everything)
- ✅ Comprehensive reporting (final summary)

## Hook Location

`.kiro/hooks/run-approval-regression-tests.kiro.hook`

## How to Use

1. Click "Run FSM Approval Regression Tests" hook
2. Select client from list
3. Select TES-070 document from list
4. If JSON exists: Choose to reuse or regenerate
5. If credentials exist: Choose to reuse or re-enter
6. Agent executes autonomously
7. Review final summary and TES-070 report

## Agent Invocation

The hook invokes the `invoice-approval-test-agent` subagent with:

```
invokeSubAgent(
    name="invoice-approval-test-agent",
    prompt="Execute FSM approval regression tests with parameters...",
    explanation="Delegating approval test execution to specialized testing agent"
)
```

## Agent Responsibilities

The agent handles:
- Loading scenario JSON
- Initializing Playwright browser
- Logging into FSM
- Navigating to Payables/GL/Cash
- Creating transactions
- Submitting for approval
- Monitoring work units
- Validating status changes
- Capturing screenshots
- Generating TES-070 report

## Output Locations

- **TES-070 Report**: `Projects/{ClientName}/TES-070/Generated_TES070s/TES-070_{timestamp}_{extension_id}.docx`
- **Evidence**: `Projects/{ClientName}/Temp/evidence/{scenario_id}/`
- **JSON Scenarios**: `Projects/{ClientName}/TestScripts/approval/{extension_id}_auto_approval_test.json`
- **Credentials**: `Projects/{ClientName}/Credentials/.env.fsm` and `.env.passwords`

## Credential Management

### First Time
- Hook prompts for credentials
- Saves to Credentials/ folder
- Passes to agent

### Subsequent Runs
- Hook checks for existing credentials
- Asks user to reuse or re-enter
- Reuses if confirmed

### Security
- Credentials stored in gitignored folder
- Passwords never logged
- Passed securely to agent
- No sensitive data in evidence

## JSON Scenario Reuse

### First Time
- Hook parses TES-070
- Generates JSON scenarios
- Validates JSON
- Passes to agent

### Subsequent Runs
- Hook checks for existing JSON
- Asks user to reuse or regenerate
- Reuses if confirmed
- Saves time on repeated testing

## Comparison: Old vs New

| Aspect | Old (3 Hooks) | New (1 Hook) |
|--------|---------------|--------------|
| User Clicks | 3 | 1 |
| Context | Lost between steps | Maintained |
| Credential Prompts | 3 times | 1 time (or reuse) |
| JSON Generation | Every time | Reuse if exists |
| User Experience | Fragmented | Seamless |
| Execution Time | Longer (manual steps) | Faster (autonomous) |
| Error Handling | Per-step | End-to-end |
| Progress Visibility | Per-step | Real-time |

## Migration Path

### Keep Old Hooks?
**Recommendation**: Keep old hooks disabled for now, remove after testing new workflow.

**Reasoning**:
- New workflow is more efficient
- Old hooks can serve as backup
- Remove after confirming new workflow works

### Testing New Workflow
1. Test with SONH client
2. Verify all phases work
3. Confirm agent executes correctly
4. Check TES-070 generation
5. Validate evidence capture

### Rollback Plan
If new workflow has issues:
1. Disable new hook
2. Re-enable old hooks
3. Fix issues in new workflow
4. Test again

## Future Enhancements

### Possible Improvements
1. **Multi-Account Support**: Handle multiple FSM accounts for approval workflows
2. **Parallel Execution**: Run multiple scenarios in parallel (if safe)
3. **Smart Retry**: Retry failed scenarios automatically
4. **Email Notifications**: Send email when testing complete
5. **Slack Integration**: Post results to Slack channel
6. **Dashboard**: Web dashboard for test results
7. **Trend Analysis**: Track pass/fail rates over time

### Agent Enhancements
1. **AI Selector Recovery**: Use AI to find elements when selectors change
2. **Smart Waiting**: Adaptive wait times based on FSM response
3. **Error Classification**: Categorize errors (UI change, timeout, data issue)
4. **Self-Healing**: Attempt to fix common issues automatically
5. **Performance Metrics**: Track execution time per scenario

## Troubleshooting

### Hook Not Appearing
- Check `.kiro/hooks/` directory
- Verify JSON syntax
- Restart Kiro IDE

### Agent Not Invoked
- Check agent exists: `.kiro/agents/invoice-approval-test-agent.md`
- Verify agent name matches
- Check agent tools access

### Credentials Not Saved
- Check Credentials/ folder exists
- Verify write permissions
- Check .gitignore includes Credentials/

### JSON Not Generated
- Check TES-070 analyzer works
- Verify document format
- Check for parsing errors

### Tests Not Executing
- Check Playwright installed
- Verify FSM credentials correct
- Check browser opens
- Monitor console output

## Success Criteria

A successful workflow execution includes:
- ✅ Client and document selected
- ✅ JSON scenarios generated or reused
- ✅ Credentials loaded or entered
- ✅ Agent invoked successfully
- ✅ All scenarios executed
- ✅ Screenshots captured
- ✅ TES-070 report generated
- ✅ Final summary displayed

## Next Steps

1. Test new consolidated workflow
2. Verify agent executes correctly
3. Confirm TES-070 generation works
4. Validate evidence capture
5. Disable old 3-step hooks
6. Document any issues
7. Iterate and improve

---

**Status**: Ready for testing
**Created**: March 6, 2026
**Version**: 1.0.0
