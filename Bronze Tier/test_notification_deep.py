"""
Deep inspection of notification panel structure
"""
from playwright.sync_api import sync_playwright
from pathlib import Path

session_path = Path("watchers/linkedin/.browser-session")

print("Deep inspection of LinkedIn notification panel...")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        headless=False,
        args=['--no-sandbox']
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    print("\n[1] Loading LinkedIn...")
    page.goto('https://www.linkedin.com', wait_until='domcontentloaded')
    page.wait_for_timeout(3000)

    print("\n[2] Clicking notification bell...")
    notifications_button = page.query_selector('a[href*="/notifications/"]')
    if notifications_button:
        notifications_button.click()
        page.wait_for_timeout(3000)

        print("\n[3] Finding notification panel...")
        panel = page.query_selector('.artdeco-dropdown__content')
        if panel:
            print("   [OK] Panel found")

            # Get all direct children
            print("\n[4] Inspecting panel children...")
            children = panel.query_selector_all('> *')
            print(f"   Found {len(children)} direct children")

            # Try to find list container
            print("\n[5] Looking for list containers...")
            list_selectors = [
                'ul',
                'div[role="list"]',
                '.artdeco-list',
                'div > div',
                '[class*="list"]'
            ]

            for selector in list_selectors:
                elements = panel.query_selector_all(selector)
                if elements:
                    print(f"   [OK] Found {len(elements)} with: {selector}")

            # Get all links inside panel
            print("\n[6] Looking for links (notifications are usually links)...")
            links = panel.query_selector_all('a')
            print(f"   Found {len(links)} links in panel")

            if len(links) > 0:
                print("\n[7] Inspecting first 3 links...")
                for i, link in enumerate(links[:3]):
                    try:
                        href = link.get_attribute('href')
                        text = link.inner_text().strip()
                        print(f"\n   Link {i+1}:")
                        print(f"      href: {href}")
                        print(f"      text: {text[:100]}...")
                    except Exception as e:
                        print(f"   Link {i+1}: Error - {e}")

            # Try to get all divs with text
            print("\n[8] Looking for divs with text content...")
            divs = panel.query_selector_all('div')
            text_divs = []
            for div in divs[:20]:  # Check first 20 divs
                try:
                    text = div.inner_text().strip()
                    if len(text) > 20 and len(text) < 500:  # Reasonable notification length
                        text_divs.append(text)
                except:
                    pass

            print(f"   Found {len(text_divs)} divs with substantial text")
            if len(text_divs) > 0:
                print(f"\n   Sample text from first div:")
                print(f"   {text_divs[0][:150]}...")

        else:
            print("   [ERR] Panel not found!")

    print("\n" + "=" * 60)
    print("Inspection complete. Check output above.")
    print("Press Ctrl+C to close...")

    import time
    time.sleep(30)

    browser.close()
