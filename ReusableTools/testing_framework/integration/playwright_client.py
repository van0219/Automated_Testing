"""Playwright client for browser automation using Python Playwright"""

from typing import Dict, Any, Optional
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, Playwright
from ..utils.exceptions import ConnectionError as FrameworkConnectionError
from ..utils.logger import Logger


class PlaywrightClient:
    """
    Browser automation using Python Playwright.
    
    Provides browser automation capabilities using the standard Playwright library.
    """
    
    def __init__(self, logger: Optional[Logger] = None, headless: bool = False, screen: int = 2):
        """
        Initialize Playwright client.
        
        Args:
            logger: Optional logger instance
            headless: Run browser in headless mode (default: False for visibility)
            screen: Screen number to display browser on (default: 2 for second screen)
        """
        self.logger = logger
        self.headless = headless
        self.screen = screen
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self._connected = False
    
    def connect(self) -> None:
        """
        Start Playwright and launch browser.
        
        Launches browser in incognito mode, on specified screen, maximized.
        
        Raises:
            FrameworkConnectionError: If browser fails to start
        """
        try:
            if self.logger:
                self.logger.info(f"Starting Playwright browser (headless={self.headless}, screen={self.screen}, incognito=True, maximized=True)")
            
            self.playwright = sync_playwright().start()
            
            # Calculate position for second screen
            # Assuming primary screen is 1920x1080, second screen starts at x=1920
            screen_width = 1920
            screen_height = 1080
            x_position = (self.screen - 1) * screen_width
            
            # Launch browser with custom args
            launch_args = [
                f'--window-position={x_position},0',  # Position on specified screen
                '--window-size=1920,1080',  # Set window size
            ]
            
            # Launch browser normally
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=launch_args
            )
            
            # Create incognito context
            context = self.browser.new_context(
                viewport=None,  # Use window size
                no_viewport=True  # Disable fixed viewport
            )
            
            self.page = context.new_page()
            self.page.set_default_timeout(60000)  # 60 second default timeout
            
            # Maximize the window using JavaScript
            self.page.evaluate("""() => {
                window.moveTo(1920, 0);  // Move to second screen
                window.resizeTo(screen.availWidth, screen.availHeight);  // Maximize
            }""")
            
            self._connected = True
            
            if self.logger:
                self.logger.info(f"Playwright browser started successfully on screen {self.screen} in incognito maximized mode")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to start browser: {str(e)}")
            raise FrameworkConnectionError(f"Failed to start Playwright browser: {str(e)}")
    
    def _ensure_connected(self) -> None:
        """
        Ensure browser is connected.
        
        Raises:
            FrameworkConnectionError: If not connected
        """
        if not self._connected or not self.page:
            raise FrameworkConnectionError("Playwright client is not connected. Call connect() first.")
    
    def navigate(self, url: str) -> None:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If navigation fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.info(f"Navigating to: {url}")
            
            self.page.goto(url, wait_until='networkidle', timeout=60000)
            
            if self.logger:
                self.logger.info(f"Navigation complete: {url}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Navigation failed: {str(e)}")
            raise Exception(f"Failed to navigate to {url}: {str(e)}")
    
    def click(self, selector: str, timeout: int = 30000) -> None:
        """
        Click element by selector.
        
        Args:
            selector: CSS selector or text selector
            timeout: Timeout in milliseconds
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If click fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.info(f"Clicking element: {selector}")
            
            self.page.click(selector, timeout=timeout)
            
            if self.logger:
                self.logger.info(f"Click successful: {selector}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Click failed: {str(e)}")
            raise Exception(f"Failed to click element {selector}: {str(e)}")
    
    def fill(self, selector: str, text: str, timeout: int = 30000) -> None:
        """
        Fill text into element.
        
        Args:
            selector: CSS selector
            text: Text to fill
            timeout: Timeout in milliseconds
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If fill fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.info(f"Filling element: {selector}")
            
            self.page.fill(selector, text, timeout=timeout)
            
            if self.logger:
                self.logger.info(f"Fill successful: {selector}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Fill failed: {str(e)}")
            raise Exception(f"Failed to fill element {selector}: {str(e)}")
    
    def type_text(self, selector: str, text: str, delay: int = 50, timeout: int = 30000) -> None:
        """
        Type text into element (character by character).
        
        Args:
            selector: CSS selector
            text: Text to type
            delay: Delay between keystrokes in milliseconds
            timeout: Timeout in milliseconds
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If typing fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.info(f"Typing into element: {selector}")
            
            self.page.type(selector, text, delay=delay, timeout=timeout)
            
            if self.logger:
                self.logger.info(f"Type successful: {selector}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Type failed: {str(e)}")
            raise Exception(f"Failed to type into element {selector}: {str(e)}")
    
    def wait_for_selector(self, selector: str, timeout: int = 30000, state: str = 'visible') -> None:
        """
        Wait for element to appear.
        
        Args:
            selector: CSS selector or text selector
            timeout: Timeout in milliseconds
            state: Element state to wait for ('visible', 'attached', 'hidden')
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If wait fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.debug(f"Waiting for selector: {selector}")
            
            self.page.wait_for_selector(selector, timeout=timeout, state=state)
            
            if self.logger:
                self.logger.debug(f"Selector found: {selector}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Wait for selector failed: {str(e)}")
            raise Exception(f"Failed to wait for selector {selector}: {str(e)}")
    
    def wait_for_load_state(self, state: str = 'networkidle', timeout: int = 30000) -> None:
        """
        Wait for page load state.
        
        Args:
            state: Load state ('load', 'domcontentloaded', 'networkidle')
            timeout: Timeout in milliseconds
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If wait fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.debug(f"Waiting for load state: {state}")
            
            self.page.wait_for_load_state(state, timeout=timeout)
            
            if self.logger:
                self.logger.debug(f"Load state reached: {state}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Wait for load state failed: {str(e)}")
            raise Exception(f"Failed to wait for load state {state}: {str(e)}")
    
    def wait_for_timeout(self, timeout: int) -> None:
        """
        Wait for specified time.
        
        Args:
            timeout: Time to wait in milliseconds
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.debug(f"Waiting for {timeout}ms")
            
            self.page.wait_for_timeout(timeout)
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Wait for timeout failed: {str(e)}")
            raise Exception(f"Failed to wait for timeout: {str(e)}")
    
    def get_text(self, selector: str, timeout: int = 30000) -> str:
        """
        Get element text content.
        
        Args:
            selector: CSS selector
            timeout: Timeout in milliseconds
        
        Returns:
            Element text content
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If get text fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.debug(f"Getting text from: {selector}")
            
            text = self.page.text_content(selector, timeout=timeout)
            
            if self.logger:
                self.logger.debug(f"Text retrieved: {text[:50]}...")
            
            return text or ""
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Get text failed: {str(e)}")
            raise Exception(f"Failed to get text from {selector}: {str(e)}")
    
    def screenshot(self, path: str, full_page: bool = False) -> str:
        """
        Capture screenshot.
        
        Args:
            path: Path to save screenshot
            full_page: Whether to capture full scrollable page
        
        Returns:
            Path to screenshot file
        
        Raises:
            FrameworkConnectionError: If not connected
            Exception: If screenshot fails
        """
        self._ensure_connected()
        
        try:
            if self.logger:
                self.logger.debug(f"Capturing screenshot: {path}")
            
            # Ensure directory exists
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            self.page.screenshot(path=path, full_page=full_page)
            
            if self.logger:
                self.logger.debug(f"Screenshot captured: {path}")
            
            return path
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Screenshot failed: {str(e)}")
            raise Exception(f"Failed to capture screenshot {path}: {str(e)}")
    
    def is_visible(self, selector: str) -> bool:
        """
        Check if element is visible.
        
        Args:
            selector: CSS selector
        
        Returns:
            True if element is visible, False otherwise
        """
        self._ensure_connected()
        
        try:
            return self.page.is_visible(selector)
        except:
            return False
    
    def close(self) -> None:
        """Close browser and cleanup resources."""
        try:
            if self.logger:
                self.logger.info("Closing browser")
            
            if self.page:
                self.page.close()
                self.page = None
            
            if self.browser:
                self.browser.close()
                self.browser = None
            
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
            
            self._connected = False
            
            if self.logger:
                self.logger.info("Browser closed")
                
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Error closing browser: {str(e)}")
    
    def __enter__(self):
        """Context manager entry - connect browser."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close browser."""
        self.close()
        return False
