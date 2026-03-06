#!/usr/bin/env python3
"""
Standalone approval test runner using Python Playwright and Test Orchestrator
"""
import sys
import argparse
import logging
from pathlib import Path

# Add ReusableTools to path
sys.path.insert(0, str(Path(__file__).parent))

from testing_framework.orchestration.test_orchestrator import TestOrchestrator
from testing_framework.utils.logger import Logger


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Run FSM approval tests')
    parser.add_argument('--client', required=True, help='Client name (e.g., SONH)')
    parser.add_argument('--scenario', required=True, help='Path to scenario JSON file')
    parser.add_argument('--environment', required=True, help='FSM environment (e.g., ACUITY_TST)')
    parser.add_argument('--url', help='FSM Portal URL (overrides credential file)')
    parser.add_argument('--username', help='FSM Username (overrides credential file)')
    parser.add_argument('--password', help='FSM Password (overrides credential file)')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    args = parser.parse_args()
    
    # Initialize logger
    logger = Logger('approval_test', level=logging.DEBUG if args.headless else logging.INFO)
    
    print('='*80)
    print('FSM APPROVAL TEST EXECUTION')
    print('='*80)
    
    # Validate scenario file exists
    scenario_path = Path(args.scenario)
    if not scenario_path.exists():
        print(f'ERROR: Scenario file not found: {scenario_path}')
        return 1
    
    print(f'\nClient: {args.client}')
    print(f'Environment: {args.environment}')
    print(f'Scenario: {scenario_path}')
    print(f'Headless: {args.headless}')
    
    # Initialize orchestrator
    print('\n[1/3] Initializing test orchestrator...')
    orchestrator = TestOrchestrator(
        client_name=args.client,
        environment=args.environment,
        logger=logger,
        headless=args.headless
    )
    
    # Override credentials if provided via command line
    if args.url and args.username and args.password:
        print('Using credentials from command-line arguments')
        orchestrator.state.set('fsm_url', args.url)
        orchestrator.state.set('fsm_username', args.username)
        orchestrator.state.set('password', args.password)
    
    try:
        # Execute tests
        print('\n[2/3] Executing test scenarios...')
        print('[*] Test execution in progress - watch the browser window for activity')
        print('    (If browser appears stuck, check the console for detailed logs)')
        
        result = orchestrator.run(str(scenario_path))
        
        # Display results
        print('\n[3/3] Test execution complete!')
        print('\n' + '='*80)
        print('TEST RESULTS')
        print('='*80)
        print(f'\nExtension: {result.interface_id}')
        print(f'Status: {"[PASSED]" if result.passed else "[FAILED]"}')
        print(f'Scenarios Executed: {len(result.scenario_results)}')
        
        # Show per-scenario results
        print('\nScenario Results:')
        for scenario_result in result.scenario_results:
            status_icon = '[PASS]' if scenario_result.passed else '[FAIL]'
            print(f'  {status_icon} Scenario {scenario_result.scenario_id}: {scenario_result.title}')
            
            # Show step details if scenario failed
            if not scenario_result.passed:
                print(f'      Failed steps:')
                for step_result in scenario_result.step_results:
                    if not step_result.passed:
                        error_msg = getattr(step_result, 'error', 'Unknown error')
                        print(f'        - Step {step_result.step_number}: {error_msg}')
        
        # Show TES-070 path if generated
        if hasattr(result, 'tes070_path') and result.tes070_path:
            print(f'\n[TES-070] Document: {result.tes070_path}')
            print('   Open in Microsoft Word and press F9 to update Table of Contents')
        
        print('\n' + '='*80)
        
        return 0 if result.passed else 1
        
    except Exception as e:
        logger.error(f'Test execution failed: {str(e)}')
        print(f'\n[ERROR] {str(e)}')
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        print('\nCleaning up...')
        orchestrator.cleanup()
        print('[OK] Cleanup complete')


if __name__ == '__main__':
    sys.exit(main())
