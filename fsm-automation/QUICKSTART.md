# Quick Start Guide

Get the FSM automation framework running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- FSM credentials

## Setup Steps

### 1. Navigate to Framework Directory

```bash
cd fsm-automation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Credentials

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
FSM_URL=https://mingle-portal.inforcloudsuite.com/v2/NMR2N66J9P445R7P_AX4
FSM_USERNAME=Frederic.Sinconegue@infor.com
FSM_PASSWORD=L@ws0n678
HEADLESS=False
SLOW_MO=400
SECOND_MONITOR_X=1920
```

### 4. Run Proof-of-Concept Test

```bash
pytest tests/approvals/test_ext_fin_004.py -v
```

You should see:
- Browser opens on second monitor
- Automated login to FSM
- Navigation to Payables
- Invoice creation
- Approval submission
- Work unit verification

### 5. View Allure Report

```bash
allure serve reports/allure-results
```

This opens a web browser with:
- Test execution summary
- Screenshots at each step
- Pass/fail status
- Execution timeline

## Expected Output

```
tests/approvals/test_ext_fin_004.py::TestEXTFIN004::test_ghr_auto_approval PASSED [100%]

========================= 1 passed in 45.23s =========================
```

## Troubleshooting

### Browser doesn't open on second monitor

Update `SECOND_MONITOR_X` in `.env`:
- Single monitor: `0`
- Second monitor on right: `1920` (or your monitor width)
- Second monitor on left: `-1920`

### Credentials error

Verify `.env` file exists and contains correct credentials.

### Playwright not installed

Run: `playwright install chromium`

### Test fails at login

Check:
1. FSM URL is correct
2. Username/password are valid
3. Network connection is stable

## Next Steps

1. ✅ Verify proof-of-concept works
2. Add more test scenarios
3. Customize page objects for your FSM instance
4. Generate TES-070 documents
5. Integrate with CI/CD

## Getting Help

- Check `README.md` for detailed documentation
- Review page objects in `pages/` directory
- Examine test structure in `tests/approvals/`
- Use Playwright Codegen to discover selectors: `playwright codegen <FSM_URL>`
