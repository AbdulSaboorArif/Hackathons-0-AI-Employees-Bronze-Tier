@echo off
echo ========================================
echo 🚀 Starting Silver Tier Watchers
echo ========================================
echo.
echo Vault: AI_Employee_Vault
echo Watchers: Gmail + WhatsApp + LinkedIn
echo.
echo ⚠️  FIRST TIME SETUP:
echo    - Gmail: Browser will open for login
echo    - WhatsApp: Scan QR code with phone
echo    - LinkedIn: Login with credentials
echo.
echo Press Ctrl+C to stop all watchers
echo ========================================
echo.

cd watchers
python orchestrator.py --config config.json

pause
