# FSM Testing Framework Redesign Plan

## Problem Statement
Current framework tries to import Playwright MCP tools from a non-existent `kiro` module, preventing standalone execution. Framework cannot run as `python script.py`.

## Solution: Use Python Playwright Directly

### Changes Required

#### 1. Replace PlaywrightMCPClient with PlaywrightClient
**File**: `ReusableTools/testing_framework/integration/playwright_client.py`

**Current**: Tries to import from `kiro` module
**New**: Use standard `playwright` Python package

```python
from playwright.sync_api import sync_playwright, Page, Browser

class PlaywrightClient:
    """Browser automation using Python Playwright"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self._connected = False
    
    def connect(self, headless: bool = False):
        """Start Playwright and launch browser"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        self._connected = True
    
    def navigate(self, url: str):
        """Navigate to URL"""
        self.page.goto(url, wait_until='networkidle')
    
    def click(self, selector: str):
        """Click element"""
        self.page.click(selector)
    
    def type_text(self, selector: str, text: str):
        """Type text into element"""
        self.page.fill(selector, text)
    
    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wait for element to appear"""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def screenshot(self, path: str):
        """Take screenshot"""
        self.page.screenshot(path=path)
    
    def get_text(self, selector: str) -> str:
        """Get element text"""
        return self.page.text_content(selector)
    
    def close(self):
        """Close browser and cleanup"""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self._connected = False
```

#### 2. Update FSM Action Handlers
**Files**: 
- `ReusableTools/testing_framework/actions/fsm/fsm_login.py`
- `ReusableTools/testing_framework/actions/fsm/fsm_payables.py`
- `ReusableTools/testing_framework/actions/fsm/fsm_workunits.py`

**Changes**: Use CSS selectors instead of accessibility snapshots

**Example - FSM Login**:
```python
def fsm_login(playwright_client, url, username, password, auth_method="Cloud Identities"):
    """Login to FSM"""
    # Navigate
    playwright_client.navigate(url)
    
    # Select auth method
    if auth_method == "Cloud Identities":
        playwright_client.click('text="Cloud Identities"')
    
    # Wait for login form
    playwright_client.wait_for_selector('input[type="email"]')
    
    # Enter credentials
    playwright_client.type_text('input[type="email"]', username)
    playwright_client.click('button:has-text("Next")')
    
    playwright_client.wait_for_selector('input[type="password"]')
    playwright_client.type_text('input[type="password"]', password)
    playwright_client.click('button:has-text("Sign In")')
    
    # Wait for portal to load
    playwright_client.wait_for_selector('text="Applications"', timeout=60000)
```

#### 3. Install Playwright
**Command**: 
```bash
pip install playwright
playwright install chromium
```

#### 4. Update TestOrchestrator
**File**: `ReusableTools/testing_framework/orchestration/test_orchestrator.py`

**Changes**:
- Replace `PlaywrightMCPClient` with `PlaywrightClient`
- Pass `headless=False` for visible browser during testing
- Ensure browser stays open across scenarios
- Close browser only in `cleanup()`

#### 5. Update Hook Step 2
**File**: `.kiro/hooks/approval-step2-execute-tests.kiro.hook`

**Changes**:
- Remove MCP-specific instructions
- Update to run as standalone Python script
- Ensure output files are saved for Step 3

**New execution**:
```bash
python ReusableTools/run_approval_tests.py \
  --client SONH \
  --scenario Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json \
  --headless false
```

#### 6. Create Standalone Runner Script
**File**: `ReusableTools/run_approval_tests.py`

```python
#!/usr/bin/env python3
"""
Standalone approval test runner
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from testing_framework.orchestration.test_orchestrator import TestOrchestrator
from testing_framework.utils.logger import Logger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', required=True)
    parser.add_argument('--scenario', required=True)
    parser.add_argument('--headless', default='false')
    args = parser.parse_args()
    
    # Initialize
    logger = Logger('approval_test')
    orchestrator = TestOrchestrator(
        client_name=args.client,
        headless=(args.headless.lower() == 'true'),
        logger=logger
    )
    
    # Run
    try:
        result = orchestrator.run(args.scenario)
        
        # Show results
        print(f'\n{"="*60}')
        print(f'TEST EXECUTION COMPLETE')
        print(f'{"="*60}')
        print(f'Extension: {result.interface_id}')
        print(f'Passed: {result.passed_count}/{result.total_count}')
        print(f'Pass Rate: {result.pass_rate:.1f}%')
        print(f'TES-070: {result.tes070_path}')
        print(f'Evidence: {result.evidence_path}')
        
        return 0 if result.passed else 1
        
    finally:
        orchestrator.cleanup()

if __name__ == '__main__':
    sys.exit(main())
```

### Data Flow Between Hooks

**Step 1 → Step 2**:
- Input: TES-070 Word document
- Output: JSON file at `Projects/{Client}/TestScripts/approval/{EXT_ID}_auto_approval_test.json`
- Step 2 reads this JSON file

**Step 2 → Step 3**:
- Input: JSON file from Step 1
- Output: 
  - TES-070 document at `Projects/{Client}/TES-070/Generated_TES070s/TES-070_{timestamp}_{EXT_ID}.docx`
  - Evidence screenshots at `Projects/{Client}/Temp/evidence/{scenario_id}/`
- Step 3 reviews these outputs

### Benefits of Redesign

1. ✅ **Standalone Execution** - Runs as `python script.py`
2. ✅ **No MCP Dependency** - Uses standard Python Playwright
3. ✅ **Visible Browser** - Can watch execution in real-time
4. ✅ **Standard Selectors** - Uses CSS selectors (easier to debug)
5. ✅ **Clear Data Flow** - Each step produces files for next step
6. ✅ **Testable** - Can run outside Kiro environment
7. ✅ **Maintainable** - Standard Playwright patterns

### Implementation Steps

1. Install Playwright: `pip install playwright && playwright install chromium`
2. Rewrite `playwright_client.py` with Python Playwright
3. Update FSM action handlers with CSS selectors
4. Update `test_orchestrator.py` to use new client
5. Create `run_approval_tests.py` standalone runner
6. Update Hook Step 2 to run standalone script
7. Test with one scenario
8. Run full test suite

### Testing Plan

1. **Unit Test**: Test PlaywrightClient methods individually
2. **Integration Test**: Test FSM login action
3. **Scenario Test**: Run one complete scenario
4. **Full Suite**: Run all 21 scenarios
5. **Verify Output**: Check TES-070 and evidence generated correctly

### Timeline

- Playwright client rewrite: 30 min
- FSM action handlers update: 1 hour
- Orchestrator update: 30 min
- Standalone runner: 30 min
- Testing and debugging: 1-2 hours
- **Total**: 3-4 hours

### Next Steps

1. Get approval for redesign approach
2. Install Playwright
3. Begin implementation
4. Test incrementally
5. Update hooks
6. Full execution

