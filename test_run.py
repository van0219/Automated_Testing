import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path.cwd()))

from ReusableTools.testing_framework.integration.credential_manager import CredentialManager

# Test configuration
CLIENT = 'SONH'
ENVIRONMENT = 'ACUITY_TST'
OUTPUT_DIR = Path('Projects/SONH/Temp/evidence/login_test')

print('='*60)
print('TEST 1: FSM Login Validation')
print('='*60)

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Load credentials
print('\n[1/7] Loading credentials...')
creds_dir = Path('Projects') / CLIENT / 'Credentials'
cred_manager = CredentialManager(creds_dir)
fsm_creds = cred_manager.get_fsm_credentials(ENVIRONMENT)

url = fsm_creds['url']
username = fsm_creds['username']
print(f'  URL: {url}')
print(f'  Username: {username}')

# Navigate to FSM
print('\n[2/7] Navigating to FSM login page...')
from kiro import mcp_playwright_browser_navigate
mcp_playwright_browser_navigate(url=url)
print('  ✓ Navigation complete')

# Wait for page load
print('\n[3/7] Waiting for page to load...')
from kiro import mcp_playwright_browser_wait_for
mcp_playwright_browser_wait_for(time=5)
print('  ✓ Page loaded')

# Take snapshot
print('\n[4/7] Taking snapshot...')
from kiro import mcp_playwright_browser_snapshot
snapshot = mcp_playwright_browser_snapshot()

# Save snapshot
snapshot_file = OUTPUT_DIR / f'01_login_page_snapshot_{timestamp}.txt'
with open(snapshot_file, 'w', encoding='utf-8') as f:
    f.write(str(snapshot))
print(f'  ✓ Snapshot saved: {snapshot_file}')

# Analyze snapshot
print('\n[5/7] Analyzing snapshot...')
snapshot_text = str(snapshot)
print(f'  Snapshot type: {type(snapshot)}')
print(f'  Snapshot length: {len(snapshot_text)} characters')

if 'Cloud Identities' in snapshot_text:
    print('  ✓ Found "Cloud Identities" in snapshot')
else:
    print('  ✗ "Cloud Identities" not found')

# Show first few lines
lines = snapshot_text.split('\n')
print(f'\n[6/7] First 10 lines of snapshot:')
for i, line in enumerate(lines[:10], 1):
    print(f'  {i}: {line[:100]}')

# Take screenshot
print('\n[7/7] Capturing screenshot...')
from kiro import mcp_playwright_browser_take_screenshot
screenshot_file = OUTPUT_DIR / f'01_login_page_{timestamp}.png'
mcp_playwright_browser_take_screenshot(
    filename=str(screenshot_file),
    type='png',
    fullPage=False
)
print(f'  ✓ Screenshot saved: {screenshot_file}')

# Close browser
print('\nClosing browser...')
from kiro import mcp_playwright_browser_close
mcp_playwright_browser_close()

print('\n' + '='*60)
print('TEST 1: COMPLETED SUCCESSFULLY')
print('='*60)
print(f'\nOutput directory: {OUTPUT_DIR}')
print('\nNext: Review snapshot and screenshot, then proceed to TEST 2')
