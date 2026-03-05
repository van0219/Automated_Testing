"""FSM Work Units automation actions"""

from typing import Dict, Any, Optional, List
from ..base import BaseAction
from ...engine.test_state import TestState
from ...engine.results import ActionResult
from ...integration.playwright_client import PlaywrightMCPClient
from ...integration.ui_map_loader import UIMapLoader
from ...evidence.screenshot_manager import ScreenshotManager
from ...utils.exceptions import ActionError
from ...utils.logger import Logger
from ...utils.snapshot_parser import find_element_ref
import time


class FSMWorkUnitsAction(BaseAction):
    """
    FSM Work Units automation via Playwright MCP.
    
    Provides functions for:
    - Navigating to Work Units page
    - Searching for work units
    - Verifying work unit status
    - Monitoring work unit completion
    """
    
    def __init__(
        self,
        playwright_client: PlaywrightMCPClient,
        ui_map_loader: UIMapLoader,
        screenshot_manager: ScreenshotManager,
        logger: Optional[Logger] = None
    ):
        """
        Initialize FSM Work Units action.
        
        Args:
            playwright_client: PlaywrightMCPClient instance
            ui_map_loader: UIMapLoader instance
            screenshot_manager: ScreenshotManager instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.playwright = playwright_client
        self.ui_map = ui_map_loader
        self.screenshot_manager = screenshot_manager
        self.map_name = 'fsm_workunits_ui_map'
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Execute Work Units action based on operation type.
        
        Args:
            config: Action configuration with:
                - operation: Operation to perform (navigate, search, verify_status, wait_for_completion)
                - process_name: Process name to search for (optional)
                - work_unit_id: Work unit ID (optional)
                - expected_status: Expected status (optional)
                - timeout: Timeout in seconds (optional)
            state: TestState instance
        
        Returns:
            ActionResult with operation status
        """
        operation = config.get('operation')
        
        if operation == 'navigate':
            return self.navigate_to_work_units(config, state)
        elif operation == 'search':
            return self.search_work_unit(config, state)
        elif operation == 'verify_status':
            return self.verify_work_unit_status(config, state)
        elif operation == 'wait_for_completion':
            return self.wait_for_work_unit_completion(config, state)
        else:
            return ActionResult(
                success=False,
                message=f"Unknown Work Units operation: {operation}"
            )
    
    def navigate_to_work_units(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Navigate to Work Units page.
        
        Args:
            config: Action configuration
            state: TestState instance
        
        Returns:
            ActionResult with navigation status
        """
        try:
            if self.logger:
                self.logger.info("Navigating to Work Units page")
            
            # Step 1: Take snapshot to find current state
            snapshot = self.playwright.snapshot()
            
            # Step 2: Switch to Process Server Administrator if needed
            # Look for application switcher
            psa_ref = find_element_ref(snapshot, "Process Server Administrator", role="combobox")
            if not psa_ref:
                psa_ref = find_element_ref(snapshot, "Process Server Administrator")
            
            if psa_ref:
                self.playwright.click(psa_ref, "Process Server Administrator")
                self.playwright.wait_for_load(2)
                snapshot = self.playwright.snapshot()
            
            # Step 3: Expand Administration menu
            admin_ref = find_element_ref(snapshot, "Administration")
            if admin_ref:
                self.playwright.click(admin_ref, "Administration")
                self.playwright.wait_for_load(1)
                snapshot = self.playwright.snapshot()
            
            # Step 4: Click Work Units link
            work_units_ref = find_element_ref(snapshot, "Work Units", role="link")
            if not work_units_ref:
                work_units_ref = find_element_ref(snapshot, "Work Units")
            
            if not work_units_ref:
                raise ActionError("Work Units link not found in navigation")
            
            self.playwright.click(work_units_ref, "Work Units")
            
            # Step 5: Wait for page to load
            self.playwright.wait_for_load(3)
            
            # Step 6: Capture screenshot
            screenshot_path = self.screenshot_manager.capture(
                step_number=3,
                description="work_units_page"
            )
            
            if self.logger:
                self.logger.info("Work Units page loaded")
            
            return ActionResult(
                success=True,
                message="Navigated to Work Units page"
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Work Units navigation failed: {str(e)}")
            
            return ActionResult(
                success=False,
                message=f"Work Units navigation failed: {str(e)}"
            )
    
    def search_work_unit(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Search for work unit by process name or work unit ID.
        
        Args:
            config: Action configuration with:
                - process_name: Process name to search for (optional)
                - work_unit_id: Work unit ID to search for (optional)
                - work_title: Work title to search for (optional)
            state: TestState instance
        
        Returns:
            ActionResult with search results
        """
        try:
            process_name = config.get('process_name')
            work_unit_id = config.get('work_unit_id')
            work_title = config.get('work_title')
            
            if not any([process_name, work_unit_id, work_title]):
                raise ActionError("Must provide process_name, work_unit_id, or work_title for search")
            
            if self.logger:
                self.logger.info(f"Searching for work unit: process={process_name}, id={work_unit_id}, title={work_title}")
            
            # Take snapshot to find search fields
            snapshot = self.playwright.snapshot()
            
            # Fill search filters
            if work_unit_id:
                work_unit_label = self.ui_map.get_label(
                    self.map_name,
                    'work_units_page',
                    'work_unit_field'
                )
                work_unit_ref = find_element_ref(snapshot, work_unit_label, role="textbox")
                if work_unit_ref:
                    self.playwright.type_text(work_unit_ref, work_unit_label, work_unit_id, submit=True)
            
            if process_name:
                process_label = self.ui_map.get_label(
                    self.map_name,
                    'work_units_page',
                    'process_field'
                )
                process_ref = find_element_ref(snapshot, process_label, role="textbox")
                if process_ref:
                    self.playwright.type_text(process_ref, process_label, process_name, submit=True)
            
            if work_title:
                work_title_label = self.ui_map.get_label(
                    self.map_name,
                    'work_units_page',
                    'work_title_field'
                )
                work_title_ref = find_element_ref(snapshot, work_title_label, role="textbox")
                if work_title_ref:
                    self.playwright.type_text(work_title_ref, work_title_label, work_title, submit=True)
            
            # Wait for results
            self.playwright.wait_for_load(2)
            
            # Take snapshot of results
            results_snapshot = self.playwright.snapshot()
            
            # Parse results to extract work unit information
            # Look for work unit in grid - this is a simplified approach
            # In a real implementation, we would parse the grid structure
            
            if self.logger:
                self.logger.info("Work unit search complete")
            
            return ActionResult(
                success=True,
                message="Work unit search complete",
                data={"search_criteria": {"process_name": process_name, "work_unit_id": work_unit_id}}
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Work unit search failed: {str(e)}")
            
            return ActionResult(
                success=False,
                message=f"Work unit search failed: {str(e)}"
            )
    
    def verify_work_unit_status(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Verify work unit status matches expected status.
        
        Args:
            config: Action configuration with:
                - work_unit_id: Work unit ID (optional, uses state if not provided)
                - expected_status: Expected status (e.g., 'Completed', 'Failed')
            state: TestState instance
        
        Returns:
            ActionResult with verification result
        """
        try:
            work_unit_id = config.get('work_unit_id') or state.get('work_unit_id')
            expected_status = config.get('expected_status', 'Completed')
            
            if not work_unit_id:
                raise ActionError("Work unit ID not provided and not found in state")
            
            if self.logger:
                self.logger.info(f"Verifying work unit {work_unit_id} status: expected={expected_status}")
            
            # Take snapshot to find work unit in grid
            snapshot = self.playwright.snapshot()
            
            # Parse snapshot to find work unit row and extract status
            # This is a simplified approach - in reality we would need to:
            # 1. Find the grid/table element
            # 2. Locate the row with matching work unit ID
            # 3. Extract the status column value
            
            # For now, we'll look for status text in the snapshot
            # A more robust implementation would parse the grid structure
            actual_status = self._extract_status_from_snapshot(snapshot, work_unit_id)
            
            if not actual_status:
                raise ActionError(f"Could not determine status for work unit {work_unit_id}")
            
            # Capture screenshot
            screenshot_path = self.screenshot_manager.capture(
                step_number=4,
                description="work_unit_status"
            )
            
            # Compare status
            status_match = actual_status == expected_status
            
            if status_match:
                if self.logger:
                    self.logger.info(f"Work unit status verified: {actual_status}")
                
                return ActionResult(
                    success=True,
                    message=f"Work unit status verified: {actual_status}",
                    data={"work_unit_id": work_unit_id, "status": actual_status}
                )
            else:
                if self.logger:
                    self.logger.warning(f"Work unit status mismatch: expected={expected_status}, actual={actual_status}")
                
                return ActionResult(
                    success=False,
                    message=f"Work unit status mismatch: expected={expected_status}, actual={actual_status}",
                    data={"work_unit_id": work_unit_id, "expected": expected_status, "actual": actual_status}
                )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Work unit status verification failed: {str(e)}")
            
            return ActionResult(
                success=False,
                message=f"Work unit status verification failed: {str(e)}"
            )
    
    def wait_for_work_unit_completion(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Wait for work unit to complete with adaptive polling.
        
        Args:
            config: Action configuration with:
                - work_unit_id: Work unit ID (optional, uses state if not provided)
                - timeout: Timeout in seconds (default: 60)
                - poll_interval: Initial poll interval in seconds (default: 10)
            state: TestState instance
        
        Returns:
            ActionResult with completion status
        """
        try:
            work_unit_id = config.get('work_unit_id') or state.get('work_unit_id')
            timeout = config.get('timeout', 60)
            poll_interval = config.get('poll_interval', 10)
            
            if not work_unit_id:
                raise ActionError("Work unit ID not provided and not found in state")
            
            if self.logger:
                self.logger.info(f"Waiting for work unit {work_unit_id} completion (timeout: {timeout}s)")
            
            start_time = time.time()
            elapsed = 0
            
            while elapsed < timeout:
                # Take snapshot to check status
                snapshot = self.playwright.snapshot()
                
                # Extract work unit status from snapshot
                current_status = self._extract_status_from_snapshot(snapshot, work_unit_id)
                
                if not current_status:
                    if self.logger:
                        self.logger.warning(f"Could not determine work unit status, continuing to wait...")
                else:
                    if current_status in ['Completed', 'Failed', 'Canceled']:
                        if self.logger:
                            self.logger.info(f"Work unit completed with status: {current_status}")
                        
                        return ActionResult(
                            success=True,
                            message=f"Work unit completed: {current_status}",
                            data={"work_unit_id": work_unit_id, "status": current_status},
                            state_updates={"work_unit_status": current_status}
                        )
                
                # Adaptive polling: increase interval as time passes
                if elapsed < 120:  # First 2 minutes
                    current_interval = 10
                elif elapsed < 300:  # 2-5 minutes
                    current_interval = 30
                else:  # After 5 minutes
                    current_interval = 60
                
                if self.logger:
                    self.logger.debug(f"Work unit still running, waiting {current_interval}s...")
                
                time.sleep(current_interval)
                elapsed = time.time() - start_time
                
                # Refresh page to get updated status
                refresh_ref = find_element_ref(snapshot, "Refresh", role="button")
                if refresh_ref:
                    self.playwright.click(refresh_ref, "Refresh")
                    self.playwright.wait_for_load(1)
            
            # Timeout reached
            if self.logger:
                self.logger.warning(f"Work unit completion timeout after {timeout}s")
            
            return ActionResult(
                success=False,
                message=f"Work unit did not complete within {timeout}s",
                data={"work_unit_id": work_unit_id, "timeout": timeout}
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Work unit wait failed: {str(e)}")
            
            return ActionResult(
                success=False,
                message=f"Work unit wait failed: {str(e)}"
            )
    
    def _extract_status_from_snapshot(self, snapshot: Dict[str, Any], work_unit_id: str) -> Optional[str]:
        """
        Extract work unit status from snapshot.
        
        This is a simplified implementation that looks for status keywords
        near the work unit ID in the snapshot text.
        
        Args:
            snapshot: Snapshot data
            work_unit_id: Work unit ID to find status for
        
        Returns:
            Status string or None if not found
        """
        # Convert snapshot to string if needed
        snapshot_text = snapshot
        if isinstance(snapshot, dict):
            snapshot_text = snapshot.get('content', str(snapshot))
        
        if not isinstance(snapshot_text, str):
            snapshot_text = str(snapshot_text)
        
        # Look for status keywords near the work unit ID
        status_keywords = ['Completed', 'Failed', 'Running', 'Waiting', 'Canceled']
        
        # Find lines containing the work unit ID
        lines = snapshot_text.split('\n')
        for i, line in enumerate(lines):
            if work_unit_id in line:
                # Check this line and nearby lines for status
                search_lines = lines[max(0, i-2):min(len(lines), i+3)]
                for search_line in search_lines:
                    for status in status_keywords:
                        if status in search_line:
                            return status
        
        return None
