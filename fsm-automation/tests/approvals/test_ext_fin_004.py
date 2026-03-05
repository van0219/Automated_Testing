"""
EXT_FIN_004 Approval Workflow Tests

Test scenarios for expense invoice approval workflows.
"""

import pytest
import allure
from datetime import datetime, timedelta
from pages.login_page import LoginPage
from pages.payables_page import PayablesPage
from pages.work_units_page import WorkUnitsPage


@allure.feature("Approval Workflows")
@allure.story("EXT_FIN_004 - Expense Invoice Approval")
@pytest.mark.approval
class TestEXTFIN004:
    """Test class for EXT_FIN_004 approval scenarios"""
    
    @allure.title("Scenario 3.1: GHR vendor auto approval")
    @allure.description("""
    Requester submits garnishment expense invoice for approval – auto approved
    
    Test Steps:
    1. Login to FSM
    2. Navigate to Payables
    3. Create expense invoice
    4. Submit for approval
    5. Verify work unit completion
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ghr_auto_approval(self, page, credentials):
        """Test GHR vendor invoice auto-approval workflow"""
        
        # Initialize page objects
        login_page = LoginPage(page)
        payables_page = PayablesPage(page)
        work_units_page = WorkUnitsPage(page)
        
        # Test data
        today = datetime.now()
        due_date = today + timedelta(days=7)
        
        invoice_data = {
            "company": "100",
            "vendor": "GHR001",  # GHR vendor for auto-approval
            "invoice_number": f"AUTO_{today.strftime('%Y%m%d_%H%M%S')}",
            "invoice_date": today.strftime("%Y%m%d"),
            "due_date": due_date.strftime("%Y%m%d"),
            "amount": "1000.00",
            "description": "Test garnishment expense - auto approval"
        }
        
        # Step 1: Login
        with allure.step("Login to FSM"):
            login_page.login(
                url=credentials["url"],
                username=credentials["username"],
                password=credentials["password"]
            )
        
        # Step 2: Navigate to Payables
        with allure.step("Navigate to Payables"):
            payables_page.navigate_to_payables()
        
        # Step 3: Create invoice
        with allure.step("Create expense invoice"):
            payables_page.create_invoice(invoice_data)
            payables_page.save_invoice()
        
        # Step 4: Submit for approval
        with allure.step("Submit invoice for approval"):
            payables_page.submit_for_approval()
        
        # Step 5: Verify work unit completion
        with allure.step("Verify approval workflow completion"):
            work_units_page.navigate_to_work_units()
            work_units_page.search_by_process("InvoiceApproval")
            
            status_info = work_units_page.wait_for_completion(timeout_seconds=120)
            
            # Assertions
            assert status_info["status"].lower() == "completed", \
                f"Expected work unit status 'Completed', got '{status_info['status']}'"
            
            allure.attach(
                f"Work Unit ID: {status_info['work_unit_id']}\n"
                f"Status: {status_info['status']}\n"
                f"Invoice: {invoice_data['invoice_number']}",
                name="test_results",
                attachment_type=allure.attachment_type.TEXT
            )
