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
        
        Handles two scenarios:
        1. From "My Available Applications" page - click Payables tile directly
        2. From portal home - expand sidebar and navigate to FSM > Payables
        
        Args:
            config: Action configuration
            state: TestState instance
        
        Returns:
            ActionResult with navigation status
        """
        try:
            if self.logger:
                self.logger.info("Navigating to Payables application")
            
            # Check if we're on "My Available Applications" page
            current_url = self.playwright.page.url
            page_title = self.playwright.page.title()
            
            # Scenario 1: On "My Available Applications" page - click Payables tile directly
            if "My Available Applications" in page_title or "fsm" in current_url.lower():
                if self.logger:
                    self.logger.debug("On My Available Applications page, looking for Payables tile")
                
                # First, try to scroll down to see more tiles
                try:
                    self.playwright.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    self.playwright.wait_for_timeout(1000)
                except:
                    pass
                
                # Look for Payables-related application tiles with multiple variations
                payables_tile_selectors = [
                    # Direct text matches
                    'text="Payables"',
                    'text="Payables Manager"',
                    'text="Manage Payables"',
                    # Button/link variations
                    'button:has-text("Payables")',
                    'a:has-text("Payables")',
                    'button:has-text("Payables Manager")',
                    'a:has-text("Payables Manager")',
                    # Aria labels
                    '[aria-label="Payables"]',
                    '[aria-label="Payables Manager"]',
                    # Generic containers
                    'div:has-text("Payables")',
                    '.application-tile:has-text("Payables")',
                    # Case insensitive search using XPath
                    '//div[contains(translate(text(), "PAYABLES", "payables"), "payables")]',
                    '//button[contains(translate(text(), "PAYABLES", "payables"), "payables")]',
                    '//a[contains(translate(text(), "PAYABLES", "payables"), "payables")]'
                ]
                
                payables_clicked = False
                for selector in payables_tile_selectors:
                    try:
                        if selector.startswith('//'):
                            # XPath selector
                            element = self.playwright.page.locator(f'xpath={selector}').first
                            if element.is_visible(timeout=2000):
                                element.click()
                                payables_clicked = True
                                if self.logger:
                                    self.logger.debug(f"Payables tile clicked using XPath: {selector}")
                                break
                        else:
                            # CSS selector
                            self.playwright.wait_for_selector(selector, timeout=3000)
                            self.playwright.click(selector)
                            payables_clicked = True
                            if self.logger:
                                self.logger.debug(f"Payables tile clicked using: {selector}")
                            break
                    except:
                        continue
                
                if payables_clicked:
                    # Wait for Payables page to load
                    self.playwright.wait_for_timeout(5000)
                    
                    if self.logger:
                        self.logger.info("Payables navigation complete")
                    
                    return ActionResult(
                        success=True,
                        message="Navigated to Payables application"
                    )
                else:
                    # If still not found, log available tiles for debugging
                    if self.logger:
                        try:
                            tiles = self.playwright.page.locator('.application-tile, [class*="application"], [class*="tile"]').all_text_contents()
                            self.logger.error(f"Payables tile not found. Available tiles: {tiles}")
                        except:
                            self.logger.error("Payables tile not found and could not list available tiles")
                    
                    raise ActionError("Payables application tile not found on My Available Applications page")
            
            # Scenario 2: From portal home - full navigation path
            if self.logger:
                self.logger.debug("Attempting full navigation path from portal home")
            
            # Step 1: Expand sidebar menu (hamburger icon)
            sidebar_selectors = [
                'button[aria-label="Menu"]',
                'button[title="Menu"]',
                '.menu-button',
                'button:has-text("☰")',
                '[data-automation-id="menu-button"]'
            ]
            
            sidebar_clicked = False
            for selector in sidebar_selectors:
                try:
                    if self.playwright.is_visible(selector):
                        self.playwright.click(selector, timeout=5000)
                        sidebar_clicked = True
                        if self.logger:
                            self.logger.debug(f"Sidebar expanded using: {selector}")
                        break
                except:
                    continue
            
            if not sidebar_clicked:
                raise ActionError("Sidebar menu button not found")
            
            self.playwright.wait_for_timeout(2000)
            
            # Step 2: Click "Financials & Supply Management"
            fsm_selectors = [
                'text="Financials & Supply Management"',
                'a:has-text("Financials & Supply Management")',
                '[aria-label="Financials & Supply Management"]'
            ]
            
            fsm_clicked = False
            for selector in fsm_selectors:
                try:
                    self.playwright.wait_for_selector(selector, timeout=5000)
                    self.playwright.click(selector)
                    fsm_clicked = True
                    if self.logger:
                        self.logger.debug(f"FSM clicked using: {selector}")
                    break
                except:
                    continue
            
            if not fsm_clicked:
                raise ActionError("Financials & Supply Management link not found")
            
            self.playwright.wait_for_timeout(3000)
            
            # Step 3: Select Payables role
            payables_selectors = [
                'text="Payables"',
                'button:has-text("Payables")',
                'a:has-text("Payables")',
                '[aria-label="Payables"]'
            ]
            
            payables_clicked = False
            for selector in payables_selectors:
                try:
                    self.playwright.wait_for_selector(selector, timeout=5000)
                    self.playwright.click(selector)
                    payables_clicked = True
                    if self.logger:
                        self.logger.debug(f"Payables clicked using: {selector}")
                    break
                except:
                    continue
            
            if not payables_clicked:
                raise ActionError("Payables link not found")
            
            # Step 4: Wait for Payables page to load
            self.playwright.wait_for_timeout(5000)
            
            if self.logger:
                self.logger.info("Payables navigation complete")
            
            return ActionResult(
                success=True,
                message="Navigated to Payables application"
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
            
            # Step 1: Click Create Invoice button
            create_button_selectors = [
                'button:has-text("Create Invoice")',
                'a:has-text("Create Invoice")',
                '[aria-label="Create Invoice"]',
                '[data-automation-id="create-invoice"]'
            ]
            
            create_clicked = False
            for selector in create_button_selectors:
                try:
                    self.playwright.wait_for_selector(selector, timeout=5000)
                    self.playwright.click(selector)
                    create_clicked = True
                    if self.logger:
                        self.logger.debug(f"Create Invoice clicked using: {selector}")
                    break
                except:
                    continue
            
            if not create_clicked:
                raise ActionError("Create Invoice button not found")
            
            # Step 2: Wait for form to load
            self.playwright.wait_for_timeout(3000)
            
            # Step 3: Fill invoice header fields
            self._fill_invoice_header(invoice_data)
            
            # Step 4: Set approval routing if provided
            if invoice_data.get('routing_category'):
                self._set_approval_routing(invoice_data)
            
            # Step 5: Save invoice
            self._save_invoice()
            
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
    
    def _fill_invoice_header(self, invoice_data: Dict[str, Any]) -> None:
        """
        Fill invoice header fields using CSS selectors.
        
        Args:
            invoice_data: Invoice data dictionary
        """
        if self.logger:
            self.logger.debug("Filling invoice header fields")
        
        # Company field
        company_selectors = [
            'input[name="company"]',
            'input[aria-label="Company"]',
            'input[placeholder*="Company"]',
            '#company'
        ]
        self._fill_field(company_selectors, invoice_data['company'], "Company")
        
        # Vendor field
        vendor_selectors = [
            'input[name="vendor"]',
            'input[aria-label="Vendor"]',
            'input[placeholder*="Vendor"]',
            '#vendor'
        ]
        self._fill_field(vendor_selectors, invoice_data['vendor'], "Vendor")
        
        # Invoice Number field
        invoice_number_selectors = [
            'input[name="invoiceNumber"]',
            'input[name="invoice_number"]',
            'input[aria-label="Invoice Number"]',
            'input[placeholder*="Invoice Number"]',
            '#invoiceNumber'
        ]
        self._fill_field(invoice_number_selectors, invoice_data['invoice_number'], "Invoice Number")
        
        # Invoice Date field
        invoice_date_selectors = [
            'input[name="invoiceDate"]',
            'input[name="invoice_date"]',
            'input[aria-label="Invoice Date"]',
            'input[placeholder*="Invoice Date"]',
            '#invoiceDate'
        ]
        self._fill_field(invoice_date_selectors, invoice_data['invoice_date'], "Invoice Date")
        
        # Due Date field
        due_date_selectors = [
            'input[name="dueDate"]',
            'input[name="due_date"]',
            'input[aria-label="Due Date"]',
            'input[placeholder*="Due Date"]',
            '#dueDate'
        ]
        self._fill_field(due_date_selectors, invoice_data['due_date'], "Due Date")
        
        # Optional: Invoice Amount
        if invoice_data.get('invoice_amount'):
            amount_selectors = [
                'input[name="invoiceAmount"]',
                'input[name="invoice_amount"]',
                'input[aria-label="Invoice Amount"]',
                'input[placeholder*="Amount"]',
                '#invoiceAmount'
            ]
            self._fill_field(amount_selectors, str(invoice_data['invoice_amount']), "Invoice Amount")
        
        # Optional: Description
        if invoice_data.get('description'):
            desc_selectors = [
                'input[name="description"]',
                'textarea[name="description"]',
                'input[aria-label="Description"]',
                'textarea[aria-label="Description"]',
                '#description'
            ]
            self._fill_field(desc_selectors, invoice_data['description'], "Description")
    
    def _fill_field(self, selectors: list, value: str, field_name: str) -> None:
        """
        Fill field using multiple selector fallbacks.
        
        Args:
            selectors: List of CSS selectors to try
            value: Value to fill
            field_name: Field name for logging
        """
        for selector in selectors:
            try:
                self.playwright.wait_for_selector(selector, timeout=3000)
                self.playwright.fill(selector, value)
                if self.logger:
                    self.logger.debug(f"{field_name} filled using: {selector}")
                return
            except:
                continue
        
        # If no selector worked, log warning but don't fail
        if self.logger:
            self.logger.warning(f"{field_name} field not found, skipping")
    
    def _set_approval_routing(self, invoice_data: Dict[str, Any]) -> None:
        """
        Set approval routing parameters.
        
        Args:
            invoice_data: Invoice data dictionary
        """
        if self.logger:
            self.logger.debug("Setting approval routing")
        
        routing_selectors = [
            'input[name="routingCategory"]',
            'input[name="routing_category"]',
            'input[aria-label="Routing Category"]',
            'select[name="routingCategory"]',
            '#routingCategory'
        ]
        
        self._fill_field(routing_selectors, invoice_data['routing_category'], "Routing Category")
    
    def _save_invoice(self) -> None:
        """Save invoice using CSS selectors."""
        if self.logger:
            self.logger.debug("Saving invoice")
        
        save_button_selectors = [
            'button:has-text("Save")',
            'button[aria-label="Save"]',
            'input[type="submit"][value="Save"]',
            '[data-automation-id="save-button"]'
        ]
        
        save_clicked = False
        for selector in save_button_selectors:
            try:
                self.playwright.wait_for_selector(selector, timeout=5000)
                self.playwright.click(selector)
                save_clicked = True
                if self.logger:
                    self.logger.debug(f"Save clicked using: {selector}")
                break
            except:
                continue
        
        if not save_clicked:
            raise ActionError("Save button not found")
        
        # Wait for save to complete
        self.playwright.wait_for_timeout(3000)
    
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
            
            # Try to find Submit for Approval button directly
            submit_selectors = [
                'button:has-text("Submit for Approval")',
                'a:has-text("Submit for Approval")',
                '[aria-label="Submit for Approval"]',
                '[data-automation-id="submit-approval"]'
            ]
            
            submit_clicked = False
            for selector in submit_selectors:
                try:
                    self.playwright.wait_for_selector(selector, timeout=5000)
                    self.playwright.click(selector)
                    submit_clicked = True
                    if self.logger:
                        self.logger.debug(f"Submit clicked using: {selector}")
                    break
                except:
                    continue
            
            # If not found, try More Actions menu
            if not submit_clicked:
                more_actions_selectors = [
                    'button:has-text("More Actions")',
                    'button:has-text("Actions")',
                    '[aria-label="More Actions"]',
                    '[data-automation-id="more-actions"]'
                ]
                
                for selector in more_actions_selectors:
                    try:
                        self.playwright.wait_for_selector(selector, timeout=5000)
                        self.playwright.click(selector)
                        self.playwright.wait_for_timeout(1000)
                        
                        # Now try Submit for Approval again
                        for submit_selector in submit_selectors:
                            try:
                                self.playwright.wait_for_selector(submit_selector, timeout=3000)
                                self.playwright.click(submit_selector)
                                submit_clicked = True
                                if self.logger:
                                    self.logger.debug(f"Submit clicked from menu using: {submit_selector}")
                                break
                            except:
                                continue
                        
                        if submit_clicked:
                            break
                    except:
                        continue
            
            if not submit_clicked:
                raise ActionError("Submit for Approval button not found")
            
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
