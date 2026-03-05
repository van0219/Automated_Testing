"""Work unit monitoring with adaptive polling"""

import time
from datetime import datetime
from typing import Dict, Any, Optional
from .playwright_client import PlaywrightClient
from ..utils.exceptions import TimeoutError as FrameworkTimeoutError, WorkUnitError
from ..utils.logger import Logger


class WorkUnitMonitor:
    """
    Monitor work unit status via UI automation with adaptive polling.
    
    Uses Playwright MCP client to navigate FSM UI and check work unit status.
    Implements adaptive polling: 0-2min=10s, 2-5min=30s, 5+min=60s
    """
    
    def __init__(self, playwright_client: PlaywrightClient, logger: Optional[Logger] = None):
        """
        Initialize work unit monitor.
        
        Args:
            playwright_client: Playwright MCP client for UI automation
            logger: Optional logger instance
        """
        self.playwright_client = playwright_client
        self.logger = logger
    
    def _get_poll_interval(self, elapsed_seconds: float, override: Optional[int] = None) -> int:
        """
        Calculate poll interval based on elapsed time.
        
        Args:
            elapsed_seconds: Time elapsed since monitoring started
            override: Optional override interval in seconds
        
        Returns:
            Poll interval in seconds
        """
        if override:
            return override
        
        # Adaptive polling
        if elapsed_seconds < 120:  # 0-2 minutes
            return 10
        elif elapsed_seconds < 300:  # 2-5 minutes
            return 30
        else:  # 5+ minutes
            return 60
    
    def wait_for_creation(
        self,
        process_name: str,
        timeout_seconds: int = 600,
        poll_interval_override: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Wait for work unit creation by process name.
        
        Args:
            process_name: Process name to monitor
            timeout_seconds: Maximum wait time in seconds (default: 600)
            poll_interval_override: Optional override for poll interval
        
        Returns:
            Dict with work_unit_id, status, and elapsed_time
        
        Raises:
            FrameworkTimeoutError: If timeout exceeded
            WorkUnitError: If work unit has Error status
        """
        start_time = datetime.now()
        start_timestamp = start_time.timestamp()
        
        if self.logger:
            self.logger.info(f"Waiting for work unit creation: {process_name} (timeout: {timeout_seconds}s)")
        
        while True:
            elapsed = (datetime.now() - start_time).total_seconds()
            
            # Check timeout
            if elapsed > timeout_seconds:
                if self.logger:
                    self.logger.error(f"Timeout waiting for work unit creation: {process_name}")
                raise FrameworkTimeoutError(
                    f"Timeout waiting for work unit creation: {process_name} "
                    f"(waited {elapsed:.0f}s)"
                )
            
            try:
                # Navigate to Work Units page
                if self.logger:
                    self.logger.debug(f"Checking for work unit (elapsed: {elapsed:.0f}s)")
                
                # Take snapshot to find work units
                snapshot = self.playwright_client.snapshot()
                
                # Parse snapshot to find work unit by process name
                # This is a simplified implementation - actual parsing would be more complex
                work_unit_id = self._find_work_unit_in_snapshot(
                    snapshot,
                    process_name,
                    start_timestamp
                )
                
                if work_unit_id:
                    # Get work unit status
                    status = self._get_work_unit_status(snapshot, work_unit_id)
                    
                    if self.logger:
                        self.logger.info(
                            f"Work unit created: {work_unit_id} "
                            f"(status: {status}, elapsed: {elapsed:.0f}s)"
                        )
                    
                    # Check for error status
                    if status == "Error":
                        raise WorkUnitError(f"Work unit {work_unit_id} has Error status")
                    
                    return {
                        'work_unit_id': work_unit_id,
                        'status': status,
                        'elapsed_time': elapsed
                    }
                
            except (FrameworkTimeoutError, WorkUnitError):
                raise
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Error checking work unit: {str(e)}")
            
            # Calculate poll interval and sleep
            poll_interval = self._get_poll_interval(elapsed, poll_interval_override)
            if self.logger:
                self.logger.debug(f"Sleeping {poll_interval}s before next poll")
            time.sleep(poll_interval)
    
    def wait_for_completion(
        self,
        work_unit_id: str,
        timeout_seconds: int = 600,
        poll_interval_override: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Wait for work unit completion by ID.
        
        Args:
            work_unit_id: Work unit ID to monitor
            timeout_seconds: Maximum wait time in seconds (default: 600)
            poll_interval_override: Optional override for poll interval
        
        Returns:
            Dict with work_unit_id, status, and elapsed_time
        
        Raises:
            FrameworkTimeoutError: If timeout exceeded
            WorkUnitError: If work unit has Error status
        """
        start_time = datetime.now()
        
        if self.logger:
            self.logger.info(
                f"Waiting for work unit completion: {work_unit_id} "
                f"(timeout: {timeout_seconds}s)"
            )
        
        while True:
            elapsed = (datetime.now() - start_time).total_seconds()
            
            # Check timeout
            if elapsed > timeout_seconds:
                if self.logger:
                    self.logger.error(f"Timeout waiting for work unit completion: {work_unit_id}")
                raise FrameworkTimeoutError(
                    f"Timeout waiting for work unit completion: {work_unit_id} "
                    f"(waited {elapsed:.0f}s)"
                )
            
            try:
                # Take snapshot to check status
                if self.logger:
                    self.logger.debug(
                        f"Checking work unit status (elapsed: {elapsed:.0f}s)"
                    )
                
                snapshot = self.playwright_client.snapshot()
                status = self._get_work_unit_status(snapshot, work_unit_id)
                
                if self.logger:
                    self.logger.debug(f"Work unit {work_unit_id} status: {status}")
                
                # Check for completion
                if status in ["Completed", "Cancelled"]:
                    if self.logger:
                        self.logger.info(
                            f"Work unit completed: {work_unit_id} "
                            f"(status: {status}, elapsed: {elapsed:.0f}s)"
                        )
                    
                    return {
                        'work_unit_id': work_unit_id,
                        'status': status,
                        'elapsed_time': elapsed
                    }
                
                # Check for error
                if status == "Error":
                    if self.logger:
                        self.logger.error(f"Work unit {work_unit_id} has Error status")
                    raise WorkUnitError(f"Work unit {work_unit_id} has Error status")
                
            except (FrameworkTimeoutError, WorkUnitError):
                raise
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Error checking work unit status: {str(e)}")
            
            # Calculate poll interval and sleep
            poll_interval = self._get_poll_interval(elapsed, poll_interval_override)
            if self.logger:
                self.logger.debug(f"Sleeping {poll_interval}s before next poll")
            time.sleep(poll_interval)
    
    def _find_work_unit_in_snapshot(
        self,
        snapshot: Dict[str, Any],
        process_name: str,
        start_timestamp: float
    ) -> Optional[str]:
        """
        Find work unit in snapshot by process name and timestamp.
        
        Args:
            snapshot: Page snapshot data
            process_name: Process name to search for
            start_timestamp: Start timestamp to filter by
        
        Returns:
            Work unit ID if found, None otherwise
        """
        # This is a placeholder implementation
        # Actual implementation would parse the snapshot structure
        # to find work units matching the process name and timestamp
        
        # For now, return None to indicate not found
        # Real implementation would search through snapshot elements
        return None
    
    def _get_work_unit_status(
        self,
        snapshot: Dict[str, Any],
        work_unit_id: str
    ) -> str:
        """
        Get work unit status from snapshot.
        
        Args:
            snapshot: Page snapshot data
            work_unit_id: Work unit ID
        
        Returns:
            Status string (Running, Completed, Error, Cancelled)
        """
        # This is a placeholder implementation
        # Actual implementation would parse the snapshot structure
        # to extract the status for the given work unit ID
        
        # For now, return "Running" as default
        # Real implementation would search through snapshot elements
        return "Running"
