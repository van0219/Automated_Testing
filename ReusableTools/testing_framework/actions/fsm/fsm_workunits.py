"""FSM Work Units automation actions using Python Playwright"""

from typing import Dict, Any, Optional
from ..base import BaseAction
from ...engine.test_state import TestState
from ...engine.results import ActionResult
from ...integration.playwright_client import PlaywrightClient
from ...utils.exceptions import ActionError
from ...utils.logger import Logger
import time


class FSMWorkUnitsAction(BaseAction):
    """
    FSM Work Units automation using Python Playwright.
    
    Provides functions for:
    - Navigating to Work Units page
    - Searching for work units
    - Verifying work unit status
    - Monitoring work unit completion with adaptive polling
    """
    
    def __init__(
        self,
        playwright_client: PlaywrightClient,
        logger: Optional[Logger] = None
    ):
        """
        Initialize FSM Work Units action.
        
        Args:
            playwright_client: PlaywrightClient instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.playwright = playwright_client
    
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
        Navigate to Work Units page from FSM portal.
        
        Args:
            config: Action configuration
            state: TestState instance
        
        Returns:
            ActionResult with navigation status
        """
        try:
            if self.logger:
                self.logger.info("Navigating to Work Units page")
            
            # Step 1: Switch to Process Server Administrator role
            psa_selectors = [
                'text="Process Server Administrator"',
                'button:has-text("Process Server Administrator")',
                'a:has-text("Process Server Administrator")',
                '[aria-label="Process Server Administrator"]'
            ]
            
            psa_clicked = False
            for selector in psa_selectors:
                try:
                    self.playwright.wait_for_selector(selector, timeout=5000)
                    self.playwright.click(selector)
                    psa_clicked = True
                    if self.logger:
                        self.logger.debug(f"Process Server Admin clicked using: {selector}")
                    break
                except:
                    continue
            
            if not psa_clicked:
                raise ActionError("Process Server Administrator link not found")
            
            self.playwright.wait_for_timeout(3000)
            
            # Step 2: Expand Administration menu (if needed)
            admin_selectors = [
                'text="Administration"',
                'button:has-text("Administration")',
                '[aria-label="Administration"]'
            ]
            
            for selector in admin_selectors:
                try:
                    if self.playwright.is_visible(selector):
                        self.playwright.click(selector, timeout=3000)
                        self.playwright.wait_for_timeout(1000)
                        if self.logger:
                            self.logger.debug(f"Administration menu expanded using: {selector}")
                        break
                except:
                    continue
            
            # Step 3: Click Work Units link
            work_units_selectors = [
                'text="Work Units"',
                'a:has-text("Work Units")',
                '[aria-label="Work Units"]',
                'button:has-text("Work Units")'
            ]
            
            work_units_clicked = False
            for selector in work_units_selectors:
                try:
                    self.playwright.wait_for_selector(selector, timeout=5000)
                    self.playwright.click(selector)
                    work_units_clicked = True
                    if self.logger:
                        self.logger.debug(f"Work Units clicked using: {selector}")
                    break
                except:
                    continue
            
            if not work_units_clicked:
                raise ActionError("Work Units link not found")
            
            # Step 4: Wait for page to load
            self.playwright.wait_for_timeout(5000)
            
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
            
            # Fill search filters
            if work_unit_id:
                work_unit_selectors = [
                    'input[name="workUnit"]',
                    'input[name="work_unit"]',
                    'input[aria-label="Work Unit"]',
                    'input[placeholder*="Work Unit"]',
                    '#workUnit'
                ]
                self._fill_and_submit(work_unit_selectors, work_unit_id, "Work Unit")
            
            if process_name:
                process_selectors = [
                    'input[name="process"]',
                    'input[name="processName"]',
                    'input[aria-label="Process"]',
                    'input[placeholder*="Process"]',
                    '#process'
                ]
                self._fill_and_submit(process_selectors, process_name, "Process")
            
            if work_title:
                work_title_selectors = [
                    'input[name="workTitle"]',
                    'input[name="work_title"]',
                    'input[aria-label="Work Title"]',
                    'input[placeholder*="Work Title"]',
                    '#workTitle'
                ]
                self._fill_and_submit(work_title_selectors, work_title, "Work Title")
            
            # Wait for results
            self.playwright.wait_for_timeout(3000)
            
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
    
    def _fill_and_submit(self, selectors: list, value: str, field_name: str) -> None:
        """
        Fill field and submit (press Enter).
        
        Args:
            selectors: List of CSS selectors to try
            value: Value to fill
            field_name: Field name for logging
        """
        for selector in selectors:
            try:
                self.playwright.wait_for_selector(selector, timeout=3000)
                self.playwright.fill(selector, value)
                # Press Enter to submit
                self.playwright.page.keyboard.press('Enter')
                if self.logger:
                    self.logger.debug(f"{field_name} filled and submitted using: {selector}")
                return
            except:
                continue
        
        if self.logger:
            self.logger.warning(f"{field_name} field not found, skipping")
    
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
            
            # Extract status from page
            actual_status = self._extract_status_from_page()
            
            if not actual_status:
                raise ActionError(f"Could not determine status for work unit {work_unit_id}")
            
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
        
        Polling strategy:
        - 0-2 minutes: Poll every 10 seconds
        - 2-5 minutes: Poll every 30 seconds
        - 5+ minutes: Poll every 60 seconds
        
        Args:
            config: Action configuration with:
                - work_unit_id: Work unit ID (optional, uses state if not provided)
                - timeout: Timeout in seconds (default: 600 = 10 minutes)
            state: TestState instance
        
        Returns:
            ActionResult with completion status
        """
        try:
            work_unit_id = config.get('work_unit_id') or state.get('work_unit_id')
            timeout = config.get('timeout', 600)  # Default 10 minutes
            
            if not work_unit_id:
                raise ActionError("Work unit ID not provided and not found in state")
            
            if self.logger:
                self.logger.info(f"Waiting for work unit {work_unit_id} completion (timeout: {timeout}s)")
            
            start_time = time.time()
            elapsed = 0
            
            while elapsed < timeout:
                # Extract work unit status from page
                current_status = self._extract_status_from_page()
                
                if current_status:
                    if self.logger:
                        self.logger.debug(f"Current work unit status: {current_status}")
                    
                    # Check if work unit is in terminal state
                    if current_status in ['Completed', 'Failed', 'Canceled', 'Cancelled']:
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
                    self.logger.debug(f"Work unit still running, waiting {current_interval}s... (elapsed: {int(elapsed)}s)")
                
                time.sleep(current_interval)
                elapsed = time.time() - start_time
                
                # Refresh page to get updated status
                self._refresh_page()
            
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
    
    def _extract_status_from_page(self) -> Optional[str]:
        """
        Extract work unit status from current page.
        
        Looks for status text in common locations:
        - Status column in work units table
        - Status field in work unit details
        
        Returns:
            Status string or None if not found
        """
        status_selectors = [
            'td[data-column="status"]',
            'td[aria-label*="Status"]',
            '[data-automation-id="status"]',
            '.status-column',
            'span:has-text("Status")',
            'label:has-text("Status")'
        ]
        
        status_keywords = ['Completed', 'Failed', 'Running', 'Waiting', 'Canceled', 'Cancelled', 'Suspended']
        
        # Try to find status using selectors
        for selector in status_selectors:
            try:
                if self.playwright.is_visible(selector):
                    text = self.playwright.get_text(selector)
                    for keyword in status_keywords:
                        if keyword in text:
                            return keyword
            except:
                continue
        
        # Fallback: Search page text for status keywords
        try:
            page_text = self.playwright.page.content()
            for keyword in status_keywords:
                if keyword in page_text:
                    return keyword
        except:
            pass
        
        return None
    
    def _refresh_page(self) -> None:
        """Refresh the page to get updated work unit status."""
        try:
            # Try to find and click Refresh button
            refresh_selectors = [
                'button:has-text("Refresh")',
                'button[aria-label="Refresh"]',
                '[data-automation-id="refresh"]',
                'button:has-text("Reload")'
            ]
            
            for selector in refresh_selectors:
                try:
                    if self.playwright.is_visible(selector):
                        self.playwright.click(selector, timeout=3000)
                        self.playwright.wait_for_timeout(2000)
                        return
                except:
                    continue
            
            # If no refresh button found, reload page
            self.playwright.page.reload()
            self.playwright.wait_for_timeout(2000)
            
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Page refresh failed: {str(e)}")
