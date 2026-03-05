"""Wait action handler for work unit monitoring"""

from typing import Dict, Any
from .base import BaseAction
from ..engine.test_state import TestState
from ..engine.results import ActionResult
from ..integration.workunit_monitor import WorkUnitMonitor
from ..utils.exceptions import ActionError, TimeoutError as FrameworkTimeoutError
from ..utils.logger import Logger


class WaitAction(BaseAction):
    """
    Wait for work unit creation or completion with adaptive polling.
    
    Monitors work units via UI automation and returns status information.
    """
    
    def __init__(self, workunit_monitor: WorkUnitMonitor, logger: Logger = None):
        """
        Initialize wait action.
        
        Args:
            workunit_monitor: WorkUnitMonitor instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.workunit_monitor = workunit_monitor
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Wait for condition to be met.
        
        Config:
        - target: "work_unit_creation" or "work_unit_completion"
        - process_name: Process name (for creation)
        - timeout_seconds: Max wait time (default 600)
        - poll_interval_override: Optional poll interval override
        
        Returns:
            ActionResult with state_updates: work_unit_id, work_unit_status
        
        Raises:
            ActionError: If wait fails
            FrameworkTimeoutError: If timeout exceeded
        """
        try:
            # Extract configuration
            target = config.get('target')
            timeout_seconds = config.get('timeout_seconds', 600)
            poll_interval_override = config.get('poll_interval_override')
            
            if not target:
                raise ActionError("Missing required field: target")
            
            if target == "work_unit_creation":
                # Wait for work unit creation
                process_name = config.get('process_name')
                if not process_name:
                    raise ActionError("Missing required field: process_name for work_unit_creation")
                
                if self.logger:
                    self.logger.info(f"Waiting for work unit creation: {process_name}")
                
                result = self.workunit_monitor.wait_for_creation(
                    process_name=process_name,
                    timeout_seconds=timeout_seconds,
                    poll_interval_override=poll_interval_override
                )
                
                return ActionResult(
                    success=True,
                    message=f"Work unit created: {result['work_unit_id']}",
                    data=result,
                    state_updates={
                        'work_unit_id': result['work_unit_id'],
                        'work_unit_status': result['status']
                    }
                )
                
            elif target == "work_unit_completion":
                # Wait for work unit completion
                work_unit_id = state.get('work_unit_id')
                if not work_unit_id:
                    raise ActionError("work_unit_id not found in state for work_unit_completion")
                
                if self.logger:
                    self.logger.info(f"Waiting for work unit completion: {work_unit_id}")
                
                result = self.workunit_monitor.wait_for_completion(
                    work_unit_id=work_unit_id,
                    timeout_seconds=timeout_seconds,
                    poll_interval_override=poll_interval_override
                )
                
                return ActionResult(
                    success=True,
                    message=f"Work unit completed: {work_unit_id}",
                    data=result,
                    state_updates={
                        'work_unit_status': result['status']
                    }
                )
                
            else:
                raise ActionError(f"Unknown wait target: {target}")
                
        except FrameworkTimeoutError:
            raise
        except ActionError:
            raise
        except Exception as e:
            if self.logger:
                self.logger.error(f"Wait action failed: {str(e)}")
            raise ActionError(f"Wait action failed: {str(e)}")
