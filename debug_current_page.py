"""Quick diagnostic to see what's on the current page"""

from playwright.sync_api import sync_playwright
import time

# Credentials
FSM_URL = "https://mingle-portal.inforcloudsuite.com/v2/NMR2N66J9P445R7P_AX4"
FSM_USERNAME = "Frederic.Sinconegue@infor.com"
FSM_PASSWORD = "L@ws0n678"

def debug_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("Navigating and logging in...")
        page.goto(FSM_URL)
        time.sleep(3)
        
        # Click Cloud Identities
        try:
            page.click('text="Cloud Identities"')
            time.sleep(5)
        except:
            print("Cloud Identities not found, might already be logged in")
        
        # Login
        try:
            page.fill('input[name="username"]', FSM_USERNAME)
            page.fill('input[type="password"]', FSM_PASSWORD)
            page.click('button[type="submit"]')
            time.sleep(10)
        except:
            print("Login fields not found, might already be logged in")
        
        print(f"\nCurrent URL: {page.url}")
        print(f"Page Title: {page.title()}")
        
        # Check if on FSM page
        if "Financials" in page.title():
            print("\n✓ On FSM page - trying to navigate to Payables")
            
            # Try to find menu button
            menu_selectors = [
                'button[aria-label="Menu"]',
                'button[title="Menu"]',
                'button.menu-button',
                '[data-automation-id="menu-button"]',
                'ids-menu-button',
                'button[class*="menu"]',
                'button[class*="hamburger"]'
            ]
            
            print("\nLooking for menu button...")
            for selector in menu_selectors:
                try:
                    if page.is_visible(selector, timeout=2000):
                        print(f"  Found menu button: {selector}")
                        page.click(selector)
                        time.sleep(2)
                        break
                except:
                    continue
            
            # Look for Payables link
            print("\nLooking for Payables link...")
            payables_selectors = [
                'text="Payables"',
                'a:has-text("Payables")',
                'button:has-text("Payables")',
                '[aria-label="Payables"]',
                '[title="Payables"]',
                'ids-menu-item:has-text("Payables")'
            ]
            
            for selector in payables_selectors:
                try:
                    if page.is_visible(selector, timeout=2000):
                        print(f"  Found Payables: {selector}")
                        page.click(selector)
                        time.sleep(5)
                        print(f"\n  After click - URL: {page.url}")
                        print(f"  After click - Title: {page.title()}")
                        break
                except Exception as e:
                    print(f"  {selector} - not found or error: {e}")
                    continue
        
        # List all visible text on page
        print("\n" + "="*80)
        print("ALL VISIBLE TEXT ON PAGE (first 50 items):")
        print("="*80)
        try:
            all_text = page.locator('body *').all_text_contents()
            visible_text = [t.strip() for t in all_text if t.strip()]
            for i, text in enumerate(visible_text[:50]):
                if len(text) < 100:  # Only show short text items
                    print(f"{i+1}. {text}")
        except:
            pass
        
        print("\n" + "="*80)
        print("Keeping browser open for 60 seconds...")
        print("="*80)
        time.sleep(60)
        
        browser.close()

if __name__ == "__main__":
    debug_page()
