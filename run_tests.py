#!/usr/bin/env python3
"""
FSM Testing Framework - CLI Entry Point

Usage:
    python run_tests.py --scenario path/to/scenario.json --client SONH --environment ACUITY_TST
    python run_tests.py --scenario path/to/scenario.json --client SONH --verbose
"""

import argparse
import sys
import logging
from pathlib import Path
from ReusableTools.testing_framework.orchestration.test_orchestrator import TestOrchestrator
from ReusableTools.testing_framework.utils.logger import StructuredLogger


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FSM Testing Framework - Execute automated test scenarios"
    )
    parser.add_argument(
        "--scenario",
        required=True,
        help="Path to JSON test scenario file"
    )
    parser.add_argument(
        "--client",
        required=True,
        help="Client name (e.g., SONH)"
    )
    parser.add_argument(
        "--environment",
        default="ACUITY_TST",
        help="FSM environment (default: ACUITY_TST)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Validate scenario file exists
    scenario_path = Path(args.scenario)
    if not scenario_path.exists():
        print(f"Error: Scenario file not found: {args.scenario}")
        sys.exit(1)
    
    # Initialize logger
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = StructuredLogger("TestRunner", None, getattr(logging, log_level))
    
    # Execute tests
    orchestrator = None
    try:
        logger.info("="*60)
        logger.info("FSM TESTING FRAMEWORK")
        logger.info("="*60)
        logger.info(f"Client: {args.client}")
        logger.info(f"Environment: {args.environment}")
        logger.info(f"Scenario: {args.scenario}")
        logger.info("="*60)
        
        orchestrator = TestOrchestrator(args.client, args.environment, logger)
        result = orchestrator.run(str(scenario_path))
        
        # Print results
        print("\n" + "="*60)
        print("TEST EXECUTION COMPLETE")
        print("="*60)
        print(f"Interface: {result.interface_id}")
        print(f"Scenarios: {len(result.scenario_results)}")
        
        passed_count = sum(1 for s in result.scenario_results if s.passed)
        failed_count = len(result.scenario_results) - passed_count
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")
        
        print(f"Status: {'PASSED' if result.passed else 'FAILED'}")
        
        if hasattr(result, 'tes070_path') and result.tes070_path:
            print(f"TES-070: {result.tes070_path}")
        
        print("="*60 + "\n")
        
        # Cleanup
        if orchestrator:
            orchestrator.cleanup()
        
        sys.exit(0 if result.passed else 1)
        
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        print(f"\nError: {str(e)}")
        
        # Cleanup
        if orchestrator:
            try:
                orchestrator.cleanup()
            except:
                pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
