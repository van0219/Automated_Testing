#!/usr/bin/env python3
"""
Execute EXT_FIN_004 approva
from pathlib import Path

# Add ReusableTools to path
sys.path.insert(0, 'ReusableTools')

from testing_framework.orchestration.test_orchestrator import TestOrchestrator
from testing_framework.utils.logger import Logger

def main():
    # Initialize logger
    logger = Logger('approval_test', verbose=True)
    
    # Initialize orchestrator
    orchestrator = TestOrchestrator(
        client_name='SONH',
        environment='ACUITY_TST',
        logger=logger
    )
    
    # Run the test
    try:
        result = orchestrator.run('Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json')
        
        print('\n=== TEST RESULT ===')
        print(f'Interface: {result.interface_id}')
        print(f'Status: {"PASSED" if result.passed else "FAILED"}')
        print(f'Scenarios: {len(result.scenario_results)}')
        
        if hasattr(result, 'tes070_path'):
            print(f'TES-070: {result.tes070_path}')
        
        return 0 if result.passed else 1
        
    except Exception as e:
        logger.error(f'Test execution failed: {str(e)}')
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        orchestrator.cleanup()

if __name__ == '__main__':
    sys.exit(main())
