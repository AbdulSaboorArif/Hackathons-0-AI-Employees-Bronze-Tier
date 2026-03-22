"""
Test LinkedIn selectors to verify watcher can detect notifications
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

session_path = Path("watchers/linkedin/.browser-session")

print("Testing LinkedIn monitoring selectors...")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        headless=False,
        args=['--no-sandbox']
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    # Navigate to LinkedIn
    print("\n[1] Loading LinkedIn...")
    page.goto('https://www.linkedin.com', wait_until='domcontentloaded')
    page.wait_for_timeout(3000)

    # Test login detection
    print("\n[2] Testing login detection...")
    login_selectors = [
        'nav[aria-label="Primary Navigation"]',
        '.global-nav',
        '[data-test-id="nav-home"]',
        'button[aria-label*="Start a post"]',
        '[id="global-nav"]',
        '.feed-identity-module'
    ]

    for selector in login_selectors:
        try:
            element = page.query_selector(selector)
            if element:
                print(f"   [OK] Found: {selector}")
            else:
                print(f"   [NO] Not found: {selector}")
        except Exception as e:
            print(f"   [ERR] Error with {selector}: {e}")

    # Test notification bell
    print("\n[3] Testing notification bell...")
    notification_selectors = [
        '[id="global-nav-icon-notifications-badge"]',
        'button[aria-label*="Notifications"]',
        '.global-nav__primary-link--notifications',
        '[data-test-global-nav-notifications]',
        'a[href*="/notifications/"]'
    ]

    for selector in notification_selectors:
        try:
            element = page.query_selector(selector)
            if element:
                print(f"   [OK] Found: {selector}")
                print(f"      Visible: {element.is_visible()}")
            else:
                print(f"   [NO] Not found: {selector}")
        except Exception as e:
            print(f"   [ERR] Error with {selector}: {e}")

    # Test notification badge (unread count)
    print("\n[4] Testing notification badge...")
    badge_selectors = [
        '.notification-badge',
        '.notification-badge__count',
        '[data-test-notification-badge]',
        '.artdeco-notification-badge'
    ]

    for selector in badge_selectors:
        try:
            element = page.query_selector(selector)
            if element:
                print(f"   [OK] Found: {selector}")
                print(f"      Text: {element.inner_text()}")
            else:
                print(f"   [NO] Not found: {selector}")
        except Exception as e:
            print(f"   [ERR] Error with {selector}: {e}")

    # Test feed posts
    print("\n[5] Testing feed posts...")
    feed_selectors = [
        '[data-test-id="feed-post"]',
        '.feed-shared-update-v2',
        '[data-urn*="urn:li:activity"]',
        '.scaffold-finite-scroll__content > div'
    ]

    for selector in feed_selectors:
        try:
            elements = page.query_selector_all(selector)
            if elements:
                print(f"   [OK] Found {len(elements)} posts with: {selector}")
            else:
                print(f"   [NO] Not found: {selector}")
        except Exception as e:
            print(f"   [ERR] Error with {selector}: {e}")

    # Test messaging
    print("\n[6] Testing messaging...")
    message_selectors = [
        '[id="global-nav-icon-messaging-badge"]',
        'button[aria-label*="Messaging"]',
        '.global-nav__primary-link--messaging',
        'a[href*="/messaging/"]'
    ]

    for selector in message_selectors:
        try:
            element = page.query_selector(selector)
            if element:
                print(f"   [OK] Found: {selector}")
            else:
                print(f"   [NO] Not found: {selector}")
        except Exception as e:
            print(f"   [ERR] Error with {selector}: {e}")

    print("\n" + "=" * 60)
    print("Test complete. Press Enter to close browser...")
    input()

    browser.close()
