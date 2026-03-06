# Intelligent Agent Routing for FSM Approval Testing

## Date: March 6, 2026

## Architecture Overview

The approval regression testing workflow uses **intelligent routing** to automatically select the appropriate specialized subagent based on the transaction type detected in the TES-070 document.

## How It Works

### Universal Hook
**Hook**: `run-approval-regression-tests.kiro.hook`
- Universal entry point for ALL FSM approval workflows
- Parses TES-070 to detect transaction type
- Routes to appropriate specialized subagent
- Validates subagent exists before proceeding

### Specialized Subagents
Each transaction type has its own specialized testing agent:

| Transaction Type | FSM Module | Subagent | Status |
|-----------------|------------|----------|--------|
| ExpenseInvoice | Payables | invoice-approval-test-agent | ✅ Created |
| ManualJournal | General Ledger | journal-approval-test-agent | ❌ Not yet created |
| CashLedgerTransaction | Cash Management | cash-approval-test-agent | ❌ Not yet created |

## Workflow

### Phase 1: Gather Information
1. User selects client
2. User selects TES-070 document
3. Hook parses TES-070 using `tes070_analyzer.py`
4. Hook extracts transaction type from analysis

### Phase 2: Intelligent Routing
5. Hook maps transaction type to subagent:
   ```
   ExpenseInvoice → invoice-approval-test-agent
   ManualJournal → journal-approval-test-agent
   CashLedgerTransaction → cash-approval-test-agent
   ```
6. Hook checks if subagent exists in `.kiro/agents/`
7. If subagent does NOT exist:
   - Display error message
   - List available agents
   - Stop execution
   - Suggest creating required agent or using different TES-070
8. If subagent exists: Continue

### Phase 3: Gather Credentials
9. Check for existing credentials
10. Prompt for credentials if needed
11. Save credentials for future use

### Phase 4: Invoke Specialized Agent
12. Invoke the appropriate subagent with parameters
13. Agent executes tests autonomously

### Phase 5: Monitor and Report
14. Display final summary with results

## Benefits

### Extensibility
- Easy to add new approval types
- Each agent specialized for its transaction type
- No code changes to hook when adding new agents

### Maintainability
- Single universal hook for all approval types
- Specialized agents easier to maintain
- Clear separation of concerns

### User Experience
- One hook for all approval workflows
- Automatic routing (no manual selection)
- Clear error messages if agent missing

### Safety
- Validates agent exists before execution
- Prevents errors from missing agents
- Guides user to create missing agents

## Transaction Type Detection

The hook extracts transaction type from TES-070 analysis JSON:

```json
{
  "transaction_type": "ExpenseInvoice",
  "fsm_module": "Payables",
  ...
}
```

Transaction types are identified by:
- Document title keywords
- Test scenario descriptions
- FSM module references
- Business class names

## Agent Mapping Logic

```python
AGENT_MAP = {
    "ExpenseInvoice": "invoice-approval-test-agent",
    "ManualJournal": "journal-approval-test-agent",
    "CashLedgerTransaction": "cash-approval-test-agent"
}

transaction_type = analysis["transaction_type"]
agent_name = AGENT_MAP.get(transaction_type)

if not agent_name:
    raise ValueError(f"Unknown transaction type: {transaction_type}")

agent_path = f".kiro/agents/{agent_name}.md"
if not os.path.exists(agent_path):
    raise FileNotFoundError(f"Agent {agent_name} not found. Please create it first.")

# Invoke agent
invokeSubAgent(name=agent_name, prompt=..., explanation=...)
```

## Error Handling

### Missing Agent Error
```
ERROR: Transaction type 'ManualJournal' requires 'journal-approval-test-agent' which is not yet created.

Available agents:
- invoice-approval-test-agent (ExpenseInvoice)

Suggestions:
1. Create journal-approval-test-agent for ManualJournal workflows
2. Use a different TES-070 document (ExpenseInvoice type)
3. Contact development team to create the required agent
```

### Unknown Transaction Type Error
```
ERROR: Unknown transaction type 'CustomTransaction' detected in TES-070.

Supported transaction types:
- ExpenseInvoice (Payables)
- ManualJournal (General Ledger)
- CashLedgerTransaction (Cash Management)

Please verify the TES-070 document or contact development team.
```

## Creating New Agents

When a new approval type is needed:

### Step 1: Identify Transaction Type
- Review TES-070 document
- Identify FSM module (Payables, GL, Cash, etc.)
- Identify business class (ExpenseInvoice, ManualJournal, etc.)

### Step 2: Create Specialized Agent
```markdown
---
name: journal-approval-test-agent
description: Autonomous QA testing agent for FSM Manual Journal approval workflows
tools: ["read", "write", "shell"]
model: claude-3-7-sonnet-20250219
---

# Manual Journal Approval Test Agent

Specialized agent for testing GL manual journal approval workflows...
```

### Step 3: Update Agent Mapping
The hook automatically detects new agents - no code changes needed!

### Step 4: Test New Agent
1. Select TES-070 for ManualJournal
2. Hook detects transaction type
3. Hook finds journal-approval-test-agent
4. Hook invokes agent
5. Agent executes tests

## Currently Available Agents

### invoice-approval-test-agent
- **Transaction Type**: ExpenseInvoice
- **FSM Module**: Payables
- **Status**: ✅ Fully implemented
- **Capabilities**:
  - Browser automation with Playwright
  - FSM login and navigation (iframe support)
  - Invoice creation and submission
  - Approval workflow execution
  - Work unit monitoring
  - Status validation
  - Screenshot capture
  - TES-070 report generation

## Future Agents (Planned)

### journal-approval-test-agent
- **Transaction Type**: ManualJournal
- **FSM Module**: General Ledger
- **Status**: ❌ Not yet created
- **Planned Capabilities**:
  - GL journal entry creation
  - Journal approval workflows
  - Account validation
  - Balance verification

### cash-approval-test-agent
- **Transaction Type**: CashLedgerTransaction
- **FSM Module**: Cash Management
- **Status**: ❌ Not yet created
- **Planned Capabilities**:
  - Cash transaction creation
  - Cash approval workflows
  - Bank reconciliation
  - Cash balance verification

## Comparison: Before vs After

### Before (Hardcoded)
- Hook always invokes invoice-approval-test-agent
- Cannot handle other approval types
- Requires new hook for each type
- Fragmented user experience

### After (Intelligent Routing)
- Hook detects transaction type automatically
- Routes to appropriate specialized agent
- Single hook for all approval types
- Extensible architecture
- Clear error messages

## Testing the Routing

### Test Case 1: ExpenseInvoice (Should Work)
1. Select TES-070 for ExpenseInvoice
2. Hook detects: ExpenseInvoice
3. Hook routes to: invoice-approval-test-agent
4. Agent executes tests
5. ✅ Success

### Test Case 2: ManualJournal (Should Fail Gracefully)
1. Select TES-070 for ManualJournal
2. Hook detects: ManualJournal
3. Hook looks for: journal-approval-test-agent
4. Agent not found
5. ❌ Error: Agent not yet created
6. Suggests creating agent or using different TES-070

### Test Case 3: Unknown Type (Should Fail Gracefully)
1. Select TES-070 for unknown type
2. Hook detects: UnknownType
3. Hook has no mapping
4. ❌ Error: Unknown transaction type
5. Lists supported types

## Next Steps

1. Test intelligent routing with ExpenseInvoice TES-070
2. Verify error handling for missing agents
3. Create journal-approval-test-agent when needed
4. Create cash-approval-test-agent when needed
5. Document agent creation process
6. Add more transaction types as needed

---

**Status**: Implemented and ready for testing
**Created**: March 6, 2026
**Version**: 1.0.0
