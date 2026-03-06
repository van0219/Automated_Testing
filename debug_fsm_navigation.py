"""Debug script to discover FSM navigation selectors"""

from playwright.sync_api import sync_playwright
import time

# Credentials
FSM_URL = "https://mingle-portal.inforcloudsuite.com/v2/NMR2N66J9P445R7P_AX4"
FSM_USERNAME = "Frederic.Sinconegue@infor.com"
FSM_PASSWORD = "L@ws0n678"

def debug_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("Step 1: Navigating to FSM portal...")
        page.goto(FSM_URL)
        time.sleep(3)
        
        print("Step 2: Selecting authentication method...")
        # Try to find and click Cloud Identities
        auth_selectors = [
            'text="Cloud Identities"',
            'a:has-text("Cloud Identities")',
            'button:has-text("Cloud Identities")',
            '[aria-label="Cloud Identities"]'
        ]
        
        auth_clicked = False
        for selector in auth_selectors:
            try:
                page.wait_for_selector(selector, timeout=3000)
                page.click(selector)
                print(f"✓ Cloud Identities clicked using: {selector}")
                auth_clicked = True
                break
            except:
                continue
        
        if not auth_clicked:
            print("✗ Cloud Identities link not found, might already be on login page")
        
        time.sleep(5)
        
        print("Step 3: Logging in...")
        # Try to find username field
        username_selectors = [
            'input[type="email"]',
            'input[name="username"]',
            'input[name="email"]',
            'input[id="username"]',
            'input[placeholder*="email"]',
            'input[placeholder*="username"]'
        ]
        
        for selector in username_selectors:
            try:
                page.wait_for_selector(selector, timeout=2000)
                page.fill(selector, FSM_USERNAME)
                print(f"✓ Username filled using: {selector}")
                break
            except:
                continue
        
        time.sleep(1)
        
        # Try to find password field
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            'input[id="password"]'
        ]
        
        for selector in password_selectors:
            try:
                page.wait_for_selector(selector, timeout=2000)
                page.fill(selector, FSM_PASSWORD)
                print(f"✓ Password filled using: {selector}")
                break
            except:
                continue
        
        time.sleep(1)
        
        # Try to find login button
        login_button_selectors = [
            'button[type="submit"]',
            'button:has-text("Sign in")',
            'button:has-text("Login")',
            'input[type="submit"]'
        ]
        
        for selector in login_button_selectors:
            try:
                page.wait_for_selector(selector, timeout=2000)
                page.click(selector)
                print(f"✓ Login button clicked using: {selector}")
                break
            except:
                continue
        
        print("Step 4: Waiting for page to load...")
        time.sleep(10)
        
        print(f"\nCurrent URL: {page.url}")
        print(f"Page Title: {page.title()}")
        
        print("\n" + "="*80)
        print("ANALYZING PAGE CONTENT")
        print("="*80)
        
        # Get all clickable elements with text
        print("\n1. All buttons:")
        buttons = page.locator('button').all()
        for i, btn in enumerate(buttons[:20]):  # Limit to first 20
            try:
                text = btn.inner_text()
                if text.strip():
                    print(f"   - {text.strip()}")
            except:
                pass
        
        print("\n2. All links:")
        links = page.locator('a').all()
        for i, link in enumerate(links[:20]):  # Limit to first 20
            try:
                text = link.inner_text()
                if text.strip():
                    print(f"   - {text.strip()}")
            except:
                pass
        
        print("\n3. All divs with text containing 'payable' (case insensitive):")
        try:
            payable_divs = page.locator('div, span, p').all()
            for div in payable_divs[:50]:  # Limit to first 50
                try:
                    text = div.inner_text()
                    if text and 'payable' in text.lower():
                        print(f"   - {text.strip()[:100]}")  # Limit text length
                except:
                    pass
        except:
            pass
        
        print("\n4. All application tiles/cards:")
        tile_selectors = [
            '.application-tile',
            '[class*="application"]',
            '[class*="tile"]',
            '[class*="card"]',
            '[role="button"]',
            '[role="link"]'
        ]
        
        for selector in tile_selectors:
            try:
                tiles = page.locator(selector).all()
                if tiles:
                    print(f"\n   Found {len(tiles)} elements with selector: {selector}")
                    for i, tile in enumerate(tiles[:10]):  # Limit to first 10
                        try:
                            text = tile.inner_text()
                            if text.strip():
                                print(f"      {i+1}. {text.strip()[:100]}")
                        except:
                            pass
            except:
                pass
        
        print("\n5. Page HTML structure (first 2000 chars):")
        try:
            html = page.content()
            print(html[:2000])
        except:
            pass
        
        print("\n" + "="*80)
        print("Keeping browser open for 60 seconds for manual inspection...")
        print("="*80)
        time.sleep(60)
        
        browser.close()

if __name__ == "__main__":
    debug_navigation()
