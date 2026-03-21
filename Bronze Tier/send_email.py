#!/usr/bin/env python3
"""
Send Email via Gmail API
Uses token.json for authentication
"""

import os
import json
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

def send_email(to, subject, body):
    """Send email via Gmail API"""

    token_path = 'token.json'

    print("\n" + "=" * 60)
    print("Gmail Email Sender")
    print("=" * 60)

    # Load credentials
    if not os.path.exists(token_path):
        print(f"\n[ERROR] Token file not found: {token_path}")
        print("[INFO] Please run authorize_gmail.py first")
        return False

    try:
        creds = Credentials.from_authorized_user_file(token_path)
        print("\n[OK] Credentials loaded successfully")
    except Exception as e:
        print(f"\n[ERROR] Could not load credentials: {e}")
        return False

    # Build Gmail service
    try:
        service = build('gmail', 'v1', credentials=creds)
        print("[OK] Gmail service initialized")
    except Exception as e:
        print(f"\n[ERROR] Could not initialize Gmail service: {e}")
        return False

    # Create message
    try:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        print(f"\n[*] Sending email...")
        print(f"    To: {to}")
        print(f"    Subject: {subject}")
        print(f"    Body length: {len(body)} characters")

    except Exception as e:
        print(f"\n[ERROR] Could not create message: {e}")
        return False

    # Send message
    try:
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        print(f"\n[OK] Email sent successfully!")
        print(f"[OK] Message ID: {sent_message['id']}")
        print(f"[OK] Thread ID: {sent_message['threadId']}")

        # Log the result
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'to': to,
            'subject': subject,
            'message_id': sent_message['id'],
            'thread_id': sent_message['threadId'],
            'status': 'sent'
        }

        print("\n" + "=" * 60)
        print("Email Sent Successfully!")
        print("=" * 60 + "\n")

        return log_entry

    except Exception as e:
        print(f"\n[ERROR] Could not send email: {e}")
        print(f"[ERROR] Details: {str(e)}")
        return False

if __name__ == '__main__':
    # Email details
    recipient = "sabooarif12@gmail.com"
    subject = "Re: Your Inquiry - Confirmation"
    body = """Dear Team at ABX Company,

Thank you for taking the time to reach out to me. I appreciate your interest and am pleased to confirm my agreement to proceed.

I look forward to working with you and will be happy to discuss next steps at your convenience.

Best regards,
Abdul Saboor Arif"""

    result = send_email(recipient, subject, body)

    if result:
        # Save log
        log_file = 'AI_Employee_Vault/Logs/email_sent_log.json'
        os.makedirs('AI_Employee_Vault/Logs', exist_ok=True)

        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append(result)

        with open(log_file, 'w') as f:
            json.dump(logs, indent=2, fp=f)

        print(f"[OK] Log saved to: {log_file}")
        exit(0)
    else:
        exit(1)
