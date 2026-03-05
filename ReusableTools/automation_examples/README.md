# Automation Examples

This folder contains example Python scripts that demonstrate how to automate FSM testing with Playwright.

## Purpose

These are **reference examples** for developers who want to:
- Automate browser interactions with FSM
- Capture screenshots automatically during testing
- Generate TES-070 documents programmatically

## For Functional Consultants

**You don't need these files!** 

Use the simple JSON approach instead:
1. Create test scenarios in `TestScripts/` folder (JSON files)
2. Run `python ReusableTools/generate_tes070_from_json.py <your_json_file>`
3. Get your TES-070 document automatically

See `TestScripts/README_FOR_CONSULTANTS.md` for details.

## For Developers

These examples show how to:
- Use Playwright to navigate FSM UI
- Capture screenshots at each test step
- Build test scenarios programmatically
- Generate TES-070 documents from test execution

### Example: GL Transaction Interface Test

`test_gl_transaction_interface.py` demonstrates:
- Reading credentials from `Credentials/` folder
- Defining test scenarios in code
- Placeholder for Playwright automation
- Automatic TES-070 generation

### Running Examples

```bash
python ReusableTools/automation_examples/test_gl_transaction_interface.py
```

Note: Playwright automation is not yet implemented - these are structural examples.
