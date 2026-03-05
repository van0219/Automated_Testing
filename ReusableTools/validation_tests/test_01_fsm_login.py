#!/usr/bin/env python3
"""
TEST 1: FSM Login Validation

Goal: Verify Playwright MCP functions and FSM login automation work

Steps:
1. Navigate to FSM login page
2. Authenticate using existing credentials
3. Wait for Financials & Supply Management portal to load
4. Capture a browser snapshot
5. Capture a screenshot
6. Close the browser

Output: Projects/SONH/Temp/evidence/login_test/
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ReusableTools.testing_framework.integration.credential_manager import CredentialManager
from ReusableTools.testing_framework.integration.playwright_client import PlaywrightMCPClient
from ReusableTools.testing_framework.utils.logger import Logger

# Test configuration
CLIENT = "SONH"
ENVIRONMENT = "ACUITY_TST"
OUTPUT_DIR = Path("Projects/SONH/Temp/evidence/login_test")

def main():
    """Execute FSM login validation test."""
    print("="*60)
    print("TEST 1: FSM Login Validation")
    print("="*60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize logger
    logger = Logger("TEST1", None, 20)  # INFO level
    
    # Initialize Playwright client
    playwright = None
    
    try:
        # Load credentials
        print("\n[1/6] Loading credentials...")
        creds_dir = Path("Projects") / CLIENT / "Credentials"
        cred_manager = CredentialManager(creds_dir)
        fsm_creds = cred_manager.get_fsm_credentials(ENVIRONMENT)
        
        url = fsm_creds['url']
        username = fsm_creds['username']
        password = fsm_creds['password']
        
        print(f"  URL: {url}")
        print(f"  Username: {username}")
        
        # Initialize Playwright MCP client
        print("\n[2/6] Initializing Playwright MCP client...")
        playwright = PlaywrightMCPClient(logger)
        playwright.connect()
        print("  ✓ Playwright MCP client connected")
        
        # Navigate to FSM
        print("\n[3/6] Navigating to FSM login page...")
        playwright.navigate(url)
        print(f"  ✓ Navigation complete")
        
        # Wait for page load
        print("\n[4/6] Waiting for page to load...")
        playwright.wait_for_load(3)
        print("  ✓ Page loaded")
        
        # Take snapshot to find auth method
        print("\n[5/6] Taking snapshot to find authentication method...")
        snapshot = playwright.snapshot()
        
        # Save snapshot for inspection
        snapshot_file = OUTPUT_DIR / f"01_login_page_snapshot_{timestamp}.txt"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            f.write(str(snapshot))
        print(f"  ✓ Snapshot saved: {snapshot_file}")
        
        # Look for Cloud Identities button
        print("\n[6/6] Looking for 'Cloud Identities' authentication method...")
        snapshot_text = str(snapshot)
        
        if "Cloud Identities" in snapshot_text:
            print("  ✓ Found 'Cloud Identities' in snapshot")
        else:
            print("  ✗ 'Cloud Identities' not found in snapshot")
            print("  Available authentication methods:")
            # Try to extract visible text
            lines = snapshot_text.split('\n')
            for line in lines[:50]:  # First 50 lines
                if 'button' in line.lower() or 'link' in line.lower():
                    print(f"    {line.strip()}")
        
        # Take screenshot
        print("\n[7/7] Capturing screenshot...")
        screenshot_file = OUTPUT_DIR / f"01_login_page_{timestamp}.png"
        playwright.screenshot(str(screenshot_file), fullPage=False)
        print(f"  ✓ Screenshot saved: {screenshot_file}")
        
        # Close browser
        print("\nClosing browser...")
        playwright.close()
        
        print("\n" + "="*60)
        print("TEST 1: COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"\nOutput directory: {OUTPUT_DIR}")
        print("\nNext steps:")
        print("1. Review the snapshot file to understand the format")
        print("2. Check if 'Cloud Identities' button was found")
        print("3. Verify screenshot shows the login page")
        print("\nIf successful, proceed to TEST 2")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        print(f"\nError type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # Try to close browser on error
        if playwright:
            try:
                playwright.close()
            except:
                pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
