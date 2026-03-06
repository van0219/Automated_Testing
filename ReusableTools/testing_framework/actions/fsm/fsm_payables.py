"""FSM Payables automation actions using Python Playwright"""

from typing import Dict, Any, Optional
from datetime import datetime
from ..base import BaseAction
from ...engine.test_state import TestState
from ...engine.results import ActionResult
from ...integration.playwright_client import PlaywrightClient
from ...utils.exceptions import ActionError
from ...utils.logger import Logger


class FSMPayablesAction(BaseAction):
    """
    FSM Payables automation using Python Playwright.
    
    Provides functions for:
    - Navigating to Payables application
    - Creating expense invoices
    - Entering invoice header data
    - Setting approval routing
    - Submitting for approval
    """
    
    def __init__(
        self,
        playwright_client: PlaywrightClient,
        logger: Optional[Logger] = None
    ):
        """
        Initialize FSM Payables action.
        
        Args:
            playwright_client: PlaywrightClient instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.playwright = playwright_client
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Execute Payables action based on operation type.
        
        Args:
            config: Action configuration with:
                - operation: Operation to perform (create_invoice, submit_for_approval, navigate_to_payables)
                - invoice_data: Invoice data dictionary (for create_invoice)
            state: TestState instance
        
        Returns:
            ActionResult with operation status
        """
        operation = config.get('operation')
        
        if operation == 'navigate_to_payables':
            return self.navigate_to_payables(config, state)
        elif operation == 'create_invoice':
            return self.create_expense_invoice(config, state)
        elif operation == 'submit_for_approval':
            return self.submit_for_approval(config, state)
        else:
            return ActionResult(
                success=False,
                message=f"Unknown Payables operation: {operation}"
            )
    
    def navigate_to_payables(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Navigate to Payables application from FSM portal.
        
        CRITICAL: FSM content is inside an iframe! Must use iframe.contentFrame() for all interactions.
        
        Handles two scenarios:
        - Scenario A: Payables NOT preferred - Navigate from "My Available Applications"
        - Scenario B: Payables IS preferred - Already on Payables page
        
        Args:
            config: Action configuration
            state: TestState instance
        
        Returns:
            ActionResult with navigation status
        """
        try:
            if self.logger:
                self.logger.info("Navigating to Payables application")
            
            # Check current page
            current_url = self.playwright.page.url
            page_title = self.playwright.page.title()
            
            if self.logger:
                self.logger.debug(f"Current URL: {current_url}")
                self.logger.debug(f"Page Title: {page_title}")
            
            # CRITICAL: Wait for FSM iframe to load
            if self.logger:
                self.logger.debug("Waiting for FSM iframe to load...")
            
            self.playwright.wait_for_timeout(8000)  # Wait for iframe to load after login
            
            # Get iframe using frame_locator
            try:
                iframe = self.playwright.page.frame_locator('iframe[name^="fsm_"]')
                if self.logger:
                    self.logger.debug("FSM iframe found")
            except Exception as e:
                raise ActionError(f"FSM iframe not found: {str(e)}")
            
            # Scenario B: Check if already on Payables (Payables is preferred)
            try:
                create_invoice_btn = iframe.get_by_role('button', name='Create Invoice')
                if create_invoice_btn.is_visible(timeout=3000):
                    if self.logger:
                        self.logger.info("Already on Payables page (Scenario B) - no navigation needed")
                    return ActionResult(
                        success=True,
                        message="Already on Payables application"
                    )
            except:
                if self.logger:
                    self.logger.debug("Not on Payables page, checking for My Available Applications")
            
            # Scenario A: Navigate from "My Available Applications"
            try:
                my_apps_heading = iframe.get_by_role('heading', name='My Available Applications')
                if my_apps_heading.is_visible(timeout=3000):
                    if self.logger:
                        self.logger.info("On My Available Applications page (Scenario A) - navigating to Payables")
                    
                    # Click "More - Payables" button
                    payables_btn = iframe.get_by_role('button', name='More - Payables')
                    payables_btn.click()
                    if self.logger:
                        self.logger.debug("Clicked 'More - Payables' button")
                    
                    # Handle optional confirmation dialog
                    self.playwright.wait_for_timeout(2000)
                    try:
                        ok_btn = iframe.get_by_role('button', name='Ok')
                        if ok_btn.is_visible(timeout=5000):
                            ok_btn.click()
                            if self.logger:
                                self.logger.debug("Clicked 'Ok' on confirmation dialog")
                    except:
                        if self.logger:
                            self.logger.debug("No confirmation dialog appeared")
                    
                    # Wait for Payables to load
                    self.playwright.wait_for_timeout(10000)
                    
                    # Verify Payables loaded
                    try:
                        create_invoice_btn = iframe.get_by_role('button', name='Create Invoice')
                        if create_invoice_btn.is_visible(timeout=5000):
                            if self.logger:
                                self.logger.info("Payables navigation complete - Create Invoice button found")
                            return ActionResult(
                                success=True,
                                message="Navigated to Payables application"
                            )
                    except:
                        raise ActionError("Payables page did not load - Create Invoice button not found")
            except:
                raise ActionError("Unknown FSM page state - not on Payables or My Available Applications")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Payables navigation failed: {str(e)}")
            
            return ActionResult(
                success=False,
                message=f"Payables navigation failed: {str(e)}"
            )
    
    def create_expense_invoice(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Create expense invoice in FSM.
        
        CRITICAL: FSM content is inside an iframe! Must use iframe.contentFrame() for all interactions.
        
        Args:
            config: Action configuration with invoice_data:
                - company: Company code (required)
                - vendor: Vendor number (required)
                - invoice_number: Invoice number (required)
                - invoice_date: Invoice date YYYYMMDD (required)
                - due_date: Due date YYYYMMDD (required)
                - invoice_amount: Invoice amount (optional)
                - description: Invoice description (optional)
                - routing_category: Approval routing category (optional)
            state: TestState instance
        
        Returns:
            ActionResult with invoice creation status and invoice_number
        """
        try:
            invoice_data = config.get('invoice_data', {})
            
            # Validate required fields
            required_fields = ['company', 'vendor', 'invoice_number', 'invoice_date', 'due_date']
            missing_fields = [f for f in required_fields if not invoice_data.get(f)]
            
            if missing_fields:
                raise ActionError(f"Missing required invoice fields: {', '.join(missing_fields)}")
            
            if self.logger:
                self.logger.info(f"Creating expense invoice: {invoice_data.get('invoice_number')}")
            
            # Get iframe
            try:
                iframe = self.playwright.page.frame_locator('iframe[name^="fsm_"]')
            except Exception as e:
                raise ActionError(f"FSM iframe not found: {str(e)}")
            
            # Step 1: Click Create Invoice button (inside iframe)
            try:
                create_btn = iframe.get_by_role('button', name='Create Invoice')
                create_btn.click()
                if self.logger:
                    self.logger.debug("Create Invoice button clicked")
            except Exception as e:
                raise ActionError(f"Create Invoice button not found: {str(e)}")
            
            # Step 2: Wait for form to load
            self.playwright.wait_for_timeout(3000)
            
            # Step 3: Fill invoice header fields (inside iframe)
            self._fill_invoice_header(invoice_data, iframe)
            
            # Step 4: Set approval routing if provided
            if invoice_data.get('routing_category'):
                self._set_approval_routing(invoice_data, iframe)
            
            # Step 5: Save invoice
            self._save_invoice(iframe)
            
            if self.logger:
                self.logger.info(f"Invoice created successfully: {invoice_data.get('invoice_number')}")
            
            return ActionResult(
                success=True,
                message=f"Invoice created: {invoice_data.get('invoice_number')}",
                data={"invoice_number": invoice_data.get('invoice_number')},
                state_updates={"invoice_number": invoice_data.get('invoice_number')}
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Invoice creation failed: {str(e)}")
            
            return ActionResult(
                success=False,
                message=f"Invoice creation failed: {str(e)}"
            )
    
    def _fill_invoice_header(self, invoice_data: Dict[str, Any], iframe) -> None:
        """
        Fill invoice header fields using role-based selectors inside iframe.
        
        Args:
            invoice_data: Invoice data dictionary
            iframe: Playwright FrameLocator for FSM iframe
        """
        if self.logger:
            self.logger.debug("Filling invoice header fields")
        
        # Use role-based selectors with iframe
        # Company field
        try:
            company_field = iframe.get_by_label('Company', exact=False)
            company_field.fill(invoice_data['company'])
            if self.logger:
                self.logger.debug(f"Company filled: {invoice_data['company']}")
        except:
            if self.logger:
                self.logger.warning("Company field not found, skipping")
        
        # Vendor field
        try:
            vendor_field = iframe.get_by_label('Vendor', exact=False)
            vendor_field.fill(invoice_data['vendor'])
            if self.logger:
                self.logger.debug(f"Vendor filled: {invoice_data['vendor']}")
        except:
            if self.logger:
                self.logger.warning("Vendor field not found, skipping")
        
        # Invoice Number field
        try:
            invoice_number_field = iframe.get_by_label('Invoice Number', exact=False)
            invoice_number_field.fill(invoice_data['invoice_number'])
            if self.logger:
                self.logger.debug(f"Invoice Number filled: {invoice_data['invoice_number']}")
        except:
            if self.logger:
                self.logger.warning("Invoice Number field not found, skipping")
        
        # Invoice Date field
        try:
            invoice_date_field = iframe.get_by_label('Invoice Date', exact=False)
            invoice_date_field.fill(invoice_data['invoice_date'])
            if self.logger:
                self.logger.debug(f"Invoice Date filled: {invoice_data['invoice_date']}")
        except:
            if self.logger:
                self.logger.warning("Invoice Date field not found, skipping")
        
        # Due Date field
        try:
            due_date_field = iframe.get_by_label('Due Date', exact=False)
            due_date_field.fill(invoice_data['due_date'])
            if self.logger:
                self.logger.debug(f"Due Date filled: {invoice_data['due_date']}")
        except:
            if self.logger:
                self.logger.warning("Due Date field not found, skipping")
        
        # Optional: Invoice Amount
        if invoice_data.get('invoice_amount'):
            try:
                amount_field = iframe.get_by_label('Invoice Amount', exact=False)
                amount_field.fill(str(invoice_data['invoice_amount']))
                if self.logger:
                    self.logger.debug(f"Invoice Amount filled: {invoice_data['invoice_amount']}")
            except:
                if self.logger:
                    self.logger.warning("Invoice Amount field not found, skipping")
        
        # Optional: Description
        if invoice_data.get('description'):
            try:
                desc_field = iframe.get_by_label('Description', exact=False)
                desc_field.fill(invoice_data['description'])
                if self.logger:
                    self.logger.debug(f"Description filled: {invoice_data['description']}")
            except:
                if self.logger:
                    self.logger.warning("Description field not found, skipping")
    
    def _set_approval_routing(self, invoice_data: Dict[str, Any], iframe) -> None:
        """
        Set approval routing parameters inside iframe.
        
        Args:
            invoice_data: Invoice data dictionary
            iframe: Playwright FrameLocator for FSM iframe
        """
        if self.logger:
            self.logger.debug("Setting approval routing")
        
        try:
            routing_field = iframe.get_by_label('Routing Category', exact=False)
            routing_field.fill(invoice_data['routing_category'])
            if self.logger:
                self.logger.debug(f"Routing Category filled: {invoice_data['routing_category']}")
        except:
            if self.logger:
                self.logger.warning("Routing Category field not found, skipping")
    
    def _save_invoice(self, iframe) -> None:
        """
        Save invoice using role-based selectors inside iframe.
        
        Args:
            iframe: Playwright FrameLocator for FSM iframe
        """
        if self.logger:
            self.logger.debug("Saving invoice")
        
        try:
            save_btn = iframe.get_by_role('button', name='Save')
            save_btn.click()
            if self.logger:
                self.logger.debug("Save button clicked")
        except Exception as e:
            raise ActionError(f"Save button not found: {str(e)}")
        
        # Wait for save to complete
        self.playwright.wait_for_timeout(3000)
    
    def submit_for_approval(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Submit invoice for approval.
        
        CRITICAL: FSM content is inside an iframe! Must use iframe.contentFrame() for all interactions.
        
        Args:
            config: Action configuration
            state: TestState instance
        
        Returns:
            ActionResult with submission status
        """
        try:
            if self.logger:
                self.logger.info("Submitting invoice for approval")
            
            # Get iframe
            try:
                iframe = self.playwright.page.frame_locator('iframe[name^="fsm_"]')
            except Exception as e:
                raise ActionError(f"FSM iframe not found: {str(e)}")
            
            # Try to find Submit for Approval button directly (inside iframe)
            try:
                submit_btn = iframe.get_by_role('button', name='Submit for Approval')
                submit_btn.click()
                if self.logger:
                    self.logger.debug("Submit for Approval button clicked")
            except:
                # If not found, try More Actions menu
                if self.logger:
                    self.logger.debug("Submit button not found directly, trying More Actions menu")
                
                try:
                    more_actions_btn = iframe.get_by_role('button', name='More Actions')
                    more_actions_btn.click()
                    self.playwright.wait_for_timeout(1000)
                    
                    # Now try Submit for Approval again
                    submit_btn = iframe.get_by_role('button', name='Submit for Approval')
                    submit_btn.click()
                    if self.logger:
                        self.logger.debug("Submit for Approval clicked from More Actions menu")
                except Exception as e:
                    raise ActionError(f"Submit for Approval button not found: {str(e)}")
            
            # Wait for submission to complete
            self.playwright.wait_for_timeout(3000)
            
            if self.logger:
                self.logger.info("Invoice submitted for approval")
            
            return ActionResult(
                success=True,
                message="Invoice submitted for approval"
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Approval submission failed: {str(e)}")
            
            return ActionResult(
                success=False,
                message=f"Approval submission failed: {str(e)}"
            )
