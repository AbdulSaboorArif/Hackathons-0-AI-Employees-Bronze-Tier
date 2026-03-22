"""
Test notification extraction to see what's in the notification panel
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

session_path = Path("watchers/linkedin/.browser-session")

print("Testing LinkedIn notification extraction...")
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

    print("\n[2] Finding notification bell...")
    notifications_button = page.query_selector('a[href*="/notifications/"]')
    if notifications_button:
        print("   [OK] Found notification bell")

        badge = page.query_selector('.notification-badge__count')
        if badge:
            badge_text = badge.inner_text().strip()
            print(f"   [OK] Badge shows: {badge_text} unread")

        print("\n[3] Clicking notification bell...")
        notifications_button.click()
        page.wait_for_timeout(3000)

        print("\n[4] Testing notification item selectors...")
        selectors = [
            '.notification-card',
            '[data-urn*="urn:li:notification"]',
            '.notifications-list li',
            '[role="listitem"]',
            '.artdeco-list__item',
            '.notification-item'
        ]

        for selector in selectors:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    print(f"   [OK] Found {len(elements)} items with: {selector}")

                    # Try to get text from first item
                    if len(elements) > 0:
                        try:
                            text = elements[0].inner_text()
                            print(f"      Sample text: {text[:100]}...")
                        except:
                            print(f"      (Could not extract text)")
                else:
                    print(f"   [NO] Not found: {selector}")
            except Exception as e:
                print(f"   [ERR] Error with {selector}: {e}")

        print("\n[5] Checking notification panel structure...")
        # Get the entire notification panel HTML structure
        panel_selectors = [
            '[role="dialog"]',
            '.notifications-container',
            '#notifications-dropdown',
            '.artdeco-dropdown__content'
        ]

        for selector in panel_selectors:
            element = page.query_selector(selector)
            if element:
                print(f"   [OK] Found panel: {selector}")

    else:
        print("   [ERR] Notification bell not found!")

    print("\n" + "=" * 60)
    print("Test complete. Press Enter to close browser...")
    input()

    browser.close()
