"""
Gmail Watcher - Monitors Gmail for important/unread emails
Uses Gmail API to check for new messages and creates action files
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from base_watcher import BaseWatcher
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailWatcher(BaseWatcher):
    """Watches Gmail for important/unread emails"""

    def __init__(self, vault_path: str, credentials_path: str, check_interval: int = 120):
        """
        Initialize Gmail watcher

        Args:
            vault_path: Path to Obsidian vault
            credentials_path: Path to Gmail credentials.json
            check_interval: Seconds between checks (default: 120)
        """
        super().__init__(vault_path, check_interval)
        self.credentials_path = credentials_path
        self.token_path = Path(credentials_path).parent / 'token.pickle'
        self.service = None
        self.processed_ids = set()

        # Initialize Gmail service
        self._initialize_gmail()

    def _initialize_gmail(self):
        """Initialize Gmail API service"""
        creds = None

        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info('Refreshing expired credentials')
                creds.refresh(Request())
            else:
                self.logger.info('Starting OAuth flow - browser will open')
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
            self.logger.info('Credentials saved')

        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info('Gmail API service initialized')

    def check_for_updates(self) -> list:
        """Check for new important/unread emails"""
        try:
            # Query for unread important emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed messages
            new_messages = [
                msg for msg in messages
                if msg['id'] not in self.processed_ids
            ]

            return new_messages

        except Exception as e:
            self.logger.error(f'Error checking Gmail: {e}')
            return []

    def create_action_file(self, message) -> Path:
        """Create action file for email"""
        try:
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = {
                h['name']: h['value']
                for h in msg['payload']['headers']
            }

            sender = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', 'Unknown')

            # Get email snippet
            snippet = msg.get('snippet', '')

            # Determine priority based on keywords
            urgent_keywords = ['urgent', 'asap', 'important', 'critical', 'invoice', 'payment']
            priority = 'high' if any(kw in subject.lower() or kw in snippet.lower() for kw in urgent_keywords) else 'normal'

            # Create markdown content
            content = f"""---
type: email
from: {sender}
subject: {subject}
date: {date}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
message_id: {message['id']}
---

## Email Content

{snippet}

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
- [ ] Mark as done

## Context
This email was flagged as important by Gmail and requires attention.
"""

            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_subject = ''.join(c for c in subject[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f'EMAIL_{timestamp}_{safe_subject}.md'

            filepath = self.needs_action / filename
            filepath.write_text(content, encoding='utf-8')

            # Mark as processed
            self.processed_ids.add(message['id'])

            return filepath

        except Exception as e:
            self.logger.error(f'Error creating action file: {e}')
            raise

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Gmail Watcher')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')
    parser.add_argument('--credentials', required=True, help='Path to credentials.json')
    parser.add_argument('--interval', type=int, default=120, help='Check interval in seconds')

    args = parser.parse_args()

    watcher = GmailWatcher(
        vault_path=args.vault,
        credentials_path=args.credentials,
        check_interval=args.interval
    )

    print(f'[START] Gmail Watcher started')
    print(f'[VAULT] Vault: {args.vault}')
    print(f'[INTERVAL] Checking every {args.interval} seconds')
    print(f'Press Ctrl+C to stop\n')

    watcher.run()
