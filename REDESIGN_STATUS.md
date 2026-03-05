# FSM Testing Framework Redesign Status

## Date: March 5, 2026

## ✅ COMPLETED: Phase 1 - Playwright Integration

### What Was Done

1. **Installed Python Playwright**
   - Package: `playwright==1.58.0`
   - Browser: Chromium installed
   - Status: ✅ Working

2. **Rewrote Playwright Client**
   - File: `ReusableTools/testing_framework/integration/playwright_client.py`
   - Replaced: Playwright MCP imports → Python Playwright
   - Methods: navigate, click, fill, type_text, wait_for_selector, screenshot, etc.
   - Status: ✅ Complete and tested

3. **Created Standalone Runner**
   - File: `ReusableTools/run_approval_tests.py`
   - Features:
     * Command-line arguments (--client, --scenario, --headless)
     * Credential loading from .env files
     * Browser automation with Python Playwright
     * Screenshot capture
     * Evidence folder management
   - Status: ✅ Working (tested successfully)

4. **Validated End-to-End**
   - Test: Navigated to FSM login page
   - Result: ✅ Browser launched, page loaded, screenshot captured
   - Evidence: `Projects/SONH/Temp/evidence/test/01_login_page.png`

### Key Changes from Original Design

| Aspect | Original (MCP) | New (Python Playwright) |
|--------|----------------|-------------------------|
| **Import** | `from kiro import mcp_playwright_*` | `from playwright.sync_api import *` |
| **Execution** | Must run in Kiro context | Standalone `python script.py` |
| **Selectors** | Accessibility snapshots + refs | CSS selectors + text selectors |
| **Browser** | Managed by MCP server | Managed by Python script |
| **Visibility** | Hidden (MCP controlled) | Visible or headless (configurable) |

### Benefits Achieved

1. ✅ **Standalone Execution** - Runs as `python script.py`
2. ✅ **No Kiro Dependency** - Works outside Kiro environment
3. ✅ **Visible Browser** - Can watch execution in real-time
4. ✅ **Standard Patterns** - Uses standard Playwright API
5. ✅ **Easier Debugging** - Standard CSS selectors
6. ✅ **Testable** - Can run unit tests independently

---

## 🚧 IN PROGRESS: Phase 2 - FSM Action Handlers

### What Needs to Be Done

The FSM action handlers need to be updated to use CSS selectors instead of accessibility snapshots:

#### 1. FSM Login Action
**File**: `ReusableTools/testing_framework/actions/fsm/fsm_login.py`

**Current**: Uses MCP snapshot parsing
**Needed**: Use CSS/text selectors

**Implementation**:
```python
def fsm_login(playwright_client, url, username, password, auth_method="Cloud Identities"):
    # Navigate
    playwright_client.navigate(url)
    
    # Select auth method
    playwright_client.click('text="Cloud Identities"')
    
    # Enter email
    playwright_client.wait_for_selector('input[type="email"]')
    playwright_client.fill('input[type="email"]', username)
    playwright_client.click('button:has-text("Next")')
    
    # Enter password
    playwright_client.wait_for_selector('input[type="password"]')
    playwright_client.fill('input[type="password"]', password)
    playwright_client.click('button:has-text("Sign In")')
    
    # Wait for portal
    playwright_client.wait_for_selector('text="Applications"', timeout=60000)
```

#### 2. FSM Payables Action
**File**: `ReusableTools/testing_framework/actions/fsm/fsm_payables.py`

**Operations Needed**:
- `navigate_to_payables` - Navigate from portal to Payables app
- `create_invoice` - Fill invoice form with test data
- `submit_for_approval` - Click Submit for Approval button

**Key Selectors to Discover**:
- Sidebar menu button
- "Financials & Supply Management" link
- "Payables" link
- "Create Invoice" button
- Form fields (Company, Vendor, Invoice Number, etc.)
- "Submit for Approval" button

#### 3. FSM Work Units Action
**File**: `ReusableTools/testing_framework/actions/fsm/fsm_workunits.py`

**Operations Needed**:
- `navigate` - Navigate to Work Units page
- `wait_for_completion` - Poll work unit status until complete
- `verify_status` - Check final work unit status

**Key Selectors to Discover**:
- "Process Server Administrator" link
- "Work Units" link
- Work unit table rows
- Status column
- Process name column

---

## 📋 TODO: Phase 3 - Complete Integration

### Remaining Tasks

1. **Update FSM Action Handlers** (2-3 hours)
   - [ ] Implement `fsm_login.py` with CSS selectors
   - [ ] Implement `fsm_payables.py` with CSS selectors
   - [ ] Implement `fsm_workunits.py` with CSS selectors
   - [ ] Test each action individually

2. **Update Test Orchestrator** (30 min)
   - [ ] Replace `PlaywrightMCPClient` with `PlaywrightClient`
   - [ ] Update initialization to pass `headless` parameter
   - [ ] Ensure browser stays open across scenarios
   - [ ] Test orchestrator with one scenario

3. **Update Approval Step 2 Hook** (15 min)
   - [ ] Change execution from MCP-based to standalone script
   - [ ] Update instructions to run: `python ReusableTools/run_approval_tests.py`
   - [ ] Remove MCP-specific notes
   - [ ] Test hook execution

4. **Implement Full Test Runner** (1 hour)
   - [ ] Expand `run_approval_tests.py` to execute all scenarios
   - [ ] Implement evidence collection
   - [ ] Implement TES-070 generation
   - [ ] Add error handling and recovery

5. **End-to-End Testing** (1-2 hours)
   - [ ] Test with 1 scenario
   - [ ] Test with 3 scenarios
   - [ ] Test with all 21 scenarios
   - [ ] Verify TES-070 generation
   - [ ] Verify evidence collection

---

## 🎯 Current Status

**Phase 1**: ✅ COMPLETE (Playwright integration working)
**Phase 2**: 🚧 IN PROGRESS (FSM actions need implementation)
**Phase 3**: ⏳ PENDING (Integration and testing)

**Estimated Time to Complete**: 4-6 hours

---

## 🔄 Data Flow Between Hooks

### Step 1 → Step 2
- **Input**: TES-070 Word document
- **Output**: `Projects/{Client}/TestScripts/approval/{EXT_ID}_auto_approval_test.json`
- **Status**: ✅ Working (already implemented)

### Step 2 → Step 3
- **Input**: JSON file from Step 1
- **Output**: 
  - TES-070: `Projects/{Client}/TES-070/Generated_TES070s/TES-070_{timestamp}_{EXT_ID}.docx`
  - Evidence: `Projects/{Client}/Temp/evidence/{scenario_id}/`
- **Status**: 🚧 In Progress (runner created, actions needed)

### Step 3 Review
- **Input**: TES-070 and evidence from Step 2
- **Output**: Reviewed and finalized document
- **Status**: ✅ Working (already implemented)

---

## 📝 Next Immediate Steps

1. **Discover FSM Selectors** - Use browser DevTools to find CSS selectors for:
   - Login form elements
   - Navigation menu items
   - Payables form fields
   - Work Units table elements

2. **Implement FSM Login** - Complete the login action handler

3. **Test Login** - Verify login works end-to-end

4. **Implement Payables** - Complete the payables action handler

5. **Test Invoice Creation** - Verify invoice creation works

6. **Implement Work Units** - Complete the work units action handler

7. **Test Full Scenario** - Run one complete scenario end-to-end

8. **Scale to All Scenarios** - Run all 21 scenarios

---

## 🎉 Success Criteria

- [x] Python Playwright installed and working
- [x] Playwright client rewritten and tested
- [x] Standalone runner created and tested
- [x] Browser launches and navigates successfully
- [ ] FSM login automation working
- [ ] Payables navigation working
- [ ] Invoice creation working
- [ ] Work unit monitoring working
- [ ] Evidence collection working
- [ ] TES-070 generation working
- [ ] All 21 scenarios execute successfully
- [ ] Hooks work sequentially (Step 1 → Step 2 → Step 3)

---

## 📊 Progress Summary

**Overall Progress**: 30% Complete

- Phase 1 (Playwright): 100% ✅
- Phase 2 (FSM Actions): 0% 🚧
- Phase 3 (Integration): 0% ⏳

**Estimated Completion**: 4-6 hours of focused development

---

## 🚀 Ready for Next Phase

The foundation is solid. Python Playwright is working perfectly. Now we need to implement the FSM-specific automation logic using standard CSS selectors.

**Recommendation**: Proceed with implementing FSM login action first, then test it thoroughly before moving to Payables and Work Units.

