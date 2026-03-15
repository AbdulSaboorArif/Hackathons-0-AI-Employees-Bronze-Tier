@echo off
REM Quick Start Script for AI Employee - Bronze Tier
REM This script starts the File System Watcher

echo ============================================================
echo AI Employee - Bronze Tier Quick Start
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.13+ and try again
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if vault exists
if not exist "AI_Employee_Vault" (
    echo ERROR: AI_Employee_Vault folder not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo Vault found: AI_Employee_Vault
echo.

REM Check if watcher exists
if not exist "watchers\filesystem_watcher.py" (
    echo ERROR: Watcher script not found
    echo Please ensure watchers\filesystem_watcher.py exists
    pause
    exit /b 1
)

echo Watcher script found
echo.

echo ============================================================
echo Starting File System Watcher...
echo ============================================================
echo.
echo The watcher will monitor: AI_Employee_Vault\Inbox
echo Drop files there to create tasks
echo.
echo Press Ctrl+C to stop the watcher
echo ============================================================
echo.

cd watchers
python filesystem_watcher.py ..\AI_Employee_Vault

pause
