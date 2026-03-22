@echo off
REM Setup script for Silver Tier Watchers (Windows)

echo ========================================
echo 🚀 Setting up Silver Tier Watchers...
echo ========================================
echo.

REM Check Python version
echo 📋 Checking Python version...
python --version
echo.

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
echo.

REM Install Playwright browsers
echo 🌐 Installing Playwright browsers...
python -m playwright install chromium
echo.

REM Create vault directories
echo 📁 Creating vault directories...
if not exist "..\Vault\Needs_Action" mkdir "..\Vault\Needs_Action"
if not exist "..\Vault\Pending_Approval" mkdir "..\Vault\Pending_Approval"
if not exist "..\Vault\Approved" mkdir "..\Vault\Approved"
if not exist "..\Vault\Rejected" mkdir "..\Vault\Rejected"
if not exist "..\Vault\Done" mkdir "..\Vault\Done"
if not exist "..\Vault\Plans" mkdir "..\Vault\Plans"
if not exist "..\Vault\Logs" mkdir "..\Vault\Logs"
echo.

echo ========================================
echo 📧 Gmail Setup:
echo ========================================
echo 1. Make sure credential.json is in .claude\skills\ directory
echo 2. First run will open browser for OAuth authentication
echo 3. Token will be saved for future runs
echo.

echo ========================================
echo 💬 WhatsApp Setup:
echo ========================================
echo 1. First run will open WhatsApp Web
echo 2. Scan QR code with your phone
echo 3. Session will be saved for future runs
echo.

echo ========================================
echo 💼 LinkedIn Setup:
echo ========================================
echo 1. First run will open LinkedIn
echo 2. Login with your credentials
echo 3. Session will be saved for future runs
echo.

echo ========================================
echo ✅ Setup complete!
echo ========================================
echo.
echo To start watchers:
echo   python orchestrator.py --config config.json
echo.
pause
