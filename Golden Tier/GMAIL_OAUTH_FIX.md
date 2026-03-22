# Gmail OAuth Setup - Error 403: access_denied

## Problem
Your Google Cloud project "hackathon-0-490304" is in testing mode and the email you're trying to authorize (sabooarif12@gmail.com) is not added as a test user.

## Solution: Add Test User

### Step 1: Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### Step 2: Select Your Project
- Click on the project dropdown at the top
- Select "hackathon-0-490304"

### Step 3: Navigate to OAuth Consent Screen
- In the left menu, go to: **APIs & Services** > **OAuth consent screen**
- Or visit directly: https://console.cloud.google.com/apis/credentials/consent

### Step 4: Add Test Users
1. Scroll down to the "Test users" section
2. Click **"+ ADD USERS"**
3. Enter the email: **sabooarif12@gmail.com**
4. Click **"SAVE"**

### Step 5: Retry Authorization
After adding the test user, run the authorization again:
```bash
python3 authorize_gmail.py
```

## Alternative Solution: Use Developer Account

If you created the Google Cloud project with **saboorarif0329@gmail.com**, use that account instead:
1. The developer account automatically has access
2. No need to add it as a test user
3. Just authorize with that account

## Quick Fix Command

After adding the test user in Google Cloud Console, run:
```bash
python3 authorize_gmail.py
```

The browser will open automatically and you should be able to authorize successfully.

---

**Note**: The app is in "Testing" mode which limits access to 100 test users. This is normal for development. To make it public, you'd need to submit for Google verification (takes 1-2 weeks).
