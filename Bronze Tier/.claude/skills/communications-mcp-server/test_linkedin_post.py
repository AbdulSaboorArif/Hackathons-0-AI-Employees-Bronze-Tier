"""
LinkedIn Post Script - Direct Posting
Uses existing browser session to post to LinkedIn
"""
import sys
import io
from pathlib import Path

# Fix Windows console encoding for emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.append(str(Path(__file__).parent.parent.parent / 'watchers'))

from playwright.sync_api import sync_playwright
import time

def post_to_linkedin(content, session_path):
    """Post content to LinkedIn using existing session"""

    print(f'[START] Posting to LinkedIn...')
    print(f'[SESSION] Using session: {session_path}')

    with sync_playwright() as p:
        # Use existing browser session (already logged in)
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,  # Visible so you can see it working
            args=['--no-sandbox']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Navigate to LinkedIn
            print('[NAVIGATE] Going to LinkedIn...')
            page.goto('https://www.linkedin.com', wait_until='domcontentloaded')
            time.sleep(3)

            # Check if logged in
            print('[CHECK] Verifying login status...')
            if page.query_selector('[data-test-id="feed-container"]') or page.query_selector('.feed-shared-update-v2'):
                print('[OK] ✅ Logged in successfully')
            else:
                print('[ERROR] ❌ Not logged in - please login manually')
                time.sleep(30)
                browser.close()
                return False

            # Click "Start a post" button
            print('[ACTION] Clicking "Start a post"...')
            start_post_selectors = [
                'button:has-text("Start a post")',
                '.share-box-feed-entry__trigger',
                '[data-test-share-box-trigger]',
                '.artdeco-button--secondary:has-text("Start")'
            ]

            clicked = False
            for selector in start_post_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        element.click()
                        clicked = True
                        print(f'[OK] Clicked using selector: {selector}')
                        break
                except Exception as e:
                    continue

            if not clicked:
                print('[ERROR] Could not find "Start a post" button')
                page.screenshot(path='linkedin_error.png')
                print('[SAVED] Screenshot saved to linkedin_error.png')
                browser.close()
                return False

            time.sleep(2)

            # Find and fill the post editor
            print('[ACTION] Typing post content...')
            editor_selectors = [
                '[role="textbox"]',
                '.ql-editor',
                '[contenteditable="true"]',
                '.share-creation-state__text-editor'
            ]

            typed = False
            for selector in editor_selectors:
                try:
                    editor = page.query_selector(selector)
                    if editor and editor.is_visible():
                        editor.click()
                        time.sleep(1)
                        editor.fill(content)
                        typed = True
                        print(f'[OK] Content typed using selector: {selector}')
                        break
                except Exception as e:
                    continue

            if not typed:
                print('[ERROR] Could not find post editor')
                page.screenshot(path='linkedin_editor_error.png')
                browser.close()
                return False

            time.sleep(2)

            # Click Post button
            print('[ACTION] Clicking "Post" button...')
            post_button_selectors = [
                'button:has-text("Post")',
                '.share-actions__primary-action',
                '[data-test-share-actions-primary-action]',
                '.artdeco-button--primary:has-text("Post")'
            ]

            posted = False
            for selector in post_button_selectors:
                try:
                    button = page.query_selector(selector)
                    if button and button.is_visible():
                        button.click()
                        posted = True
                        print(f'[OK] Clicked Post button using selector: {selector}')
                        break
                except Exception as e:
                    continue

            if not posted:
                print('[ERROR] Could not find Post button')
                page.screenshot(path='linkedin_post_button_error.png')
                browser.close()
                return False

            # Wait for post to be published
            print('[WAIT] Waiting for post to publish...')
            time.sleep(5)

            # Take screenshot of success
            page.screenshot(path='linkedin_post_success.png')
            print('[SUCCESS] ✅ Post published successfully!')
            print('[SAVED] Screenshot saved to linkedin_post_success.png')

            browser.close()
            return True

        except Exception as e:
            print(f'[ERROR] ❌ Failed to post: {e}')
            page.screenshot(path='linkedin_error.png')
            browser.close()
            return False

if __name__ == '__main__':
    # Post content
    content = """🤖 Exciting milestone in our AI automation journey!

We've successfully built an autonomous AI Employee system that:

✅ Monitors emails, WhatsApp, and LinkedIn 24/7
✅ Processes tasks with human-in-the-loop approval
✅ Automates routine communications
✅ Maintains organized knowledge base
✅ Generates daily business briefings

Key achievement: Reduced response time by 80% while maintaining full control and security.

The future of work isn't about replacing humans—it's about augmenting our capabilities with intelligent automation.

Interested in AI automation for your business? Let's connect! 👇

#AI #Automation #BusinessEfficiency #Innovation #FutureOfWork"""

    # Use existing LinkedIn session
    session_path = r'C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Bronze Tier\watchers\linkedin\.browser-session'

    print('=' * 60)
    print('LINKEDIN POSTING SCRIPT')
    print('=' * 60)
    print()

    success = post_to_linkedin(content, session_path)

    print()
    print('=' * 60)
    if success:
        print('✅ POSTING COMPLETE - Check your LinkedIn profile!')
    else:
        print('❌ POSTING FAILED - Check error screenshots')
    print('=' * 60)
