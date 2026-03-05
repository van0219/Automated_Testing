#!/usr/bin/env python3
"""
Execute EXT_FIN_004 approval tests directly in Kiro context
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add ReusableTools to path
sys.path.insert(0, 'ReusableTools')

# Configuration
CLIENT = 'SONH'
SCENARIO_FILE = 'Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json'
CREDS_DIR = Path('Projects/SONH/Credentials')

print('='*60)
print('EXT_FIN_004 APPROVAL TEST EXECUTION')
print('='*60)

# Load test scenarios
print('\n[1/5] Loading test scenarios...')
with open(SCENARIO_FILE, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

extension_id = test_data['extension_id']
scenarios = test_data['scenarios']
print(f'  Extension: {extension_id}')
print(f'  Scenarios: {len(scenarios)}')

# Load credentials
print('\n[2/5] Loading credentials...')
env_file = CREDS_DIR / '.env.fsm'
password_file = CREDS_DIR / '.env.passwords'

# Parse credentials (using SONH_ prefix, not environment name)
fsm_url = None
fsm_username = None
fsm_password = None

with open(env_file, 'r') as f:
    for line in f:
        if 'SONH_URL=' in line:
            fsm_url = line.split('=', 1)[1].strip()
        elif 'SONH_USERNAME=' in line:
            fsm_username = line.split('=', 1)[1].strip()

with open(password_file, 'r') as f:
    for line in f:
        if 'SONH_PASSWORD=' in line:
            fsm_password = line.split('=', 1)[1].strip()

if not all([fsm_url, fsm_username, fsm_password]):
    print('  ✗ ERROR: Missing credentials')
    sys.exit(1)

print(f'  URL: {fsm_url}')
print(f'  Username: {fsm_username}')
print('  Password: [REDACTED]')

# Generate unique run group
run_group = f"AUTOTEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
print(f'\n[3/5] Test run group: {run_group}')

# Import MCP tools
print('\n[4/5] Importing Playwright MCP tools...')
try:
    from kiro import (
        mcp_playwright_browser_navigate,
        mcp_playwright_browser_snapshot,
        mcp_playwright_browser_click,
        mcp_playwright_browser_type,
        mcp_playwright_browser_wait_for,
        mcp_playwright_browser_take_screenshot,
        mcp_playwright_browser_close
    )
    print('  ✓ MCP tools imported successfully')
except ImportError as e:
    print(f'  ✗ ERROR: Cannot import MCP tools: {e}')
    print('  This script must run in Kiro execution context')
    sys.exit(1)

# Execute first scenario as test
print('\n[5/5] Executing first scenario as test...')
scenario = scenarios[0]
print(f'  Scenario {scenario["scenario_id"]}: {scenario["title"]}')

# Navigate to FSM
print('\n  Step 1: Navigating to FSM...')
mcp_playwright_browser_navigate(url=fsm_url)
mcp_playwright_browser_wait_for(time=3)
print('    ✓ Navigation complete')

# Take snapshot
print('\n  Step 2: Taking snapshot...')
snapshot = mcp_playwright_browser_snapshot()
print(f'    ✓ Snapshot captured ({len(str(snapshot))} chars)')

# Check for login page
snapshot_text = str(snapshot)
if 'Cloud Identities' in snapshot_text:
    print('    ✓ Login page detected')
else:
    print('    ⚠ Login page not detected - may already be logged in')

print('\n' + '='*60)
print('TEST EXECUTION: INITIAL VALIDATION COMPLETE')
print('='*60)
print('\nNext steps:')
print('1. Complete login automation')
print('2. Navigate to Payables')
print('3. Create invoice')
print('4. Submit for approval')
print('5. Monitor work unit')
print('6. Capture evidence')
print('7. Generate TES-070')

# Close browser
print('\nClosing browser...')
mcp_playwright_browser_close()
print('✓ Browser closed')
