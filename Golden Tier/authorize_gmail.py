#!/usr/bin/env python3
"""
Gmail OAuth2 Authorization Script
Automatically handles OAuth flow and generates token.json
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authorize_gmail():
    """Authorize Gmail API and save token"""
    creds = None
    token_path = 'token.json'
    credentials_path = 'credential.json'

    print("\n" + "=" * 60)
    print("Gmail OAuth2 Authorization")
    print("=" * 60)

    # Check if credentials file exists
    if not os.path.exists(credentials_path):
        print(f"\n[ERROR] Credentials file not found: {credentials_path}")
        print("[INFO] Please ensure credential.json exists in the current directory")
        return False

    # Check if token already exists and is valid
    if os.path.exists(token_path):
        print("\n[*] Found existing token.json, checking validity...")
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            print(f"[WARNING] Could not load existing token: {e}")
            creds = None

    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[*] Refreshing expired token...")
            try:
                creds.refresh(Request())
                print("[OK] Token refreshed successfully")
            except Exception as e:
                print(f"[WARNING] Could not refresh token: {e}")
                creds = None

        if not creds:
            print("\n[*] Starting OAuth authorization flow...")
            print("[*] A browser window will open automatically")
            print("[*] Please sign in and grant permissions\n")

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path,
                    SCOPES,
                    redirect_uri='http://localhost:8080/'
                )

                # Run local server and open browser automatically
                creds = flow.run_local_server(
                    port=8080,
                    authorization_prompt_message='Please visit this URL to authorize: {url}',
                    success_message='Authorization successful! You can close this window.',
                    open_browser=True
                )

                print("\n[OK] Authorization successful!")

            except Exception as e:
                print(f"\n[ERROR] Authorization failed: {e}")
                return False

        # Save credentials
        try:
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
            print(f"[OK] Token saved to: {token_path}")
        except Exception as e:
            print(f"[ERROR] Could not save token: {e}")
            return False
    else:
        print("\n[OK] Valid token already exists")

    # Test the credentials by building Gmail service
    try:
        print("\n[*] Testing Gmail API connection...")
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        email = profile.get('emailAddress', 'Unknown')
        print(f"[OK] Successfully connected to Gmail API")
        print(f"[OK] Authorized email: {email}")
    except Exception as e:
        print(f"[ERROR] Could not connect to Gmail API: {e}")
        return False

    print("\n" + "=" * 60)
    print("Gmail API is ready to use!")
    print("=" * 60 + "\n")

    return True

if __name__ == '__main__':
    success = authorize_gmail()
    exit(0 if success else 1)
