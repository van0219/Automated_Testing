"""Screenshot management for test evidence"""

from pathlib import Path
from datetime import datetime
from typing import Optional
from ..integration.playwright_client import PlaywrightClient
from ..utils.logger import Logger


class ScreenshotManager:
    """
    Capture and organize screenshots for test evidence.
    
    Manages screenshot naming, directory structure, and file organization
    for TES-070 document generation.
    """
    
    def __init__(self, playwright_client: PlaywrightClient, output_dir: str = "", logger: Optional[Logger] = None):
        """
        Initialize screenshot manager.
        
        Args:
            playwright_client: Playwright MCP client for screenshot capture
            output_dir: Base output directory (will be set per test)
            logger: Optional logger instance
        """
        self.playwright_client = playwright_client
        self.output_dir = Path(output_dir) if output_dir else Path("Temp")
        self.logger = logger
    
    def set_output_dir(self, interface_id: str) -> None:
        """
        Set output directory for current test.
        
        Args:
            interface_id: Interface ID for directory naming
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("Temp") / f"{interface_id}_{timestamp}"
        
        # Create directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.logger:
            self.logger.info(f"Screenshot output directory: {self.output_dir}")
    
    def capture(self, step_number: int, name: str) -> str:
        """
        Capture screenshot with naming convention.
        
        Args:
            step_number: Test step number
            name: Screenshot name (without extension)
        
        Returns:
            Full path to screenshot file
        """
        # Generate filename: {step_number:02d}_{name}.png
        filename = f"{step_number:02d}_{name}.png"
        filepath = self.output_dir / filename
        
        try:
            if self.logger:
                self.logger.debug(f"Capturing screenshot: {filename}")
            
            # Capture screenshot via Playwright
            self.playwright_client.screenshot(str(filepath), fullPage=False)
            
            if self.logger:
                self.logger.info(f"Screenshot captured: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            # Log warning but don't fail test execution
            if self.logger:
                self.logger.warning(f"Screenshot capture failed: {str(e)}")
            
            # Return empty string to indicate failure
            return ""
