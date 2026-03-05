"""FSM Payables automation actions"""

from typing import Dict, Any, Optional
from datetime import datetime
from ..base import BaseAction
from ...engine.test_state import TestState
from ...engine.results import ActionResult
from ...integration.playwright_client import PlaywrightMCPClient
from ...integration.ui_map_loader import UIMapLoader
from ...evidence.screenshot_manager import ScreenshotManager
from ...utils.exceptions import ActionError
from ...utils.logger import Logger
from ...utils.snapshot_parser import find_element_ref


class FSMPayablesAction(BaseAction):
    """
    FSM Payables automation via Playwright MCP.
    
    Provides functions for:
    - Creating expense invoices
    - Entering invoice header data
    - Setting approval routing
    - Submitting for approval
    """
    
    def __init__(
        self,
        playwright_client: PlaywrightMCPClient,
        ui_map_loader: UIMapLoader,
        screenshot_manager: ScreenshotManager,
        logger: Optional[Logger] = None
    ):
        """
        Initialize FSM Payables action.
        
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
        self.map_name = 'fsm_payables_ui_map'
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Execute Payables action based on operation type.
        
        Args:
            config: Action configuration with:
                - operation: Operation to perform (create_invoice, submit_for_approval, etc.)
                - invoice_data: Invoice data dictionary
            state: TestState instance
        
        Returns:
            ActionResult with operation status
        """
        operation = config.get('operation')
        
        if operation == 'create_invoice':
            return self.create_expense_invoice(config, state)
        elif operation == 'submit_for_approval':
            return self.submit_for_approval(config, state)
        elif operation == 'navigate_to_payables':
            return self.navigate_to_payables(config, state)
        else:
            return ActionResult(
                success=False,
                message=f"Unknown Payables operation: {operation}"
            )
    
    def navigate_to_payables(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Navigate to Payables application.
        
        Args:
            config: Action configuration
            state: TestState instance
        
        Returns:
            ActionResult with navigation status
        """
        try:
            if self.logger:
                self.logger.info("Navigating to Payables")
            
            # Take snapshot to find current state
            snapshot = self.playwright.snapshot()
            
            # Find and click Payables navigation element
            # This could be in the application switcher or sidebar
            payables_ref = find_element_ref(snapshot, "Payables", role="link")
            if not payables_ref:
                payables_ref = find_element_ref(snapshot, "Payables")
            
            if not payables_ref:
                raise ActionError("Payables navigation element not found")
            
            self.playwright.click(payables_ref, "Payables")
            self.playwright.wait_for_load(3)
            
            if self.logger:
                self.logger.info("Payables navigation complete")
            
            return ActionResult(
                success=True,
                message="Navigated to Payables"
            )
            
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
        
        Args:
            config: Action configuration with invoice_data:
                - company: Company code (required)
                - vendor: Vendor number (required)
                - invoice_number: Invoice number (required)
                - invoice_date: Invoice date (required)
                - due_date: Due date (required)
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
            
            # Step 1: Click Create Invoice button
            create_button_label = self.ui_map.get_label(
                self.map_name,
                'payables_search',
                'create_invoice_button'
            )
            
            if self.logger:
                self.logger.debug(f"Clicking: {create_button_label}")
            
            # Take snapshot to find button
            snapshot = self.playwright.snapshot()
            
            create_button_ref = find_element_ref(snapshot, create_button_label, role="button")
            if not create_button_ref:
                raise ActionError(f"Create Invoice button not found: {create_button_label}")
            
            self.playwright.click(create_button_ref, create_button_label)
            
            # Step 2: Wait for form to load
            self.playwright.wait_for_load(3)
            
            # Step 3: Take snapshot of form
            snapshot = self.playwright.snapshot()
            
            # Step 4: Fill invoice header fields
            self._fill_invoice_header(invoice_data, snapshot)
            
            # Step 5: Set approval routing if provided
            if invoice_data.get('routing_category'):
                self._set_approval_routing(invoice_data, snapshot)
            
            # Step 6: Capture screenshot
            screenshot_path = self.screenshot_manager.capture(
                step_number=1,
                description="invoice_created"
            )
            
            # Step 7: Save invoice
            self._save_invoice(snapshot)
            
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
    
    def _fill_invoice_header(self, invoice_data: Dict[str, Any], snapshot: Dict[str, Any]) -> None:
        """
        Fill invoice header fields.
        
        Args:
            invoice_data: Invoice data dictionary
            snapshot: Current page snapshot
        """
        # Get field labels from UI map
        company_label = self.ui_map.get_label(self.map_name, 'create_invoice_form', 'company_field')
        vendor_label = self.ui_map.get_label(self.map_name, 'create_invoice_form', 'vendor_field')
        invoice_number_label = self.ui_map.get_label(self.map_name, 'create_invoice_form', 'invoice_number_field')
        invoice_date_label = self.ui_map.get_label(self.map_name, 'create_invoice_form', 'invoice_date_field')
        due_date_label = self.ui_map.get_label(self.map_name, 'create_invoice_form', 'due_date_field')
        
        if self.logger:
            self.logger.debug("Filling invoice header fields")
        
        # Fill required fields
        company_ref = find_element_ref(snapshot, company_label, role="textbox")
        if company_ref:
            self.playwright.type_text(company_ref, company_label, invoice_data['company'])
        
        vendor_ref = find_element_ref(snapshot, vendor_label, role="textbox")
        if vendor_ref:
            self.playwright.type_text(vendor_ref, vendor_label, invoice_data['vendor'])
        
        invoice_number_ref = find_element_ref(snapshot, invoice_number_label, role="textbox")
        if invoice_number_ref:
            self.playwright.type_text(invoice_number_ref, invoice_number_label, invoice_data['invoice_number'])
        
        invoice_date_ref = find_element_ref(snapshot, invoice_date_label, role="combobox")
        if invoice_date_ref:
            self.playwright.type_text(invoice_date_ref, invoice_date_label, invoice_data['invoice_date'])
        
        due_date_ref = find_element_ref(snapshot, due_date_label, role="combobox")
        if due_date_ref:
            self.playwright.type_text(due_date_ref, due_date_label, invoice_data['due_date'])
        
        # Optional fields
        if invoice_data.get('invoice_amount'):
            amount_label = self.ui_map.get_label(self.map_name, 'create_invoice_form', 'invoice_amount_field')
            amount_ref = find_element_ref(snapshot, amount_label, role="textbox")
            if amount_ref:
                self.playwright.type_text(amount_ref, amount_label, str(invoice_data['invoice_amount']))
        
        if invoice_data.get('description'):
            desc_label = self.ui_map.get_label(self.map_name, 'create_invoice_form', 'description_field')
            desc_ref = find_element_ref(snapshot, desc_label, role="textbox")
            if desc_ref:
                self.playwright.type_text(desc_ref, desc_label, invoice_data['description'])
    
    def _set_approval_routing(self, invoice_data: Dict[str, Any], snapshot: Dict[str, Any]) -> None:
        """
        Set approval routing parameters.
        
        Args:
            invoice_data: Invoice data dictionary
            snapshot: Current page snapshot
        """
        if self.logger:
            self.logger.debug("Setting approval routing")
        
        routing_category_label = self.ui_map.get_label(
            self.map_name,
            'create_invoice_form',
            'invoice_routing_category'
        )
        
        routing_ref = find_element_ref(snapshot, routing_category_label, role="textbox")
        if routing_ref:
            self.playwright.type_text(routing_ref, routing_category_label, invoice_data['routing_category'])
    
    def _save_invoice(self, snapshot: Dict[str, Any]) -> None:
        """
        Save invoice.
        
        Args:
            snapshot: Current page snapshot
        """
        if self.logger:
            self.logger.debug("Saving invoice")
        
        save_button_label = self.ui_map.get_label(
            self.map_name,
            'create_invoice_form',
            'save_button'
        )
        
        save_ref = find_element_ref(snapshot, save_button_label, role="button")
        if not save_ref:
            raise ActionError(f"Save button not found: {save_button_label}")
        
        self.playwright.click(save_ref, save_button_label)
        
        # Wait for save to complete
        self.playwright.wait_for_load(2)
    
    def submit_for_approval(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Submit invoice for approval.
        
        Args:
            config: Action configuration
            state: TestState instance
        
        Returns:
            ActionResult with submission status
        """
        try:
            if self.logger:
                self.logger.info("Submitting invoice for approval")
            
            # Take snapshot to find submit button
            snapshot = self.playwright.snapshot()
            
            # Look for "Submit for Approval" button
            # This might be in More Actions menu or as a direct button
            submit_ref = find_element_ref(snapshot, "Submit for Approval", role="button")
            
            if not submit_ref:
                # Try to find More Actions button first
                more_actions_ref = find_element_ref(snapshot, "More Actions", role="button")
                if more_actions_ref:
                    self.playwright.click(more_actions_ref, "More Actions")
                    self.playwright.wait_for_load(1)
                    
                    # Take new snapshot after opening menu
                    snapshot = self.playwright.snapshot()
                    submit_ref = find_element_ref(snapshot, "Submit for Approval", role="button")
            
            if not submit_ref:
                raise ActionError("Submit for Approval button not found")
            
            self.playwright.click(submit_ref, "Submit for Approval")
            self.playwright.wait_for_load(2)
            
            # Capture screenshot
            screenshot_path = self.screenshot_manager.capture(
                step_number=2,
                description="approval_submitted"
            )
            
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
