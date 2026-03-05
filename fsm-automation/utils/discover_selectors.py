"""
Selector Discovery Helper

Use this script to discover available elements on FSM pages.
"""

import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def discover_my_available_applications():
    """Discover available application tiles"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        # Login
        url = os.getenv("FSM_URL")
        username = os.getenv("FSM_USERNAME")
        password = os.getenv("FSM_PASSWORD")
        
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        
        # Click Cloud Identities
        page.get_by_text("Cloud Identities").click()
        page.wait_for_load_state("networkidle")
        
        # Enter credentials
        page.locator('input[type="email"]').first.fill(username)
        page.locator('button[type="submit"]').first.click()
        page.wait_for_timeout(2000)
        
        page.locator('input[type="password"]').first.fill(password)
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_timeout(2000)
        
        # Handle Stay signed in
        try:
            page.get_by_role("button", name="Yes").click(timeout=3000)
        except:
            pass
        
        page.wait_for_timeout(5000)
        
        # Scroll down
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        
        # Take screenshot
        page.screenshot(path="reports/screenshots/my_available_applications.png")
        
        # Get all visible text
        print("\n=== Available Application Tiles ===\n")
        
        # Try to find all application tiles
        tiles = page.locator('[class*="application"], [class*="tile"], [class*="card"]').all()
        
        for i, tile in enumerate(tiles):
            try:
                text = tile.inner_text(timeout=1000)
                if text.strip():
                    print(f"{i+1}. {text.strip()}")
            except:
                pass
        
        print("\n=== All Visible Text ===\n")
        body_text = page.locator('body').inner_text()
        lines = [line.strip() for line in body_text.split('\n') if line.strip()]
        for line in lines[:50]:  # First 50 lines
            print(line)
        
        print("\n\nScreenshot saved to: reports/screenshots/my_available_applications.png")
        print("Press Enter to close browser...")
        input()
        
        browser.close()

if __name__ == "__main__":
    discover_my_available_applications()
