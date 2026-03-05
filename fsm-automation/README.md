# FSM Automated Testing Framework

Modern FSM regression testing framework using Python, Playwright, PyTest, and Allure Reports.

## Architecture

```
fsm-automation/
├── tests/              # Test files organized by module
├── pages/              # Page Object Model classes
├── fixtures/           # PyTest fixtures
├── data/               # Test data files
├── utils/              # Utility scripts
├── reports/            # Test reports and screenshots
├── pytest.ini          # PyTest configuration
├── conftest.py         # Shared fixtures
└── requirements.txt    # Python dependencies
```

## Installation

### 1. Install Python Dependencies

```bash
cd fsm-automation
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Configure Credentials

Copy `.env.example` to `.env` and update with your FSM credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
FSM_URL=https://your-fsm-portal.com
FSM_USERNAME=your.email@infor.com
FSM_PASSWORD=your_password
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/approvals/test_ext_fin_004.py
```

### Run Specific Test

```bash
pytest tests/approvals/test_ext_fin_004.py::TestEXTFIN004::test_ghr_auto_approval
```

### Run with Markers

```bash
# Run only approval tests
pytest -m approval

# Run smoke tests
pytest -m smoke
```

## Viewing Reports

### Generate and Open Allure Report

```bash
allure serve reports/allure-results
```

This will:
1. Generate the Allure report
2. Start a local web server
3. Open the report in your browser

### Allure Report Features

- Test execution summary
- Test steps with screenshots
- Execution timeline
- Error stack traces
- Test history and trends

## Browser Configuration

The framework runs in headed mode by default with the browser visible on your second monitor.

Configuration in `.env`:
```
HEADLESS=False          # Set to True for headless mode
SLOW_MO=400            # Slow down actions by 400ms
SECOND_MONITOR_X=1920  # X position for second monitor
```

## Page Object Model

Page objects encapsulate FSM screen interactions:

- `LoginPage` - FSM login and authentication
- `PayablesPage` - Invoice creation and submission
- `WorkUnitsPage` - Work unit monitoring and verification

## Test Structure

Each test follows this pattern:

```python
@allure.feature("Module Name")
@allure.story("Test Story")
@pytest.mark.marker_name
class TestClassName:
    
    @allure.title("Test Title")
    @allure.description("Test description")
    def test_scenario_name(self, page, credentials):
        # Initialize page objects
        # Execute test steps
        # Verify results
        # Attach evidence to Allure
```

## Selector Strategy

Use Playwright's semantic selectors:

```python
# Preferred
page.get_by_role("button", name="Create Invoice")
page.get_by_text("Submit for Approval")
page.get_by_label("Company")

# Fallback
page.locator('button:has-text("Create")')
```

## Discovering Selectors

Use Playwright Codegen to record interactions:

```bash
playwright codegen https://your-fsm-url.com
```

This opens a browser and records your actions, generating selector code.

## TES-070 Generation

TES-070 documents can be generated from test results:

```bash
python utils/tes070_generator.py --test-results reports/allure-results
```

Output: `reports/TES070/EXT_FIN_004_TES070.docx`

## Troubleshooting

### Browser Not Opening on Second Monitor

Update `SECOND_MONITOR_X` in `.env` to match your monitor setup.

### Selectors Not Found

1. Use Playwright Inspector: `pytest --headed --slowmo=1000`
2. Use Codegen to discover selectors
3. Check if FSM UI has changed

### Tests Timing Out

Increase timeouts in page objects or use `--timeout` flag:

```bash
pytest --timeout=300 tests/
```

## Next Steps

1. Run the proof-of-concept test
2. Verify Allure report generation
3. Add more approval scenarios
4. Expand to other FSM modules (Payables, GL, Cash)

## Support

For issues or questions, refer to:
- Playwright docs: https://playwright.dev/python/
- PyTest docs: https://docs.pytest.org/
- Allure docs: https://docs.qameta.io/allure/
