"""FSM Login Page Object"""

import allure
from playwright.sync_api import Page, expect


class LoginPage:
    """Page object for FSM login functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Selectors
        self.cloud_identities_button = page.get_by_text("Cloud Identities")
        self.email_input = page.locator('input[type="email"], input[name="loginfmt"], input[name="username"]')
        self.next_button = page.locator('button[type="submit"], input[type="submit"]').first
        self.password_input = page.locator('input[type="password"], input[name="passwd"]')
        self.signin_button = page.get_by_role("button", name="Sign in")
        self.stay_signed_in_yes = page.get_by_role("button", name="Yes")
    
    @allure.step("Navigate to FSM login page")
    def navigate(self, url: str):
        """Navigate to FSM portal"""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
    
    @allure.step("Select Cloud Identities authentication")
    def select_cloud_identities(self):
        """Click Cloud Identities button"""
        self.cloud_identities_button.wait_for(state="visible", timeout=10000)
        self.cloud_identities_button.click()
        self.page.wait_for_load_state("networkidle")
    
    @allure.step("Enter username: {username}")
    def enter_username(self, username: str):
        """Enter email/username"""
        self.email_input.wait_for(state="visible", timeout=30000)
        self.email_input.fill(username)
        self.next_button.click()
        self.page.wait_for_timeout(2000)
    
    @allure.step("Enter password")
    def enter_password(self, password: str):
        """Enter password"""
        self.password_input.wait_for(state="visible", timeout=10000)
        self.password_input.fill(password)
        self.signin_button.click()
        self.page.wait_for_timeout(2000)
    
    @allure.step("Handle 'Stay signed in?' prompt")
    def handle_stay_signed_in(self):
        """Click Yes on Stay signed in prompt if it appears"""
        try:
            if self.stay_signed_in_yes.is_visible(timeout=3000):
                self.stay_signed_in_yes.click()
                self.page.wait_for_timeout(2000)
        except:
            pass  # Prompt didn't appear
    
    @allure.step("Wait for FSM portal to load")
    def wait_for_portal(self):
        """Wait for FSM portal to load after login"""
        # Wait for My Available Applications page
        self.page.wait_for_timeout(5000)
        
        # Check if we're on the portal
        current_url = self.page.url
        if "login" not in current_url.lower() and "auth" not in current_url.lower():
            return True
        
        raise Exception("FSM portal did not load after login")
    
    @allure.step("Login to FSM with credentials")
    def login(self, url: str, username: str, password: str):
        """Complete login flow"""
        self.navigate(url)
        self.select_cloud_identities()
        self.enter_username(username)
        self.enter_password(password)
        self.handle_stay_signed_in()
        self.wait_for_portal()
        
        # Attach screenshot
        allure.attach(
            self.page.screenshot(),
            name="01_login_complete",
            attachment_type=allure.attachment_type.PNG
        )
