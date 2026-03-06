"""FSM login automation action using Python Playwright"""

from typing import Dict, Any, Optional
from ..base import BaseAction
from ...engine.test_state import TestState
from ...engine.results import ActionResult
from ...integration.playwright_client import PlaywrightClient
from ...utils.exceptions import ActionError
from ...utils.logger import Logger


class FSMLoginAction(BaseAction):
    """
    FSM login automation using Python Playwright.
    
    Handles:
    - Navigation to FSM portal
    - Authentication selection (Cloud Identities or Azure)
    - Credential entry
    - Login verification
    """
    
    def __init__(
        self,
        playwright_client: PlaywrightClient,
        logger: Optional[Logger] = None
    ):
        """
        Initialize FSM login action.
        
        Args:
            playwright_client: PlaywrightClient instance
            logger: Optional logger instance
        """
        super().__init__(logger)
        self.playwright = playwright_client
    
    def execute(self, config: Dict[str, Any], state: TestState) -> ActionResult:
        """
        Execute FSM login.
        
        Args:
            config: Action configuration with:
                - url: FSM portal URL
                - username: FSM username
                - password: FSM password
                - auth_method: Authentication method (default: 'Cloud Identities')
            state: TestState instance
        
        Returns:
            ActionResult with login status
        
        Raises:
            ActionError: If login fails
        """
        try:
            # Extract configuration
            url = config.get('url')
            username = config.get('username')
            password = config.get('password')
            auth_method = config.get('auth_method', 'Cloud Identities')
            
            if not url or not username or not password:
                raise ActionError("Missing required login credentials: url, username, password")
            
            if self.logger:
                self.logger.info(f"Logging into FSM: {url}")
            
            # Step 1: Navigate to FSM portal
            self.playwright.navigate(url)
            self.playwright.wait_for_timeout(3000)
            
            # Check if already logged in (look for FSM portal indicators)
            try:
                # Check for common FSM portal elements
                fsm_indicators = [
                    'text="Financials & Supply Management"',
                    'text="Applications"',
                    '[aria-label="Applications"]',
                    '.portal-header',
                    'text="Infor OS Portal"'
                ]
                
                for indicator in fsm_indicators:
                    try:
                        if self.playwright.is_visible(indicator, timeout=2000):
                            if self.logger:
                                self.logger.info("Already logged in - FSM portal detected")
                            return ActionResult(
                                success=True,
                                message="Already logged in - FSM portal detected",
                                data={"url": url, "username": username}
                            )
                    except:
                        continue
            except:
                pass
            
            # Step 2: Select authentication method
            if self.logger:
                self.logger.debug(f"Selecting authentication method: {auth_method}")
            
            # Check if authentication selection page is present
            try:
                # Try multiple selectors for authentication method
                auth_selectors = [
                    f'text="{auth_method}"',
                    f'a:has-text("{auth_method}")',
                    f'button:has-text("{auth_method}")',
                    f'[aria-label="{auth_method}"]'
                ]
                
                auth_clicked = False
                for selector in auth_selectors:
                    try:
                        self.playwright.wait_for_selector(selector, timeout=5000)
                        self.playwright.click(selector)
                        auth_clicked = True
                        if self.logger:
                            self.logger.debug(f"Authentication method clicked using: {selector}")
                        break
                    except:
                        continue
                
                if auth_clicked:
                    # Step 3: Wait for login page to load (may redirect)
                    self.playwright.wait_for_load_state('networkidle', timeout=30000)
                    self.playwright.wait_for_timeout(3000)
                else:
                    # Authentication selection not found, might already be on login page
                    if self.logger:
                        self.logger.debug("Authentication selection not found, assuming already on login page")
            except:
                # Authentication selection page not present, continue to login
                if self.logger:
                    self.logger.debug("No authentication selection page, continuing to login")
            
            # Step 4: Enter email/username
            if self.logger:
                self.logger.info("Entering credentials")
            
            # Wait for email input field (increased timeout for redirect)
            email_selector = 'input[type="email"], input[name="loginfmt"], input[name="username"], input[id="i0116"]'
            self.playwright.wait_for_selector(email_selector, timeout=30000)
            self.playwright.fill(email_selector, username)
            
            # Click Next button (try multiple selectors)
            next_selectors = [
                'input[type="submit"]',
                'button[type="submit"]',
                'input[value="Next"]',
                '#idSIButton9',  # Microsoft login Next button ID
                'button:has-text("Next")'
            ]
            
            next_clicked = False
            for selector in next_selectors:
                try:
                    if self.playwright.is_visible(selector):
                        self.playwright.click(selector, timeout=5000)
                        next_clicked = True
                        break
                except:
                    continue
            
            if not next_clicked:
                raise ActionError("Next button not found after entering email")
            
            # Step 5: Enter password
            self.playwright.wait_for_timeout(2000)
            
            # Wait for password input field
            password_selector = 'input[type="password"], input[name="passwd"]'
            self.playwright.wait_for_selector(password_selector, timeout=10000)
            self.playwright.fill(password_selector, password)
            
            # Click Sign In button
            signin_button = 'button:has-text("Sign in"), button:has-text("Sign In"), input[type="submit"][value="Sign in"]'
            self.playwright.click(signin_button)
            
            # Step 6: Handle "Stay signed in?" prompt if it appears
            self.playwright.wait_for_timeout(2000)
            
            try:
                # Check if "Stay signed in?" prompt appears
                stay_signed_in = 'button:has-text("Yes"), button:has-text("No")'
                if self.playwright.is_visible(stay_signed_in):
                    # Click "Yes" to stay signed in
                    self.playwright.click('button:has-text("Yes")')
                    if self.logger:
                        self.logger.debug("Clicked 'Yes' on 'Stay signed in?' prompt")
            except:
                # Prompt didn't appear, continue
                pass
            
            # Step 7: Wait for FSM portal to load
            if self.logger:
                self.logger.info("Waiting for FSM portal to load...")
            
            # Wait for portal - try multiple selectors
            portal_selectors = [
                'text="Applications"',
                '[aria-label="Applications"]',
                '.portal-header',
                '#homePage',
                '.home-page',
                'text="Infor OS Portal"'
            ]
            
            portal_loaded = False
            for selector in portal_selectors:
                try:
                    self.playwright.wait_for_selector(selector, timeout=10000)
                    portal_loaded = True
                    if self.logger:
                        self.logger.info(f"Portal loaded - found selector: {selector}")
                    break
                except:
                    continue
            
            if not portal_loaded:
                # Portal might have loaded but with different elements
                # Check if we're no longer on login page
                self.playwright.wait_for_timeout(5000)
                current_url = self.playwright.page.url
                if 'login' not in current_url.lower() and 'auth' not in current_url.lower():
                    portal_loaded = True
                    if self.logger:
                        self.logger.info(f"Portal loaded - URL changed to: {current_url}")
            
            if not portal_loaded:
                raise ActionError("FSM portal did not load after login")
            
            if self.logger:
                self.logger.info("Login successful - FSM portal loaded")
            
            return ActionResult(
                success=True,
                message="FSM login successful",
                data={"url": url, "username": username}
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"FSM login failed: {str(e)}")
            
            return ActionResult(
                success=False,
                message=f"FSM login failed: {str(e)}"
            )
