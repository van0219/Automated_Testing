"""Inbound interface test executor"""

import random
import string
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..engine.step_engine import StepEngine
from ..engine.test_state import TestState
from ..engine.results import ScenarioResult
from ..utils.logger import Logger


class InboundExecutor:
    """
    Execute inbound interface test scenarios.
    
    Generates unique identifiers and executes test steps sequentially.
    """
    
    def __init__(self, step_engine: StepEngine, state: TestState, logger: Optional[Logger] = None):
        """
        Initialize inbound executor.
        
        Args:
            step_engine: StepEngine for step execution
            state: TestState for variable management
            logger: Optional logger instance
        """
        self.step_engine = step_engine
        self.state = state
        self.logger = logger
    
    def execute_scenario(self, scenario: Dict[str, Any]) -> ScenarioResult:
        """
        Execute single test scenario.
        
        Args:
            scenario: Scenario configuration with id, title, description, steps
        
        Returns:
            ScenarioResult with pass/fail status and step results
        """
        scenario_id = scenario.get('scenario_id', 'Unknown')
        title = scenario.get('title', '')
        steps = scenario.get('steps', [])
        
        if self.logger:
            self.logger.info(f"Executing scenario {scenario_id}: {title}")
        
        # Generate unique run_group identifier
        run_group = self._generate_run_group()
        self.state.set('run_group', run_group)
        
        if self.logger:
            self.logger.info(f"Generated run_group: {run_group}")
        
        # Execute steps sequentially
        step_results = []
        all_passed = True
        
        for step_config in steps:
            step_number = step_config.get('number', 0)
            
            if self.logger:
                self.logger.info(f"Executing step {step_number}")
            
            try:
                step_result = self.step_engine.execute_step(step_config)
                step_results.append(step_result)
                
                if not step_result.passed:
                    all_passed = False
                    if self.logger:
                        self.logger.warning(f"Step {step_number} failed")
                    # Continue with remaining steps even if one fails
                    
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Step {step_number} error: {str(e)}")
                all_passed = False
                # Continue with remaining steps
        
        # Build scenario result
        result = ScenarioResult(
            scenario_id=scenario_id,
            title=title,
            step_results=step_results,
            passed=all_passed
        )
        
        if self.logger:
            status = "PASSED" if all_passed else "FAILED"
            self.logger.info(f"Scenario {scenario_id} {status}")
        
        return result
    
    def _generate_run_group(self) -> str:
        """
        Generate unique run_group identifier.
        
        Format: AUTOTEST_<timestamp>_<random>
        Example: AUTOTEST_20260305103045_A7B9C2
        
        Returns:
            Unique run_group string
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"AUTOTEST_{timestamp}_{random_suffix}"
