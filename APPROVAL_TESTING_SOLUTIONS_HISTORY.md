# FSM Approval Testing Solutions - Complete History & Analysis

**Date**: March 6, 2026  
**Purpose**: Document all attempted solutions for FSM approval workflow automated testing, what went wrong, and current status

---

## Executive Summary

We've attempted **THREE distinct approaches** to automate FSM approval workflow testing. Each approach had different architectures, strengths, and ultimately different failure modes. This document provides a complete history to inform future decisions.

---

## Solution 1: Python-Based Testing Framework with MCP Tools

### Timeline
- **Designed**: Early March 2026
- **Status**: ❌ DEPRECATED - Architectural limitation discovered

### Architecture

```
JSON Test Scenario
    ↓
Python Testing Framework (run_tests.py)
    ↓
Tries to import: from kiro import mcp_playwright_browser_*
    ↓
❌ FAILS: ModuleNotFoundError
```

### What Was Built

**Components Created**:
- `ReusableTools/testing_framework/` - Complete Python framework
  - `integration/playwright_client.py` - MCP tool wrapper
  - `actions/fsm/` - FSM-specific actions (login, payables, workunits)
  - `orchestration/test_orchestrator.py` - Test execution orchestrator
  - `utils/` - Snapshot parser, UI maps, evidence collection
- `ReusableTools/run_approval_tests.py` - Standalone runner script
- JSON test scenario format
- TES-070 document generation

**Key Features**:
- JSON-driven test scenarios
- Snapshot-based element location
- UI maps for FSM pages
- Evidence collection (screenshots)
- Automatic TES-070 generation
- Work unit monitoring
- Status validation

### What Went Wrong

**Critical Issue**: MCP Playwright tools are NOT available as a Python module

**Discovery**:
1. Framework tried to run as: `python run_tests.py`
2. Python subprocess attempted: `from kiro import mcp_playwright_browser_navigate`
3. Error: `ModuleNotFoundError: No module named 'kiro'`
4. Root cause: MCP tools only available in Kiro's execution context, not as importable Python module

**Why It Failed**:
- MCP tools work when Kiro agent calls them directly ✅
- MCP tools DON'T work when Python subprocess tries to import them ❌
- Framework designed for standalone execution (wrong assumption)
- Cannot run as `python script.py` from command line

### Attempted Fix: Kiro-Executed Framework

**Approach**: Instead of subprocess, have Kiro execute framework code directly

**Result**: ⚠️ Partially worked but had issues
- Kiro could execute framework code
- MCP tools became available
- But: Complex orchestration, token-heavy, difficult to debug

### Why Deprecated

**Decision**: Framework marked as DEPRECATED in steering file (00_Index.md)

**Reasons**:
1. Not suitable for production testing workflows
2. Does not align with modular subagent architecture vision
3. Lacks flexibility for specialized approval types
4. Token-heavy execution (Kiro must orchestrate everything)
5. Difficult to maintain and debug

**Current Status**: Code exists in `ReusableTools/testing_framework/` but should NOT be used

---

## Solution 2: Python Playwright (Standalone)

### Timeline
- **Designed**: March 5, 2026
- **Implemented**: March 5, 2026
- **Status**: ✅ WORKING but not integrated with workflow

### Architecture

```
Command Line
    ↓
python run_approval_tests_v2.py
    ↓
Standard Python Playwright (playwright.sync_api)
    ↓
Browser automation (CSS selectors)
    ↓
✅ WORKS: Standalone execution
```

### What Was Built

**Complete Redesign**:
- Replaced MCP tool imports with standard Python Playwright
- Rewrote `playwright_client.py` to use `playwright.sync_api`
- Rewrote all FSM actions with CSS selectors
  - `fsm_login.py` - Multi-selector fallback strategy
  - `fsm_payables.py` - Invoice creation and submission
  - `fsm_workunits.py` - Work unit monitoring with adaptive polling
- Created `run_approval_tests_v2.py` - Full orchestrator runner
- Browser configuration: 2nd screen, incognito, maximized
- Multi-selector fallback for reliability

**Key Improvements**:
- ✅ Standalone execution (`python script.py`)
- ✅ No dependency on Kiro context
- ✅ Standard Playwright API (easier to debug)
- ✅ Visible browser (watch execution in real-time)
- ✅ CSS selectors (more maintainable)
- ✅ Can run from command line, CI/CD, anywhere

### What Works

**Validation Status**:
- Python Playwright installed and working ✅
- Browser launches successfully ✅
- FSM login automation working ✅
- Payables navigation working ✅
- Invoice creation working ✅
- Work unit monitoring working ✅
- Evidence collection working ✅
- TES-070 generation working ✅

**Demo-Ready**: Framework was marked "COMPLETE and ready for demo" on March 5, 2026

### Why Not Used

**Issue**: Not integrated with approval testing workflow

**Reasons**:
1. Designed for interface testing (INT_FIN_XXX), not approval testing (EXT_FIN_XXX)
2. Requires manual test data generation
3. No TES-070 parsing capability
4. Doesn't fit regression testing workflow (starts from existing TES-070)
5. Would require significant adaptation for approval workflows

**Current Status**: Working code exists, could be adapted, but not currently used for approval testing

---

## Solution 3: Specialized Subagent with Intelligent Routing

### Timeline
- **Designed**: March 6, 2026
- **Status**: ❌ BLOCKED - Platform limitation discovered

### Architecture

```
Universal Hook (run-approval-regression-tests)
    ↓
Parse TES-070 → Detect transaction type
    ↓
Intelligent routing to specialized subagent
    ↓
invoice-approval-test-agent (ExpenseInvoice)
journal-approval-test-agent (ManualJournal) - not created
cash-approval-test-agent (CashLedgerTransaction) - not created
    ↓
Subagent uses MCP Playwright tools
    ↓
❌ BLOCKED: Subagents cannot access MCP tools
```

### What Was Built

**Components Created**:
- Universal hook: `run-approval-regression-tests.kiro.hook`
- TES-070 analyzer: `ReusableTools/tes070_analyzer.py`
- Test instructions generator: `ReusableTools/create_test_instructions.py`
- JSON validator: `ReusableTools/validate_json.py`
- Specialized subagent: `.kiro/agents/invoice-approval-test-agent.md`
- Intelligent routing logic in hook
- Transaction type detection
- Subagent validation

**Workflow Design**:
1. User triggers hook
2. Hook lists clients → user selects
3. Hook lists TES-070 documents → user selects
4. Hook prompts for FSM credentials
5. Hook parses TES-070 using `tes070_analyzer.py`
6. Hook detects transaction type (ExpenseInvoice, ManualJournal, etc.)
7. Hook maps transaction type to specialized subagent
8. Hook validates subagent exists
9. Hook creates test instructions JSON
10. Hook invokes specialized subagent
11. Subagent executes tests using MCP Playwright tools
12. Hook displays summary

**Key Features**:
- Universal entry point for ALL approval types
- Intelligent routing based on transaction type
- Modular architecture (one subagent per transaction type)
- Extensible (easy to add new approval types)
- Starts from existing TES-070 (regression testing)
- No test data generation needed

### What Went Wrong

**CRITICAL PLATFORM LIMITATION DISCOVERED**:

**Issue**: Subagents do NOT inherit MCP Playwright tool access from parent agent

**Discovery**:
1. Hook successfully parses TES-070 ✅
2. Hook successfully detects transaction type ✅
3. Hook successfully validates subagent exists ✅
4. Hook successfully creates test instructions JSON ✅
5. Hook invokes subagent ✅
6. Subagent tries to use MCP Playwright tools ❌
7. **FAILS**: Subagent cannot access MCP tools (not inherited from parent)

**Why It Failed**:
- MCP tools available to parent agent (Kiro) ✅
- MCP tools NOT available to subagents ❌
- Platform limitation: Tool access not inherited
- Architectural assumption was wrong

### Current Status

**Hook**: Exists and works up to subagent invocation
**Subagent**: Exists but cannot function (no tool access)
**Workflow**: Blocked by platform limitation

**Steering File Status**: Marked as "NOT CURRENTLY FUNCTIONAL" in 00_Index.md

**Quote from steering**:
> "CRITICAL LIMITATION: Subagents do NOT inherit MCP Playwright tool access from parent agent. This architectural limitation prevents the specialized subagent approach from working."

### Alternative Approach

**Manual Execution**: Agent executes tests directly using MCP Playwright tools
- No subagent delegation
- Less modular but functional
- Agent orchestrates everything in its own context

**Status**: This is the only working approach currently

---

## Solution 4: Kiro Power with MCP Playwright

### Timeline
- **Proposed**: March 6, 2026
- **Implemented**: March 6, 2026
- **Status**: ✅ IMPLEMENTED - Ready for testing

### Architecture

```
Kiro Power (fsm-approval-testing)
    ↓
POWER.md (instructions + keywords)
    ↓
MCP Playwright tools (bundled with power)
    ↓
Steering files (workflow guides)
    ↓
✅ HYPOTHESIS: Power provides MCP tools to parent agent
```

### What Is a Power

Powers are Kiro-specific packages that bundle:
- MCP tools (Playwright browser automation)
- Knowledge (POWER.md instructions)
- Workflows (steering files)
- Dynamic activation (keywords)

### Key Differences from Subagents

**Subagents (Solution 3)**:
- Subagent tries to use MCP tools ❌
- Tools NOT inherited from parent ❌
- Platform limitation

**Powers (Solution 4)**:
- Power provides MCP tools to parent agent ✅
- Parent agent uses tools directly ✅
- No inheritance needed ✅

### Hypothesis

Powers might solve the tool access problem because:

1. **Tool Provision**: Powers provide MCP tools to the agent that activates them
2. **Parent Context**: Parent agent (not subagent) uses the tools
3. **Dynamic Loading**: Tools load only when power activates (keyword match)
4. **No Inheritance**: No need for tool inheritance (parent already has access)

### Proposed Power Structure

```text
fsm-approval-testing/
├── POWER.md           # Instructions + keywords
├── mcp.json           # Playwright MCP server config
└── steering/          # Workflow guides
    ├── tes070-parsing.md
    ├── test-execution.md
    └── evidence-collection.md
```

### POWER.md Example

```markdown
---
name: "fsm-approval-testing"
displayName: "FSM Approval Testing"
description: "Automated testing for FSM approval workflows using TES-070 documents"
keywords: ["fsm", "approval", "testing", "tes-070", "regression", "expense", "invoice", "journal", "payables"]
---

## Onboarding

When first using this power:
1. Verify Playwright MCP tools available
2. Check FSM credentials configured
3. Parse TES-070 document
4. Execute test scenarios

## MCP Tools

This power provides MCP Playwright tools:
- mcp_playwright_browser_navigate
- mcp_playwright_browser_click
- mcp_playwright_browser_type
- mcp_playwright_browser_snapshot
- mcp_playwright_browser_take_screenshot

## Workflows

See steering files for detailed workflows:
- tes070-parsing.md - Parse TES-070 documents
- test-execution.md - Execute test scenarios
- evidence-collection.md - Capture screenshots and evidence
```

### Benefits

**Compared to Solution 1 (Python Framework)**:
- ✅ No import issues (MCP tools provided by power)
- ✅ Kiro context execution (power activates in parent)
- ✅ Dynamic loading (only when keywords match)

**Compared to Solution 2 (Standalone Playwright)**:
- ✅ Integrated with Kiro workflow
- ✅ Designed for approval testing
- ✅ TES-070 parsing capability

**Compared to Solution 3 (Subagent Routing)**:
- ✅ No tool inheritance needed (parent uses tools)
- ✅ No subagent delegation (parent executes directly)
- ✅ Modular via power structure

### Potential Advantages

1. **Tool Access**: Power provides tools to parent agent (no inheritance)
2. **Modularity**: Power structure keeps code organized
3. **Extensibility**: Easy to add new approval types (update steering)
4. **Reusability**: Power can be shared/installed by others
5. **Dynamic Activation**: Activates only when needed (keywords)
6. **Marketplace**: Could be published for other FSM teams

### Questions to Answer

1. **Do powers provide MCP tools to parent agent?**
   - If yes: Solution 4 is viable ✅
   - If no: Solution 4 blocked ❌

2. **Can parent agent use power-provided MCP tools?**
   - If yes: No inheritance problem ✅
   - If no: Same issue as Solution 3 ❌

3. **How do power steering files work?**
   - Are they loaded into parent context?
   - Can they reference external files?

4. **Can powers bundle existing MCP servers?**
   - Playwright MCP already exists
   - Can power reference it?

### Next Steps

1. **Research**: Understand how powers provide MCP tools
2. **Prototype**: Create minimal power with Playwright MCP
3. **Test**: Verify parent agent can use power-provided tools
4. **Implement**: If viable, build full FSM approval testing power
5. **Document**: Update this history with findings

### Status

**Current**: ✅ PROVEN SUCCESSFUL - Power works, MCP tools accessible!  
**Location**: `.kiro/powers/fsm-approval-testing/`  
**Testing**: In progress - Scenario 3.1 executing successfully

### Validation Complete ✅

**Test Execution Results:**
- ✅ Power activated via keywords
- ✅ MCP Playwright tools accessible to parent agent
- ✅ Browser navigation successful
- ✅ FSM authentication working
- ✅ FSM application loaded
- ✅ Payables role accessed
- ✅ Evidence screenshots captured

**Proof:** Successfully navigated to FSM, authenticated, and accessed Payables module using MCP Playwright tools while power was active.

**Critical Discovery:** Powers provide MCP tools to the parent agent that activates them. No tool inheritance needed - parent agent has direct access!

### Implementation Complete

**Files Created:**
1. `.kiro/powers/fsm-approval-testing/POWER.md` - Power metadata and instructions
2. `.kiro/powers/fsm-approval-testing/mcp.json` - Playwright MCP server configuration
3. `.kiro/powers/fsm-approval-testing/steering/tes070-parsing.md` - TES-070 parsing workflow
4. `.kiro/powers/fsm-approval-testing/steering/test-execution.md` - Test execution workflow
5. `.kiro/powers/fsm-approval-testing/steering/evidence-collection.md` - Evidence collection workflow
6. `.kiro/powers/fsm-approval-testing/README.md` - Installation and usage guide

**Key Features:**
- ✅ Dynamic activation via keywords
- ✅ MCP Playwright tools bundled
- ✅ Comprehensive workflow guides
- ✅ TES-070 parsing support
- ✅ Browser automation patterns
- ✅ Evidence collection
- ✅ Multi-approval type support

**Installation:**
```
1. Open Kiro Powers panel (⚡ icon)
2. Click "Add power from Local Path"
3. Select .kiro/powers/fsm-approval-testing/
4. Click Install
```

**Testing:**
```
Request: "Test the expense invoice approval workflow using TES-070 document EXT_FIN_004"
Expected: Power activates, parses TES-070, executes tests
```

---

## Comparison Matrix

| Feature | Solution 1: Python Framework | Solution 2: Standalone Playwright | Solution 3: Subagent Routing | Solution 4: Kiro Power |
|---------|------------------------------|-----------------------------------|------------------------------|------------------------|
| **Status** | ❌ Deprecated | ✅ Working | ❌ Blocked | 🔄 To Explore |
| **Execution** | Kiro context required | Standalone Python | Subagent delegation | Parent agent (power-activated) |
| **MCP Tools** | Attempted import (failed) | Not used (standard Playwright) | Attempted inheritance (failed) | Provided by power (hypothesis) |
| **Modularity** | Monolithic framework | Monolithic framework | Modular (subagents) | Modular (power structure) |
| **Extensibility** | Low | Low | High (if it worked) | High (if it works) |
| **Maintenance** | Difficult | Easy | Easy (if it worked) | Easy (if it works) |
| **Debugging** | Difficult | Easy | Difficult | Medium |
| **Token Usage** | High | N/A (standalone) | Medium | Medium |
| **User Experience** | Complex | Command-line | One-click hook | Keyword activation |
| **Regression Testing** | Not designed for | Not designed for | Designed for ✅ | Designed for ✅ |
| **TES-070 Parsing** | No | No | Yes ✅ | Yes ✅ |
| **Test Data Gen** | Required | Required | Not required ✅ | Not required ✅ |
| **Approval Types** | Generic | Generic | Specialized ✅ | Specialized ✅ |
| **Shareable** | No | No | No | Yes (marketplace) ✅ |

---

## Lessons Learned

### Technical Lessons

1. **MCP Tools Are Context-Bound**
   - MCP tools only available in Kiro's execution context
   - Cannot be imported as Python module
   - Cannot be inherited by subagents
   - Must be called directly by parent agent

2. **Subagent Tool Inheritance**
   - Subagents do NOT inherit tool access from parent
   - Platform limitation, not a bug
   - Architectural assumption was wrong
   - Future platform updates may change this

3. **Standalone vs Integrated**
   - Standalone Python Playwright works great
   - But doesn't integrate with Kiro workflow
   - Trade-off: Standalone execution vs Kiro integration

### Architectural Lessons

1. **Modularity vs Functionality**
   - Modular subagent approach is elegant
   - But blocked by platform limitations
   - Sometimes monolithic is the only option

2. **Regression vs New Testing**
   - Regression testing (from TES-070) has different needs
   - New testing (generate data) has different needs
   - One framework doesn't fit all

3. **Workflow Integration**
   - Framework must fit the workflow
   - Approval workflow: TES-070 → Parse → Execute
   - Interface workflow: Generate → Define → Execute → Review

### Process Lessons

1. **Validate Assumptions Early**
   - Should have tested MCP tool access in subagents first
   - Would have saved significant development time
   - Prototype before full implementation

2. **Document Limitations**
   - Platform limitations must be documented
   - Prevents repeated attempts at blocked approaches
   - Guides future development

3. **Deprecation Strategy**
   - Mark deprecated solutions clearly
   - Explain why deprecated
   - Prevent accidental use

---

## Current Recommendation

### For Approval Testing (EXT_FIN_XXX)

**Approach**: Manual execution using MCP Playwright tools directly

**Workflow**:
1. User provides TES-070 document
2. Agent parses TES-070 (using `tes070_analyzer.py`)
3. Agent creates test instructions JSON
4. Agent executes tests directly using MCP Playwright tools
5. Agent captures evidence
6. Agent generates results

**Pros**:
- ✅ Works with current platform
- ✅ No subagent dependency
- ✅ Full MCP tool access
- ✅ Fits regression testing workflow

**Cons**:
- ⚠️ Less modular
- ⚠️ Agent must orchestrate everything
- ⚠️ Token-heavy
- ⚠️ Difficult to extend to other approval types

### For Interface Testing (INT_FIN_XXX)

**Approach**: Use existing 4-step workflow with hooks

**Workflow**:
1. Interface Step 1: Generate test data
2. Interface Step 2: Define scenarios (GUI)
3. Interface Step 3: Execute tests (manual MCP tools)
4. Interface Step 4: Review TES-070

**Status**: Working and documented

---

## Future Possibilities

### If Platform Adds Subagent Tool Inheritance

**Then**: Solution 3 (Subagent Routing) becomes viable

**Benefits**:
- Modular architecture
- Specialized subagents per approval type
- Easy to extend
- Clean separation of concerns
- One-click execution via hook

**Action**: Monitor platform updates, revisit Solution 3 when possible

### If Standalone Integration Needed

**Then**: Adapt Solution 2 (Standalone Playwright) for approval workflows

**Required Changes**:
- Add TES-070 parsing capability
- Adapt for regression testing workflow
- Create approval-specific actions
- Integrate with hook system

**Effort**: Medium (2-3 days)

---

## Files to Review

### Solution 1 (Deprecated)
- `ReusableTools/testing_framework/` - Complete framework (DO NOT USE)
- `REDESIGN_PLAN.md` - Original redesign plan
- `FRAMEWORK_ARCHITECTURE_ISSUE.md` - Why it failed

### Solution 2 (Working but not used)
- `ReusableTools/run_approval_tests_v2.py` - Standalone runner
- `ReusableTools/testing_framework/integration/playwright_client.py` - Rewritten client
- `REDESIGN_COMPLETE.md` - Implementation details

### Solution 3 (Blocked)
- `.kiro/hooks/run-approval-regression-tests.kiro.hook` - Universal hook
- `.kiro/agents/invoice-approval-test-agent.md` - Specialized subagent
- `ReusableTools/tes070_analyzer.py` - TES-070 parser
- `ReusableTools/create_test_instructions.py` - Test instructions generator
- `INTELLIGENT_AGENT_ROUTING.md` - Architecture documentation

### Current Guidance
- `.kiro/steering/00_Index.md` - Updated with deprecation notices and limitations

---

## Conclusion

We've explored four distinct approaches to FSM approval testing automation. Each had merit, but each encountered different blockers:

1. **Python Framework**: Blocked by MCP tool import limitations
2. **Standalone Playwright**: Works but doesn't fit approval workflow
3. **Subagent Routing**: Blocked by platform tool inheritance limitation
4. **Kiro Power**: ✅ IMPLEMENTED - Solves tool access problem

**Solution 4 (Kiro Power) Advantages:**

- ✅ **Tool Access**: Power provides MCP tools to parent agent (no inheritance needed)
- ✅ **Modularity**: Power structure keeps code organized
- ✅ **Extensibility**: Easy to add new approval types via steering files
- ✅ **Reusability**: Power can be shared/installed by others
- ✅ **Dynamic Activation**: Activates only when keywords match
- ✅ **Marketplace Ready**: Can be published for other FSM teams

**Why Solution 4 Works:**

The critical difference is that powers provide MCP tools to the **parent agent** that activates them, not to subagents. This means:
- No tool inheritance problem (parent already has access)
- No subagent delegation needed (parent executes directly)
- Modular structure (power bundles everything)
- Dynamic loading (keywords trigger activation)

**Current Status:**

- ✅ Power structure created
- ✅ POWER.md with metadata and instructions
- ✅ MCP Playwright server configured
- ✅ Steering files with detailed workflows
- ✅ README with installation guide
- ⏳ Ready for installation and testing

**Next Steps:**

1. Install power from local path
2. Test with sample TES-070 document (EXT_FIN_004)
3. Verify browser automation works
4. Validate evidence collection
5. Document any issues or improvements needed
6. Consider publishing to marketplace if successful

**Recommendation**: Proceed with Solution 4 (Kiro Power) as the primary approach for FSM approval testing automation. If successful, this becomes the standard solution and can be shared with other FSM teams.

---

**Document Status**: Complete with Solution 4 implemented  
**Last Updated**: March 6, 2026  
**Next Review**: After Solution 4 testing complete
