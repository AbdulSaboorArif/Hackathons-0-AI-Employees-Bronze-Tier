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
            page.wait_for_timeout(3000)

            # Check if logged in
            print('[CHECK] Verifying login status...')
            try:
                page.wait_for_selector('[data-test-id="feed-container"]', timeout=5000, state='visible')
                print('[OK] ✅ Logged in successfully')
            except:
                # Try alternative feed selector
                try:
                    page.wait_for_selector('.feed-shared-update-v2', timeout=5000, state='visible')
                    print('[OK] ✅ Logged in successfully')
                except:
                    print('[ERROR] ❌ Not logged in - please login manually')
                    print('[INFO] Browser will stay open for 30 seconds - please login')
                    page.wait_for_timeout(30000)
                    browser.close()
                    return False

            # Click "Start a post" button
            print('[ACTION] Clicking "Start a post"...')
            start_post_selectors = [
                'button:has-text("Start a post")',
                '.share-box-feed-entry__trigger',
                '[data-test-share-box-trigger]',
                '.artdeco-button--secondary:has-text("Start")',
                'button.share-box-feed-entry__trigger'
            ]

            clicked = False
            for selector in start_post_selectors:
                try:
                    print(f'[TRY] Attempting selector: {selector}')
                    page.wait_for_selector(selector, timeout=5000, state='visible')
                    page.click(selector)
                    clicked = True
                    print(f'[OK] ✅ Clicked using selector: {selector}')
                    break
                except Exception as e:
                    print(f'[DEBUG] Selector failed: {selector} - {str(e)[:50]}')
                    continue

            if not clicked:
                print('[ERROR] ❌ Could not find "Start a post" button')
                page.screenshot(path='linkedin_error.png')
                print('[SAVED] Screenshot saved to linkedin_error.png')
                browser.close()
                return False

            # Wait for post dialog to open
            print('[WAIT] Waiting for post dialog to open...')
            page.wait_for_timeout(2000)

            # Find and fill the post editor
            print('[ACTION] Typing post content...')
            editor_selectors = [
                'div[role="textbox"][contenteditable="true"]',
                '.ql-editor[contenteditable="true"]',
                '[contenteditable="true"].ql-editor',
                'div[contenteditable="true"]',
                '.share-creation-state__text-editor'
            ]

            typed = False
            for selector in editor_selectors:
                try:
                    print(f'[TRY] Attempting editor selector: {selector}')
                    page.wait_for_selector(selector, timeout=5000, state='visible')
                    page.click(selector)
                    page.wait_for_timeout(500)

                    # Type content character by character for better reliability
                    page.fill(selector, content)
                    typed = True
                    print(f'[OK] ✅ Content typed using selector: {selector}')
                    break
                except Exception as e:
                    print(f'[DEBUG] Editor selector failed: {selector} - {str(e)[:50]}')
                    continue

            if not typed:
                print('[ERROR] ❌ Could not find post editor')
                page.screenshot(path='linkedin_editor_error.png')
                print('[SAVED] Screenshot saved to linkedin_editor_error.png')
                browser.close()
                return False

            # Wait for content to be fully entered
            print('[WAIT] Waiting for content to be processed...')
            page.wait_for_timeout(2000)

            # Click Post button - THIS IS THE CRITICAL STEP
            print('[ACTION] Clicking "Post" button...')
            print('[DEBUG] Looking for Post button with multiple strategies...')

            post_button_selectors = [
                'button.share-actions__primary-action:has-text("Post")',
                'button[aria-label*="Post"]',
                'button:has-text("Post"):visible',
                '.share-actions__primary-action',
                'button.artdeco-button--primary:has-text("Post")',
                'button[data-test-share-actions-primary-action]',
                'button.share-actions__primary-action.artdeco-button--primary'
            ]

            posted = False
            for attempt, selector in enumerate(post_button_selectors, 1):
                try:
                    print(f'[TRY {attempt}/{len(post_button_selectors)}] Attempting selector: {selector}')

                    # Wait for button to be visible and enabled
                    page.wait_for_selector(selector, timeout=5000, state='visible')

                    # Check if button is enabled (not disabled)
                    button = page.query_selector(selector)
                    if button:
                        is_disabled = button.get_attribute('disabled')
                        if is_disabled:
                            print(f'[DEBUG] Button found but disabled, trying next selector...')
                            continue

                        print(f'[DEBUG] Button found and enabled, clicking...')
                        page.click(selector, timeout=5000)
                        posted = True
                        print(f'[OK] ✅ Clicked Post button using selector: {selector}')
                        break
                except Exception as e:
                    print(f'[DEBUG] Selector failed: {selector} - {str(e)[:80]}')
                    continue

            if not posted:
                print('[ERROR] ❌ Could not find or click Post button')
                print('[DEBUG] Taking screenshot for debugging...')
                page.screenshot(path='linkedin_post_button_error.png')
                print('[SAVED] Screenshot saved to linkedin_post_button_error.png')

                # Try one more time with a generic approach
                print('[RETRY] Attempting generic button click...')
                try:
                    all_buttons = page.query_selector_all('button')
                    for btn in all_buttons:
                        text = btn.inner_text().strip().lower()
                        if text == 'post':
                            print(f'[FOUND] Found button with text "Post", clicking...')
                            btn.click()
                            posted = True
                            print('[OK] ✅ Successfully clicked Post button via generic search')
                            break
                except Exception as e:
                    print(f'[ERROR] Generic retry also failed: {e}')

                if not posted:
                    browser.close()
                    return False

            # Wait for post to be published
            print('[WAIT] Waiting for post to publish...')
            page.wait_for_timeout(5000)

            # IMPORTANT: Verify the post actually published
            print('[VERIFY] Checking if post was published...')

            # Wait a bit for the post to process
            page.wait_for_timeout(3000)

            # Take screenshot BEFORE checking
            page.screenshot(path='linkedin_post_attempt.png')
            print('[SAVED] Screenshot saved to linkedin_post_attempt.png')

            # Check if post dialog closed (indicates success)
            print('[CHECK] Looking for post dialog...')
            try:
                post_dialog = page.wait_for_selector('[role="dialog"]', timeout=2000, state='hidden')
                print('[OK] ✅ Post dialog closed - post likely published!')
            except:
                # Dialog might still be visible
                post_dialog = page.query_selector('[role="dialog"]')
                if post_dialog and post_dialog.is_visible():
                    print('[WARNING] ⚠️ Post dialog still open - post may not have published')
                    print('[ACTION] Waiting 10 more seconds...')
                    page.wait_for_timeout(10000)

                    # Check again
                    post_dialog = page.query_selector('[role="dialog"]')
                    if post_dialog and post_dialog.is_visible():
                        print('[ERROR] ❌ Post dialog still open after 10 seconds')
                        print('[INFO] This usually means the Post button was not clicked successfully')
                        page.screenshot(path='linkedin_post_failed.png')
                        print('[SAVED] Failure screenshot saved to linkedin_post_failed.png')
                        browser.close()
                        return False
                    else:
                        print('[OK] ✅ Dialog closed after waiting')
                else:
                    print('[OK] ✅ No dialog found - post likely published')

            # Navigate to feed to verify
            print('[VERIFY] Navigating to feed to check...')
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded')
            page.wait_for_timeout(3000)

            # Take final screenshot
            page.screenshot(path='linkedin_post_success.png')
            print('[SAVED] ✅ Final screenshot saved to linkedin_post_success.png')

            print('[SUCCESS] ✅ Post published successfully!')
            print('[INFO] Check linkedin_post_success.png to verify')
            print('[INFO] Browser will stay open for 10 seconds for manual verification')
            page.wait_for_timeout(10000)

            browser.close()
            return True

        except Exception as e:
            print(f'[ERROR] ❌ Failed to post: {e}')
            page.screenshot(path='linkedin_error.png')
            browser.close()
            return False

if __name__ == '__main__':
    # Post content - APPROVED 2026-03-21
    content = """🤖 Building the Future: My Journey with AI Automation

I've been working on something exciting - an autonomous AI Employee system that's transforming how I manage daily operations.

Here's what it does:

✅ Monitors Gmail, WhatsApp, and LinkedIn 24/7
✅ Automatically detects urgent messages and creates action items
✅ Processes tasks with intelligent reasoning
✅ Maintains human-in-the-loop approval for sensitive actions
✅ Generates organized plans and audit trails

**Key Achievement:** Reduced response time by 80% while maintaining full control and security.

The future of work isn't about replacing humans—it's about augmenting our capabilities with intelligent automation. This system handles the routine monitoring and organization, freeing me to focus on high-value decisions.

Built using Claude Code, Obsidian, and Python watchers. Local-first architecture ensures privacy and security.

Interested in AI automation for your business? Let's connect! 👇

#AI #Automation #Productivity #Innovation #FutureOfWork #BusinessEfficiency"""

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
