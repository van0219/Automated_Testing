#!/usr/bin/env python3
"""
Standalone approval test runner using Python Playwright
"""
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add ReusableTools to path
sys.path.insert(0, str(Path(__file__).parent))

from testing_framework.integration.playwright_client import PlaywrightClient
from testing_framework.integration.credential_manager import CredentialManager
from testing_framework.utils.logger import Logger


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Run FSM approval tests')
    parser.add_argument('--client', required=True, help='Client name (e.g., SONH)')
    parser.add_argument('--scenario', required=True, help='Path to scenario JSON file')
    parser.add_argument('--headless', default='false', help='Run browser in headless mode')
    parser.add_argument('--screen', type=int, default=2, help='Screen number to display browser (default: 2)')
    args = parser.parse_args()
    
    # Initialize logger
    logger = Logger('approval_test')
    
    print('='*60)
    print('FSM APPROVAL TEST EXECUTION')
    print('='*60)
    
    # Load scenario file
    print(f'\n[1/6] Loading test scenarios...')
    scenario_path = Path(args.scenario)
    if not scenario_path.exists():
        print(f'ERROR: Scenario file not found: {scenario_path}')
        return 1
    
    with open(scenario_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    extension_id = test_data.get('extension_id', 'UNKNOWN')
    scenarios = test_data.get('scenarios', [])
    print(f'  Extension: {extension_id}')
    print(f'  Scenarios: {len(scenarios)}')
    
    # Load credentials
    print(f'\n[2/6] Loading credentials...')
    creds_dir = Path('Projects') / args.client / 'Credentials'
    if not creds_dir.exists():
        print(f'ERROR: Credentials directory not found: {creds_dir}')
        return 1
    
    # Read credentials using client name prefix
    env_file = creds_dir / '.env.fsm'
    password_file = creds_dir / '.env.passwords'
    
    fsm_url = None
    fsm_username = None
    fsm_password = None
    
    # Parse credentials (using client name prefix, e.g., SONH_)
    prefix = f'{args.client.upper()}_'
    
    with open(env_file, 'r') as f:
        for line in f:
            if f'{prefix}URL=' in line:
                fsm_url = line.split('=', 1)[1].strip()
            elif f'{prefix}USERNAME=' in line:
                fsm_username = line.split('=', 1)[1].strip()
    
    with open(password_file, 'r') as f:
        for line in f:
            if f'{prefix}PASSWORD=' in line:
                fsm_password = line.split('=', 1)[1].strip()
    
    if not all([fsm_url, fsm_username, fsm_password]):
        print('ERROR: Missing credentials')
        print(f'  URL: {"✓" if fsm_url else "✗"}')
        print(f'  Username: {"✓" if fsm_username else "✗"}')
        print(f'  Password: {"✓" if fsm_password else "✗"}')
        return 1
    
    print(f'  URL: {fsm_url}')
    print(f'  Username: {fsm_username}')
    print(f'  Password: [REDACTED]')
    
    # Generate unique run group
    run_group = f"AUTOTEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f'\n[3/6] Test run group: {run_group}')
    
    # Create evidence directory
    evidence_dir = Path('Projects') / args.client / 'Temp' / 'evidence' / 'test'
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize Playwright
    print(f'\n[4/6] Starting browser...')
    headless = args.headless.lower() == 'true'
    playwright_client = PlaywrightClient(logger=logger, headless=headless, screen=args.screen)
    
    try:
        playwright_client.connect()
        print(f'  ✓ Browser started (headless={headless}, screen={args.screen}, incognito=True, maximized=True)')
        
        # Navigate to FSM
        print(f'\n[5/6] Navigating to FSM...')
        playwright_client.navigate(fsm_url)
        print(f'  ✓ Navigation complete')
        
        # Wait for page load
        playwright_client.wait_for_timeout(3000)
        
        # Take initial screenshot
        screenshot_path = evidence_dir / '01_login_page.png'
        playwright_client.screenshot(str(screenshot_path))
        print(f'  ✓ Screenshot saved: {screenshot_path}')
        
        # Check if login page loaded
        print(f'\n[6/6] Testing FSM login...')
        if playwright_client.is_visible('text="Cloud Identities"'):
            print(f'  ✓ Login page detected')
            
            # Test login
            print(f'  → Attempting login...')
            
            # Import and use FSM login action
            sys.path.insert(0, str(Path(__file__).parent))
            from testing_framework.actions.fsm.fsm_login import FSMLoginAction
            
            login_action = FSMLoginAction(playwright_client, logger)
            login_config = {
                'url': fsm_url,
                'username': fsm_username,
                'password': fsm_password,
                'auth_method': 'Cloud Identities'
            }
            
            from testing_framework.engine.test_state import TestState
            test_state = TestState()
            
            result = login_action.execute(login_config, test_state)
            
            if result.success:
                print(f'  ✅ Login successful!')
                print(f'  ✓ FSM portal loaded')
                
                # Take screenshot of portal
                screenshot_path = evidence_dir / '02_fsm_portal.png'
                playwright_client.screenshot(str(screenshot_path))
                print(f'  ✓ Screenshot saved: {screenshot_path}')
            else:
                print(f'  ❌ Login failed: {result.message}')
                return 1
        else:
            print(f'  ⚠ Login page not detected - may already be logged in')
        
        # Take screenshot
        evidence_dir = Path('Projects') / args.client / 'Temp' / 'evidence' / 'test'
        evidence_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = evidence_dir / '01_login_page.png'
        playwright_client.screenshot(str(screenshot_path))
        print(f'  ✓ Screenshot saved: {screenshot_path}')
        
        print('\n' + '='*60)
        print('INITIAL VALIDATION COMPLETE')
        print('='*60)
        print('\nNext steps:')
        print('1. Implement FSM login automation')
        print('2. Implement Payables navigation')
        print('3. Implement invoice creation')
        print('4. Implement approval submission')
        print('5. Implement work unit monitoring')
        print('6. Implement evidence collection')
        print('7. Implement TES-070 generation')
        
        # Keep browser open for inspection
        input('\nPress Enter to close browser...')
        
        return 0
        
    except Exception as e:
        logger.error(f'Test execution failed: {str(e)}')
        print(f'\nERROR: {str(e)}')
        return 1
        
    finally:
        playwright_client.close()
        print('\n✓ Browser closed')


if __name__ == '__main__':
    sys.exit(main())
