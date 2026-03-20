#!/bin/bash
# Setup script for Silver Tier Watchers (Linux/Mac)

echo "🚀 Setting up Silver Tier Watchers..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
python3 -m playwright install chromium

# Create vault directories
echo ""
echo "📁 Creating vault directories..."
mkdir -p ../Vault/{Needs_Action,Pending_Approval,Approved,Rejected,Done,Plans,Logs}

# Setup Gmail authentication
echo ""
echo "📧 Gmail Setup:"
echo "1. Make sure credential.json is in .claude/skills/ directory"
echo "2. First run will open browser for OAuth authentication"
echo "3. Token will be saved for future runs"

# Setup WhatsApp
echo ""
echo "💬 WhatsApp Setup:"
echo "1. First run will open WhatsApp Web"
echo "2. Scan QR code with your phone"
echo "3. Session will be saved for future runs"

# Setup LinkedIn
echo ""
echo "💼 LinkedIn Setup:"
echo "1. First run will open LinkedIn"
echo "2. Login with your credentials"
echo "3. Session will be saved for future runs"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start watchers:"
echo "  python3 orchestrator.py --config config.json"
echo ""
