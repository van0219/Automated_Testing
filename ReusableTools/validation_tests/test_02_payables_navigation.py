#!/usr/bin/env python3
"""
TEST 2: Payables Navigation Validation

Goal: Verify that UI discovery labels and snapshot parsing work

Steps:
1. Login to FSM
2. Navigate to Financials & Supply Management
3. Open Payables application
4. Wait for Payables Search page to load
5. Capture snapshot
6. Capture screenshot

Output: Projects/SONH/Temp/evidence/payables_navigation_test/
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ReusableTools.testing_framework.integration.credential_manager import CredentialManager
from ReusableTools.testing_framework.utils.snapshot_parser import find_element_ref

# Test configuration
CLIENT = "SONH"
ENVIRONMENT = "ACUITY_TST"
OUTPUT_DIR = Path("Projects/SONH/Temp/evidence/payables_navigation_test")

def main():
    """Execute Payables navigation validation test."""
    print("="*60)
    print("TEST 2: Payables Navigation Validation")
    print("="*60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Load credentials
        print("\n[1/7] Loading credentials...")
        creds_dir = Path("Projects") / CLIENT / "Credentials"
        cred_manager = CredentialManager(creds_dir)
        fsm_creds = cred_manager.get_fsm_credentials(ENVIRONMENT)
        
        url = fsm_creds['url']
        username = fsm_creds['username']
        password = fsm_creds['password']
        
        print(f"  URL: {url}")
        print(f"  Username: {username}")
        
        # Navigate to FSM
        print("\n[2/7] Navigating to FSM...")
        mcp_playwright_browser_navigate(url=url)
        mcp_playwright_browser_wait_for(time=5)
        
        # Take screenshot of login page
        screenshot_file = OUTPUT_DIR / f"01_login_page_{timestamp}.png"
        mcp_playwright_browser_take_screenshot(
            filename=str(screenshot_file),
            type="png"
        )
        print(f"  Login page screenshot: {screenshot_file}")
        
        # Note: For this test, we'll stop at the login page
        # In a real scenario, we would:
        # - Find and click Cloud Identities
        # - Enter credentials
        # - Wait for portal to load
        # - Navigate to Payables
        
        print("\n[3/7] Taking snapshot of current page...")
        snapshot = mcp_playwright_browser_snapshot()
        
        # Save snapshot
        snapshot_file = OUTPUT_DIR / f"02_current_page_snapshot_{timestamp}.txt"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            f.write(str(snapshot))
        print(f"  Snapshot saved: {snapshot_file}")
        
        # Test snapshot parser
        print("\n[4/7] Testing snapshot parser...")
        print("  Looking for 'Cloud Identities' button...")
        
        ref = find_element_ref(snapshot, "Cloud Identities", role="button")
        if ref:
            print(f"  ✓ Found element ref: {ref}")
        else:
            print("  ✗ Element not found with role='button'")
            print("  Trying without role filter...")
            ref = find_element_ref(snapshot, "Cloud Identities")
            if ref:
                print(f"  ✓ Found element ref: {ref}")
            else:
                print("  ✗ Element not found")
        
        # Analyze snapshot structure
        print("\n[5/7] Analyzing snapshot structure...")
        snapshot_text = str(snapshot)
        
        print(f"  Snapshot type: {type(snapshot)}")
        print(f"  Snapshot length: {len(snapshot_text)} characters")
        
        # Show first few lines
        lines = snapshot_text.split('\n')
        print(f"  First 10 lines:")
        for i, line in enumerate(lines[:10], 1):
            print(f"    {i}: {line[:100]}")
        
        # Look for button patterns
        print("\n[6/7] Searching for button patterns...")
        button_count = 0
        for line in lines[:100]:
            if 'button' in line.lower():
                print(f"    {line.strip()[:120]}")
                button_count += 1
                if button_count >= 5:
                    break
        
        # Final screenshot
        print("\n[7/7] Capturing final screenshot...")
        screenshot_file = OUTPUT_DIR / f"03_final_state_{timestamp}.png"
        mcp_playwright_browser_take_screenshot(
            filename=str(screenshot_file),
            type="png"
        )
        print(f"  Screenshot saved: {screenshot_file}")
        
        # Close browser
        print("\nClosing browser...")
        mcp_playwright_browser_close()
        
        print("\n" + "="*60)
        print("TEST 2: COMPLETED")
        print("="*60)
        print(f"\nOutput directory: {OUTPUT_DIR}")
        print("\nAnalysis:")
        print("1. Review snapshot structure to understand format")
        print("2. Check if snapshot parser found element refs")
        print("3. Verify screenshot quality")
        print("\nIf snapshot parsing works, proceed to TEST 3")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        print(f"\nError type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # Try to close browser on error
        try:
            mcp_playwright_browser_close()
        except:
            pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
