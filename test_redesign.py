#!/usr/bin/env python3
"""
Quick validation test for redesigned framework
"""
import sys
from pathlib import Path

# Add ReusableTools to path
sys.path.insert(0, 'ReusableTools')

from testing_framework.integration.playwright_client import PlaywrightClient
from testing_framework.actions.fsm.fsm_login import FSMLoginAction
from testing_framework.engine.test_state import TestState
from testing_framework.utils.logger import Logger


def test_playwright_client():
    """Test PlaywrightClient initialization"""
    print('\n[TEST 1] PlaywrightClient Initialization')
    print('-' * 60)
    
    logger = Logger('test', verbose=True)
    client = PlaywrightClient(logger=logger, headless=False, screen=2)
    
    try:
        client.connect()
        print('✅ PlaywrightClient connected successfully')
        
        # Test navigation
        client.navigate('https://www.google.com')
        print('✅ Navigation working')
        
        # Test screenshot
        screenshot_path = 'test_screenshot.png'
        client.screenshot(screenshot_path)
        print(f'✅ Screenshot captured: {screenshot_path}')
        
        return True
        
    except Exception as e:
        print(f'❌ PlaywrightClient test failed: {str(e)}')
        return False
        
    finally:
        client.close()
        print('✅ PlaywrightClient closed')


def test_fsm_login():
    """Test FSM Login action"""
    print('\n[TEST 2] FSM Login Action')
    print('-' * 60)
    
    # Load credentials
    creds_file = Path('Projects/SONH/Credentials/.env.fsm')
    password_file = Path('Projects/SONH/Credentials/.env.passwords')
    
    if not creds_file.exists():
        print('❌ Credentials file not found')
        return False
    
    if not password_file.exists():
        print('❌ Password file not found')
        return False
    
    # Parse credentials
    fsm_url = None
    fsm_username = None
    fsm_password = None
    
    with open(creds_file, 'r') as f:
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
        print('❌ Missing credentials')
        print(f'  URL: {"✓" if fsm_url else "✗"}')
        print(f'  Username: {"✓" if fsm_username else "✗"}')
        print(f'  Password: {"✓" if fsm_password else "✗"}')
        return False
    
    print(f'✅ Credentials loaded')
    print(f'  URL: {fsm_url}')
    print(f'  Username: {fsm_username}')
    
    # Test login
    logger = Logger('test', verbose=True)
    client = PlaywrightClient(logger=logger, headless=False, screen=2)
    
    try:
        client.connect()
        print('✅ Browser connected')
        
        # Create login action
        login_action = FSMLoginAction(client, logger)
        
        # Execute login
        config = {
            'url': fsm_url,
            'username': fsm_username,
            'password': fsm_password,
            'auth_method': 'Cloud Identities'
        }
        
        state = TestState()
        result = login_action.execute(config, state)
        
        if result.success:
            print('✅ FSM Login successful!')
            
            # Take screenshot
            screenshot_path = 'test_fsm_portal.png'
            client.screenshot(screenshot_path)
            print(f'✅ Screenshot captured: {screenshot_path}')
            
            return True
        else:
            print(f'❌ FSM Login failed: {result.message}')
            return False
        
    except Exception as e:
        print(f'❌ FSM Login test failed: {str(e)}')
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        input('\nPress Enter to close browser...')
        client.close()
        print('✅ Browser closed')


def main():
    """Run all tests"""
    print('='*60)
    print('FSM TESTING FRAMEWORK REDESIGN VALIDATION')
    print('='*60)
    
    results = []
    
    # Test 1: PlaywrightClient
    results.append(('PlaywrightClient', test_playwright_client()))
    
    # Test 2: FSM Login
    results.append(('FSM Login', test_fsm_login()))
    
    # Summary
    print('\n' + '='*60)
    print('TEST SUMMARY')
    print('='*60)
    
    for test_name, passed in results:
        status = '✅ PASSED' if passed else '❌ FAILED'
        print(f'{test_name}: {status}')
    
    all_passed = all(result[1] for result in results)
    
    print('\n' + '='*60)
    if all_passed:
        print('🎉 ALL TESTS PASSED - REDESIGN VALIDATED!')
    else:
        print('❌ SOME TESTS FAILED - REVIEW ERRORS ABOVE')
    print('='*60)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
