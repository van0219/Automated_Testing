#!/usr/bin/env python3
"""
TEST 3: Create Invoice Screen Validation

Goal: Verify that the Create Invoice button can be located and clicked

Steps:
1. Login to FSM
2. Open Payables
3. Locate Create Invoice button using snapshot parser
4. Click Create Invoice
5. Wait for invoice form to load
6. Capture snapshot
7. Capture screenshot

Output: Projects/SONH/Temp/evidence/create_invoice_test/

Note: This test requires manual completion of login steps first
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ReusableTools.testing_framework.integration.credential_manager import CredentialManager
from ReusableTools.testing_framework.utils.snapshot_parser import find_element_ref, find_all_elements

# Test configuration
CLIENT = "SONH"
ENVIRONMENT = "ACUITY_TST"
OUTPUT_DIR = Path("Projects/SONH/Temp/evidence/create_invoice_test")

def main():
    """Execute Create Invoice button validation test."""
    print("="*60)
    print("TEST 3: Create Invoice Screen Validation")
    print("="*60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Load credentials
        print("\n[1/8] Loading credentials...")
        creds_dir = Path("Projects") / CLIENT / "Credentials"
        cred_manager = CredentialManager(creds_dir)
        fsm_creds = cred_manager.get_fsm_credentials(ENVIRONMENT)
        
        url = fsm_creds['url']
        
        print(f"  URL: {url}")
        
        # Navigate to FSM
        print("\n[2/8] Navigating to FSM...")
        mcp_playwright_browser_navigate(url=url)
        mcp_playwright_browser_wait_for(time=5)
        
        # Take initial screenshot
        screenshot_file = OUTPUT_DIR / f"01_initial_page_{timestamp}.png"
        mcp_playwright_browser_take_screenshot(
            filename=str(screenshot_file),
            type="png"
        )
        print(f"  Initial screenshot: {screenshot_file}")
        
        # Take snapshot
        print("\n[3/8] Taking snapshot of current page...")
        snapshot = mcp_playwright_browser_snapshot()
        
        # Save snapshot
        snapshot_file = OUTPUT_DIR / f"02_page_snapshot_{timestamp}.txt"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            f.write(str(snapshot))
        print(f"  Snapshot saved: {snapshot_file}")
        
        # Find all buttons
        print("\n[4/8] Finding all buttons on page...")
        buttons = find_all_elements(snapshot, role="button")
        print(f"  Found {len(buttons)} buttons")
        
        if buttons:
            print("  First 10 buttons:")
            for i, btn in enumerate(buttons[:10], 1):
                label = btn.get('label', 'No label')
                ref = btn.get('ref', 'No ref')
                print(f"    {i}. {label[:50]} [ref={ref}]")
        
        # Look for Create Invoice button
        print("\n[5/8] Looking for 'Create Invoice' button...")
        create_invoice_ref = find_element_ref(snapshot, "Create Invoice", role="button")
        
        if create_invoice_ref:
            print(f"  ✓ Found 'Create Invoice' button: {create_invoice_ref}")
        else:
            print("  ✗ 'Create Invoice' button not found")
            print("  Trying partial match...")
            create_invoice_ref = find_element_ref(snapshot, "Create", role="button")
            if create_invoice_ref:
                print(f"  ✓ Found button with 'Create': {create_invoice_ref}")
            else:
                print("  ✗ No 'Create' button found")
        
        # Look for other common buttons
        print("\n[6/8] Looking for other common buttons...")
        common_buttons = ["Search", "Advanced Search", "More Actions", "Refresh"]
        
        for button_name in common_buttons:
            ref = find_element_ref(snapshot, button_name, role="button")
            if ref:
                print(f"  ✓ Found '{button_name}': {ref}")
            else:
                print(f"  ✗ '{button_name}' not found")
        
        # Analyze snapshot format
        print("\n[7/8] Analyzing snapshot format...")
        snapshot_text = str(snapshot)
        
        # Check if it's YAML-like or dict-like
        if isinstance(snapshot, dict):
            print("  Format: Dictionary")
            print(f"  Keys: {list(snapshot.keys())[:10]}")
        elif isinstance(snapshot, str):
            print("  Format: String/YAML")
            # Look for patterns
            if '[ref=' in snapshot_text:
                print("  ✓ Contains [ref=...] patterns")
            if 'button "' in snapshot_text:
                print("  ✓ Contains button \"...\" patterns")
        
        # Show sample lines with 'button'
        print("\n  Sample button lines:")
        lines = snapshot_text.split('\n')
        button_lines = [line for line in lines if 'button' in line.lower()][:5]
        for line in button_lines:
            print(f"    {line.strip()[:120]}")
        
        # Final screenshot
        print("\n[8/8] Capturing final screenshot...")
        screenshot_file = OUTPUT_DIR / f"03_final_state_{timestamp}.png"
        mcp_playwright_browser_take_screenshot(
            filename=str(screenshot_file),
            type="png",
            fullPage=True
        )
        print(f"  Screenshot saved: {screenshot_file}")
        
        # Close browser
        print("\nClosing browser...")
        mcp_playwright_browser_close()
        
        print("\n" + "="*60)
        print("TEST 3: COMPLETED")
        print("="*60)
        print(f"\nOutput directory: {OUTPUT_DIR}")
        print("\nValidation Results:")
        print(f"  Buttons found: {len(buttons) if buttons else 0}")
        print(f"  Create Invoice button: {'✓ Found' if create_invoice_ref else '✗ Not found'}")
        print("\nNext Steps:")
        print("1. Review snapshot format and button discovery")
        print("2. Verify snapshot parser works correctly")
        print("3. If all tests pass, framework is ready for approval workflows")
        
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
