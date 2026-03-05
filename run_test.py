import sys
from pathlib import Path
sys.path.insert(0, 'ReusableTools')

from testing_framework.orchestration.test_orchestrator import TestOrchestrator
from testing_framework.utils.logger import Logger

# Read environment
environment = 'ACUITY_TST'
print(f'Environment: {environment}')
print('Starting test execution...')
print()

# Initialize
logger = Logger('approval_test')
orchestrator = TestOrchestrator(
    client_name='SONH',
    environment=environment,
    logger=logger
)

# Run test
try:
    result = orchestrator.run('Projects/SONH/TestScripts/approval/EXT_FIN_004_auto_approval_test.json')
    
    print()
    print('=' * 60)
    print('TEST EXECUTION COMPLETE')
    print('=' * 60)
    print(f'Extension: {result.interface_id}')
    print(f'Scenarios: {len(result.scenario_results)}')
    
    passed = sum(1 for r in result.scenario_results if r.passed)
    failed = len(result.scenario_results) - passed
    
    print(f'Passed: {passed}')
    print(f'Failed: {failed}')
    print(f'Pass Rate: {(passed/len(result.scenario_results)*100):.1f}%')
    
    if hasattr(result, 'tes070_path') and result.tes070_path:
        print(f'TES-070: {result.tes070_path}')
    
finally:
    orchestrator.cleanup()
