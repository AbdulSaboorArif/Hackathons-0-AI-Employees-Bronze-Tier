#!/bin/bash
# Quick Start Script for AI Employee - Bronze Tier (Linux/Mac)
# This script starts the File System Watcher

echo "============================================================"
echo "AI Employee - Bronze Tier Quick Start"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.13+ and try again"
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

# Check if vault exists
if [ ! -d "AI_Employee_Vault" ]; then
    echo "ERROR: AI_Employee_Vault folder not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "Vault found: AI_Employee_Vault"
echo ""

# Check if watcher exists
if [ ! -f "watchers/filesystem_watcher.py" ]; then
    echo "ERROR: Watcher script not found"
    echo "Please ensure watchers/filesystem_watcher.py exists"
    exit 1
fi

echo "Watcher script found"
echo ""

echo "============================================================"
echo "Starting File System Watcher..."
echo "============================================================"
echo ""
echo "The watcher will monitor: AI_Employee_Vault/Inbox"
echo "Drop files there to create tasks"
echo ""
echo "Press Ctrl+C to stop the watcher"
echo "============================================================"
echo ""

cd watchers
python3 filesystem_watcher.py ../AI_Employee_Vault
