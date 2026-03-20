#!/bin/bash
# Quick Start Script for Silver Tier
# Sets up and verifies Silver Tier AI Employee

set -e  # Exit on error

echo "======================================================================"
echo "Silver Tier AI Employee - Quick Start"
echo "======================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo "ℹ️  $1"
}

# Check if we're in the vault directory
if [ ! -f "Dashboard.md" ] && [ ! -f "Company_Handbook.md" ]; then
    print_error "Not in AI Employee vault directory"
    echo "Please run this script from your AI_Employee_Vault directory"
    exit 1
fi

print_success "Found AI Employee vault"
echo ""

# Step 1: Check folder structure
echo "Step 1: Checking folder structure..."
echo "----------------------------------------------------------------------"

folders=(
    "Needs_Action"
    "Plans"
    "Pending_Approval"
    "Approved"
    "Rejected"
    "Expired"
    "Executed"
    "Done"
    "Logs"
    "LinkedIn_Content"
    "LinkedIn_Content/Drafts"
    "LinkedIn_Content/Analytics"
    "Schedules"
    "Briefings"
    "Audits"
)

missing_folders=()

for folder in "${folders[@]}"; do
    if [ -d "$folder" ]; then
        print_success "$folder"
    else
        print_warning "$folder (missing - will create)"
        missing_folders+=("$folder")
    fi
done

if [ ${#missing_folders[@]} -gt 0 ]; then
    echo ""
    read -p "Create missing folders? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for folder in "${missing_folders[@]}"; do
            mkdir -p "$folder"
            print_success "Created $folder"
        done
    fi
fi

echo ""

# Step 2: Check Claude Code skills
echo "Step 2: Checking Claude Code skills..."
echo "----------------------------------------------------------------------"

skills=(
    ".claude/skills/ai-employee-processor/SKILL.md"
    ".claude/skills/browsing-with-playwright/SKILL.md"
    ".claude/skills/linkedin-poster/SKILL.md"
    ".claude/skills/email-sender/SKILL.md"
    ".claude/skills/whatsapp-messenger/SKILL.md"
    ".claude/skills/scheduler/SKILL.md"
    ".claude/skills/approval-manager/SKILL.md"
)

for skill in "${skills[@]}"; do
    if [ -f "$skill" ]; then
        skill_name=$(basename $(dirname "$skill"))
        print_success "$skill_name"
    else
        skill_name=$(basename $(dirname "$skill"))
        print_error "$skill_name (missing)"
    fi
done

echo ""

# Step 3: Check Python dependencies
echo "Step 3: Checking Python dependencies..."
echo "----------------------------------------------------------------------"

python_packages=(
    "google-auth"
    "google-auth-oauthlib"
    "google-api-python-tools"
    "pyyaml"
)

for package in "${python_packages[@]}"; do
    if python3 -c "import ${package//-/_}" 2>/dev/null; then
        print_success "$package"
    else
        print_warning "$package (not installed)"
    fi
done

echo ""

# Step 4: Check Gmail API setup
echo "Step 4: Checking Gmail API setup..."
echo "----------------------------------------------------------------------"

if [ -f "credentials.json" ]; then
    print_success "credentials.json found"
else
    print_warning "credentials.json not found"
    echo "  Please download from Google Cloud Console"
fi

if [ -f "token.pickle" ]; then
    print_success "token.pickle found (authorized)"
else
    print_warning "token.pickle not found (not authorized)"
    echo "  Run: python3 .claude/skills/email-sender/scripts/authorize_gmail.py"
fi

echo ""

# Step 5: Check Playwright server
echo "Step 5: Checking Playwright server..."
echo "----------------------------------------------------------------------"

if pgrep -f "@playwright/mcp" > /dev/null; then
    print_success "Playwright server is running"
else
    print_warning "Playwright server not running"
    echo "  Start with: bash .claude/skills/browsing-with-playwright/scripts/start-server.sh"
fi

echo ""

# Step 6: Check scheduled tasks
echo "Step 6: Checking scheduled tasks..."
echo "----------------------------------------------------------------------"

if command -v crontab &> /dev/null; then
    cron_count=$(crontab -l 2>/dev/null | grep -c "claude" || true)
    if [ $cron_count -gt 0 ]; then
        print_success "Found $cron_count scheduled task(s)"
    else
        print_warning "No scheduled tasks found"
        echo "  See SILVER_TIER_SETUP.md for scheduling instructions"
    fi
else
    print_warning "crontab not available (Windows?)"
    echo "  Use Task Scheduler on Windows"
fi

echo ""

# Summary
echo "======================================================================"
echo "Setup Summary"
echo "======================================================================"
echo ""

print_info "Next steps:"
echo ""
echo "1. If Gmail API not set up:"
echo "   python3 .claude/skills/email-sender/scripts/authorize_gmail.py"
echo ""
echo "2. If Playwright not running:"
echo "   bash .claude/skills/browsing-with-playwright/scripts/start-server.sh"
echo ""
echo "3. Test email sending:"
echo "   python3 .claude/skills/email-sender/scripts/test_email.py your@email.com"
echo ""
echo "4. Set up scheduled tasks:"
echo "   See SILVER_TIER_SETUP.md Step 4"
echo ""
echo "5. Start using skills:"
echo "   claude '/email-sender'"
echo "   claude '/linkedin-poster'"
echo "   claude '/approval-manager'"
echo ""

print_success "Silver Tier setup check complete!"
echo ""
echo "For detailed setup instructions, see: SILVER_TIER_SETUP.md"
echo "For usage examples, see: SILVER_TIER_README.md"
