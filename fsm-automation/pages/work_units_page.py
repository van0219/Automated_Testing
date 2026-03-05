"""FSM Work Units Page Object"""

import allure
from playwright.sync_api import Page


class WorkUnitsPage:
    """Page object for FSM Work Units functionality"""
    
    def __init__(self, page: Page):
        self.page = page
    
    @allure.step("Navigate to Work Units")
    def navigate_to_work_units(self):
        """Navigate to Process Server Administrator > Work Units"""
        # Expand sidebar if collapsed
        try:
            menu_button = self.page.locator('button[aria-label="Menu"]').first
            if menu_button.is_visible(timeout=3000):
                menu_button.click()
                self.page.wait_for_timeout(1000)
        except:
            pass
        
        # Click Administration menu
        admin_menu = self.page.get_by_text("Administration")
        admin_menu.click()
        self.page.wait_for_timeout(1000)
        
        # Click Work Units
        work_units_link = self.page.get_by_text("Work Units")
        work_units_link.click()
        self.page.wait_for_timeout(3000)
        
        # Attach screenshot
        allure.attach(
            self.page.screenshot(),
            name="05_work_units_page",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure.step("Search for work unit by process name: {process_name}")
    def search_by_process(self, process_name: str):
        """Search for work units by process name"""
        # Find search/filter input
        search_input = self.page.locator('input[placeholder*="Search"], input[placeholder*="Filter"]').first
        search_input.fill(process_name)
        self.page.wait_for_timeout(2000)
    
    @allure.step("Get latest work unit status")
    def get_latest_work_unit_status(self) -> dict:
        """Get status of the most recent work unit"""
        # Get first row in the grid
        first_row = self.page.locator('tr[role="row"]').nth(1)
        
        # Extract work unit details
        work_unit_id = first_row.locator('td').nth(0).inner_text()
        status = first_row.locator('td').nth(3).inner_text()
        
        return {
            "work_unit_id": work_unit_id,
            "status": status
        }
    
    @allure.step("Wait for work unit completion")
    def wait_for_completion(self, timeout_seconds: int = 60):
        """Wait for work unit to complete"""
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            status_info = self.get_latest_work_unit_status()
            status = status_info["status"]
            
            if status.lower() in ["completed", "failed"]:
                allure.attach(
                    self.page.screenshot(),
                    name=f"06_work_unit_{status.lower()}",
                    attachment_type=allure.attachment_type.PNG
                )
                return status_info
            
            # Refresh page
            self.page.reload()
            self.page.wait_for_timeout(5000)
        
        raise TimeoutError(f"Work unit did not complete within {timeout_seconds} seconds")
