# Approval Hooks Optimization Recommendations

## Executive Summary

The three approval hooks (Step 1-3) have organizational issues that make them confusing and hard to maintain. This document provides specific recommendations to streamline and clarify the workflow.

---

## Current Issues

### 1. Naming Confusion
- **Step 3** is named "Generate TES-070" but TES-070 is already generated in Step 2
- Should be renamed to "Review TES-070 Document" (already done in v3.1.0)

### 2. Excessive Repetition
The following information is repeated across multiple hooks:
- Extension IDs start with EXT_ (mentioned 10+ times)
- Framework execution context requirements (3+ times)
- Credential security rules (3+ times)
- Interactive UI pattern explanations (2+ times)
- "This is for ENHANCEMENTS, not INTERFACES" (5+ times)

### 3. Inconsistent Terminology
- Mixing "Extension ID" vs "Interface ID" (framework uses `interface_id` field)
- "Approval workflows" vs "Enhancements" vs "Extensions"
- Need consistent language throughout

### 4. Overly Detailed Instructions
- **Step 1** has 200+ lines of parsing rules that could be condensed
- **Step 2** has 150+ lines of framework execution details
- **Step 3** has 100+ lines of review checklist

### 5. Buried Critical Information
Important notes scattered throughout instead of highlighted upfront:
- Framework must run in Kiro context (buried in Step 2)
- TES-070 auto-generated (mentioned late in Step 2)
- Sequential execution requirement (buried in notes)

---

## Recommended Structure

### Common Header (All Steps)
Place at the top of each hook to establish context once:

```
**WORKFLOW:** Approval Testing (Enhancements - E in RICE)
**EXTENSION IDs:** Start with EXT_ (e.g., EXT_FIN_004)
**SEQUENCE:** Step 1 → Step 2 → Step 3 (run in order)
**FRAMEWORK:** Automated testing with auto-generated TES-070
```

### Step 1: Parse TES-070 (Simplified)

**Current:** 200+ lines with extensive parsing rules
**Recommended:** 80-100 lines focusing on workflow

**Simplifications:**
1. Remove detailed parsing rules → Reference analyzer tool documentation
2. Consolidate vendor/amount inference → Use defaults, document exceptions
3. Remove JSON structure examples → Reference framework documentation
4. Focus on: Select document → Run analyzer → Generate JSON → Validate

**Key Sections:**
- User Selection (client + document)
- Run Analyzer Tool
- Generate Framework JSON (reference template)
- Validate Output
- Show Summary + Next Steps

### Step 2: Execute Tests (Streamlined)

**Current:** 150+ lines with framework details
**Recommended:** 60-80 lines focusing on execution

**Simplifications:**
1. Remove framework architecture explanation → Reference docs
2. Consolidate credential verification → Single check function
3. Remove "what framework does" section → Users don't need internals
4. Focus on: Select scenario → Verify setup → Execute → Show results

**Key Sections:**
- User Selection (client + scenario file)
- Prerequisites Check (credentials + validation)
- Execute Framework (code block only)
- Show Results Summary
- Next Steps

### Step 3: Review TES-070 (Focused)

**Current:** 100+ lines with extensive checklist
**Recommended:** 50-60 lines focusing on review

**Simplifications:**
1. Remove automated verification code → Optional, not required
2. Consolidate review checklist → High-level items only
3. Remove troubleshooting → Reference main docs
4. Focus on: Locate document → Open + F9 → Review checklist → Finalize

**Key Sections:**
- Locate Document
- Open and Update TOC (F9)
- Review Checklist (5-7 items)
- Finalization Steps
- Completion Confirmation

---

## Specific Optimizations

### 1. Create Shared Context Section

Create a new file: `.kiro/hooks/_approval_context.md`

```markdown
# Approval Testing Context (Shared)

**Workflow Type:** Enhancements (E in RICE) - Approval workflows
**Extension IDs:** Start with EXT_ (e.g., EXT_FIN_004)
**Transaction Types:** ExpenseInvoice, ManualJournal, CashLedgerTransaction
**Modules:** Payables, General Ledger, Cash Management

**Framework Behavior:**
- Runs in Kiro execution context (MCP tools available)
- Auto-generates TES-070 in Step 2
- Sequential scenario execution
- Automatic evidence collection
- State interpolation with {{state.variable}}

**Credentials:**
- Location: Projects/{ClientName}/Credentials/
- Files: .env.fsm, .env.passwords
- Security: Never commit, never log, read at runtime

**File Locations:**
- Input TES-070: Projects/{ClientName}/TES-070/Approval_TES070s_For_Regression_Testing/
- Scenarios: Projects/{ClientName}/TestScripts/approval/
- Evidence: Projects/{ClientName}/Temp/evidence/
- Output TES-070: Projects/{ClientName}/TES-070/Generated_TES070s/
```

Reference this in each hook with: "See _approval_context.md for workflow details"

### 2. Simplify Step 1 Parsing Rules

**Current approach:** 50+ lines of inference rules
**Recommended:** Use defaults + document exceptions

```python
# Default values (covers 80% of cases)
defaults = {
    'vendor_class': 'GHR',
    'amount': '100.00',
    'authority_code': None,
    'expected_route': 'AUTO',
    'expected_status': 'Released'
}

# Override only when explicitly mentioned in TES-070
# Let analyzer tool handle inference
```

### 3. Consolidate Framework Execution

**Current:** Framework code + explanation + notes = 100+ lines
**Recommended:** Code block only with inline comments

```python
# Step 2 simplified execution block
import sys
sys.path.insert(0, 'ReusableTools')
from testing_framework.orchestration.test_orchestrator import TestOrchestrator
from testing_framework.utils.logger import Logger

# Read environment from credentials
with open('Projects/{ClientName}/Credentials/.env.fsm') as f:
    environment = [line.split('=')[1].strip() for line in f if line.startswith('FSM_ENVIRONMENT=')][0]

# Execute tests
logger = Logger('approval_test', verbose=True)
orchestrator = TestOrchestrator(client_name='{ClientName}', environment=environment, logger=logger)

try:
    result = orchestrator.run('Projects/{ClientName}/TestScripts/approval/{scenario_file}')
    print(f'Status: {"PASSED" if result.passed else "FAILED"}')
    print(f'TES-070: {result.tes070_path}')
finally:
    orchestrator.cleanup()
```

### 4. Streamline Review Checklist

**Current:** 30+ checklist items
**Recommended:** 7 high-level items

```
Review Checklist:
1. Open document, press F9 to update TOC
2. Verify title page (client, extension ID, date)
3. Check test summary (scenario counts, pass rate)
4. Review scenario results (all documented with screenshots)
5. Verify approval routing documented for each scenario
6. Check screenshot quality (clear, readable, properly inserted)
7. Save and finalize document
```

### 5. Remove Redundant Sections

**Remove from all hooks:**
- "IMPORTANT: Load steering file..." (not needed, auto-loaded)
- Repeated security warnings (mention once in shared context)
- "This is for ENHANCEMENTS not INTERFACES" (state once in header)
- Framework architecture explanations (reference docs)
- Extensive troubleshooting (keep 2-3 common issues only)

### 6. Standardize User Interaction Pattern

**Current:** Inconsistent explanations of interactive UI
**Recommended:** Standard pattern in all hooks

```
**USER SELECTION:**
1. List available options (clients/documents/scenarios)
2. User selects from interactive UI
3. Proceed with selection
```

---

## Implementation Priority

### High Priority (Do First)
1. ✅ Update Step 3 name to "Review TES-070" (DONE in v3.1.0)
2. Create shared context file (_approval_context.md)
3. Simplify Step 1 parsing rules (use defaults)
4. Consolidate Step 2 framework execution (code only)
5. Streamline Step 3 review checklist (7 items)

### Medium Priority (Do Next)
6. Remove redundant "ENHANCEMENTS not INTERFACES" warnings
7. Standardize user interaction pattern
8. Remove "Load steering file" instructions (auto-loaded)
9. Consolidate credential security warnings
10. Remove framework architecture explanations

### Low Priority (Nice to Have)
11. Add visual flow diagram to shared context
12. Create troubleshooting reference doc (separate from hooks)
13. Add version history to each hook
14. Create hook testing checklist

---

## Estimated Impact

### Before Optimization
- **Step 1:** 200+ lines, 15-20 min to read/understand
- **Step 2:** 150+ lines, 10-15 min to read/understand
- **Step 3:** 100+ lines, 8-10 min to read/understand
- **Total:** 450+ lines, 33-45 min cognitive load

### After Optimization
- **Step 1:** 80-100 lines, 5-7 min to read/understand
- **Step 2:** 60-80 lines, 4-5 min to read/understand
- **Step 3:** 50-60 lines, 3-4 min to read/understand
- **Total:** 190-240 lines, 12-16 min cognitive load

**Improvement:** 57% reduction in length, 63% reduction in cognitive load

---

## Next Steps

1. Review these recommendations with team
2. Prioritize which optimizations to implement
3. Create shared context file
4. Update hooks incrementally (test after each change)
5. Document changes in CHANGELOG.md
6. Update user documentation to reflect simplified workflow

---

## Questions to Consider

1. Should we create a visual workflow diagram?
2. Do we need separate troubleshooting documentation?
3. Should parsing rules be externalized to a config file?
4. Can we auto-detect extension ID from filename?
5. Should we add hook validation tests?

---

## Conclusion

The approval hooks are functional but overly verbose and repetitive. By consolidating shared context, simplifying instructions, and focusing on workflow rather than implementation details, we can reduce cognitive load by 60%+ while maintaining all functionality.

**Recommended approach:** Implement high-priority items first, test thoroughly, then proceed with medium-priority optimizations.
