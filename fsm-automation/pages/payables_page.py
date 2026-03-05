"""FSM Payables Page Object"""

import allure
from playwright.sync_api import Page
from datetime import datetime


class PayablesPage:
    """Page object for FSM Payables functionality"""
    
    def __init__(self, page: Page):
        self.page = page
    
    @allure.step("Navigate to Payables application")
    def navigate_to_payables(self):
        """Navigate from My Available Applications to Payables"""
        # Wait for iframe to load
        self.page.wait_for_timeout(3000)
        
        # Get the FSM iframe
        iframe = self.page.frame_locator('iframe[name^="fsm_"]')
        
        # Scroll down to see more tiles
        iframe.locator('body').evaluate("el => window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(1000)
        
        # Click on Payables tile - using the text we discovered
        # The tile contains "Payables" and "Setup, Process Invoices, Process Payments, Manage Vendors"
        payables_tile = iframe.get_by_text("Payables Setup, Process", exact=False)
        payables_tile.click()
        
        # Wait for Payables page to load
        self.page.wait_for_timeout(5000)
        
        # Wait for "Create Invoice" button to be visible (confirms page loaded)
        create_invoice_btn = iframe.get_by_role("button", name="Create Invoice")
        create_invoice_btn.wait_for(state="visible", timeout=10000)
        
        # Attach screenshot
        allure.attach(
            self.page.screenshot(),
            name="02_payables_loaded",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.step("Create expense invoice")
    def create_invoice(self, invoice_data: dict):
        """Create a new expense invoice"""
        # Get the FSM iframe
        iframe = self.page.frame_locator('iframe[name^="fsm_"]')
        
        # Click Create Invoice button
        create_button = iframe.get_by_role("button", name="Create Invoice")
        create_button.click()
        self.page.wait_for_timeout(3000)
        
        # Fill invoice fields
        self._fill_invoice_fields(invoice_data)
        
        # Attach screenshot
        allure.attach(
            self.page.screenshot(),
            name="03_invoice_created",
            attachment_type=allure.attachment_type.PNG
        )
    
    def _fill_invoice_fields(self, data: dict):
        """Fill invoice form fields"""
        # Company
        if "company" in data:
            self._fill_field("Company", data["company"])
        
        # Vendor
        if "vendor" in data:
            self._fill_field("Vendor", data["vendor"])
        
        # Invoice Number
        if "invoice_number" in data:
            self._fill_field("Invoice Number", data["invoice_number"])
        
        # Invoice Date
        if "invoice_date" in data:
            self._fill_field("Invoice Date", data["invoice_date"])
        
        # Due Date
        if "due_date" in data:
            self._fill_field("Due Date", data["due_date"])
        
        # Amount
        if "amount" in data:
            self._fill_field("Amount", str(data["amount"]))
        
        # Description
        if "description" in data:
            self._fill_field("Description", data["description"])
    
    def _fill_field(self, label: str, value: str):
        """Fill a form field by label"""
        try:
            # Try by label
            field = self.page.get_by_label(label)
            if field.is_visible(timeout=2000):
                field.fill(value)
                return
        except:
            pass
        
        try:
            # Try by placeholder
            field = self.page.locator(f'input[placeholder*="{label}"]')
            if field.is_visible(timeout=2000):
                field.fill(value)
                return
        except:
            pass
        
        # Log warning if field not found
        print(f"Warning: Could not find field '{label}'")
    
    @allure.step("Save invoice")
    def save_invoice(self):
        """Save the invoice"""
        save_button = self.page.get_by_role("button", name="Save")
        if not save_button.is_visible(timeout=5000):
            save_button = self.page.locator('button:has-text("Save")').first
        
        save_button.click()
        self.page.wait_for_timeout(3000)
    
    @allure.step("Submit invoice for approval")
    def submit_for_approval(self):
        """Submit invoice for approval"""
        # Try direct Submit for Approval button
        submit_selectors = [
            'button:has-text("Submit for Approval")',
            'a:has-text("Submit for Approval")',
        ]
        
        clicked = False
        for selector in submit_selectors:
            try:
                element = self.page.locator(selector).first
                if element.is_visible(timeout=5000):
                    element.click()
                    clicked = True
                    break
            except:
                continue
        
        # If not found, try More Actions menu
        if not clicked:
            try:
                more_actions = self.page.get_by_role("button", name="More Actions")
                more_actions.click()
                self.page.wait_for_timeout(1000)
                
                submit = self.page.locator('text="Submit for Approval"').first
                submit.click()
                clicked = True
            except:
                pass
        
        if not clicked:
            raise Exception("Submit for Approval button not found")
        
        self.page.wait_for_timeout(3000)
        
        # Attach screenshot
        allure.attach(
            self.page.screenshot(),
            name="04_invoice_submitted",
            attachment_type=allure.attachment_type.PNG
        )
