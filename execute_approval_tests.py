#!/usr/bin/env python3
"""
Interactive wrapper for running FSM approval tests.
Prompts for credentials and executes tests with real-time progress reporting.
"""
import subprocess
import sys
from pathlib import Path


def main():
    """Main execution function"""
    print('='*80)
    print('FSM APPROVAL TEST RUNNER')
    print('='*80)
    
    # Fixed parameters
    client = 'SONH'
    scenario = 'Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json'
    
    # Verify scenario file exists
    if not Path(scenario).exists():
        print(f'\n❌ ERROR: Scenario file not found: {scenario}')
        return 1
    
    print(f'\nClient: {client}')
    print(f'Scenario: {scenario}')
    
    # Prompt for credentials
    print('\n' + '='*80)
    print('CREDENTIALS')
    print('='*80)
    
    url = input('\n1. FSM Portal URL: ').strip()
    username = input('2. FSM Username: ').strip()
    password = input('3. FSM Password: ').strip()
    
    if not url or not username or not password:
        print('\n❌ ERROR: All credentials are required')
        return 1
    
    # Build command
    cmd = [
        sys.executable,  # Use same Python interpreter
        'ReusableTools/run_approval_tests_v2.py',
        '--client', client,
        '--scenario', scenario,
        '--environment', 'SONH',
        '--url', url,
        '--username', username,
        '--password', password
    ]
    
    print('\n' + '='*80)
    print('STARTING TEST EXECUTION')
    print('='*80)
    print('\n⏳ Launching browser and executing tests...')
    print('   Watch the browser window for activity')
    print('   Progress will be reported below:\n')
    
    # Execute command
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print('\n\n⚠️  Test execution interrupted by user')
        return 130
    except Exception as e:
        print(f'\n❌ ERROR: {str(e)}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
