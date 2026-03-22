# Golden Tier Setup Guide

Complete step-by-step guide to set up your Golden Tier AI Employee.

---

## Prerequisites

Before starting, ensure you have:

- ✅ Windows 10/11, macOS, or Linux
- ✅ Python 3.13+ installed
- ✅ Node.js 24+ installed
- ✅ Docker Desktop installed
- ✅ Git installed
- ✅ Claude Code subscription
- ✅ 16GB RAM minimum
- ✅ 50GB free disk space

---

## Part 1: Foundation Setup (30 minutes)

### 1.1 Clone and Navigate
```bash
cd "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Golden Tier"
```

### 1.2 Install Python Dependencies
```bash
# Install watchers dependencies
cd watchers
pip install -r requirements.txt
playwright install chromium

# Install skill dependencies
cd ../.claude/skills/facebook-poster
pip install -r requirements.txt

cd ../instagram-poster
pip install -r requirements.txt

cd ../twitter-poster
pip install -r requirements.txt

cd ../ceo-briefing
pip install -r requirements.txt
```

### 1.3 Install Node.js Dependencies
```bash
# Install Odoo MCP server
cd .claude/skills/odoo-mcp-server
npm install
```

---

## Part 2: Odoo Accounting Setup (20 minutes)

### 2.1 Start Odoo with Docker
```bash
cd "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Golden Tier"

# Start Odoo and PostgreSQL
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f odoo
```

### 2.2 Configure Odoo Web Interface
1. Open browser: http://localhost:8069
2. Create new database:
   - **Database Name**: `ai_employee_db`
   - **Email**: your-email@example.com
   - **Password**: Choose strong password
   - **Language**: English
   - **Country**: Your country

3. Install modules:
   - Go to Apps
   - Search and install: **Accounting**
   - Search and install: **Invoicing**
   - Search and install: **Contacts**

### 2.3 Configure Odoo MCP Server
```bash
cd .claude/skills/odoo-mcp-server

# Copy environment template
cp .env.example .env

# Edit .env file
# ODOO_URL=http://localhost:8069
# ODOO_DB=ai_employee_db
# ODOO_USERNAME=admin
# ODOO_PASSWORD=your_password_from_step_2.2

# Test connection
npm start
```

---

## Part 3: Social Media Setup (30 minutes)

### 3.1 Facebook Setup
```bash
cd .claude/skills/facebook-poster/scripts

# Run setup (browser will open)
python setup_facebook_session.py

# Follow prompts:
# 1. Log into Facebook
# 2. Complete 2FA if required
# 3. Press ENTER when logged in
```

### 3.2 Instagram Setup
```bash
cd .claude/skills/instagram-poster/scripts

# Run setup (browser will open)
python setup_instagram_session.py

# Follow prompts:
# 1. Log into Instagram
# 2. Complete 2FA if required
# 3. Click "Not Now" on save login
# 4. Click "Not Now" on notifications
# 5. Press ENTER when logged in
```

### 3.3 Twitter Setup
```bash
cd .claude/skills/twitter-poster/scripts

# Run setup (browser will open)
python setup_twitter_session.py

# Follow prompts:
# 1. Log into Twitter
# 2. Complete 2FA if required
# 3. Press ENTER when logged in
```

### 3.4 LinkedIn Setup (Already done in Silver Tier)
If not done yet:
```bash
cd .claude/skills/linkedin-poster/scripts
python setup_linkedin_session.py
```

---

## Part 4: Email Setup (10 minutes)

### 4.1 Gmail API Setup
Already completed in Silver Tier. Verify:
```bash
# Check if token.json exists
ls token.json

# If not, run authorization
python authorize_gmail.py
```

---

## Part 5: Business Configuration (15 minutes)

### 5.1 Configure Business Goals
Edit `AI_Employee_Vault/Business_Goals.md`:
```markdown
---
last_updated: 2026-03-21
review_frequency: weekly
---

# Business Goals

## Q1 2026 Objectives

### Revenue Target
- Monthly goal: $10,000  # CHANGE THIS
- Current MTD: $0

### Key Metrics to Track
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Client response time | < 24 hours | > 48 hours |
| Invoice payment rate | > 90% | < 80% |
```

### 5.2 Configure Company Handbook
Edit `AI_Employee_Vault/Company_Handbook.md`:
- Add your business rules
- Define approval thresholds
- Set communication guidelines

### 5.3 Add Customers to Odoo
1. Go to http://localhost:8069
2. Navigate to Contacts
3. Add your customers:
   - Name
   - Email
   - Phone
   - Company type

---

## Part 6: Test Each Integration (30 minutes)

### 6.1 Test Odoo Integration
```bash
cd .claude/skills/odoo-mcp-server

# Test invoice creation
node test_odoo.js
```

### 6.2 Test Facebook Posting
```bash
# Create test approval file
cat > AI_Employee_Vault/Pending_Approval/FACEBOOK_TEST.md << 'EOF'
---
type: facebook_post
status: pending
created: 2026-03-21T20:00:00Z
---

# Facebook Post

Testing my Golden Tier AI Employee! 🚀

This post was created autonomously with human approval.

#AIEmployee #Automation #GoldenTier
EOF

# Move to approved
mv AI_Employee_Vault/Pending_Approval/FACEBOOK_TEST.md AI_Employee_Vault/Approved/

# Post to Facebook
python .claude/skills/facebook-poster/scripts/post_to_facebook.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/facebook/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/FACEBOOK_TEST.md"
```

### 6.3 Test Instagram Posting
```bash
# First, prepare a test image
# Place an image at: AI_Employee_Vault/Media/test_image.jpg

# Create test approval file
cat > AI_Employee_Vault/Pending_Approval/INSTAGRAM_TEST.md << 'EOF'
---
type: instagram_post
status: pending
created: 2026-03-21T20:00:00Z
image_path: AI_Employee_Vault/Media/test_image.jpg
---

# Instagram Post

Testing my Golden Tier AI Employee! 🚀

Autonomous posting with human oversight.

#AIEmployee #Automation #GoldenTier
EOF

# Move to approved
mv AI_Employee_Vault/Pending_Approval/INSTAGRAM_TEST.md AI_Employee_Vault/Approved/

# Post to Instagram
python .claude/skills/instagram-poster/scripts/post_to_instagram.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/instagram/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/INSTAGRAM_TEST.md"
```

### 6.4 Test Twitter Posting
```bash
# Create test approval file
cat > AI_Employee_Vault/Pending_Approval/TWITTER_TEST.md << 'EOF'
---
type: twitter_post
status: pending
created: 2026-03-21T20:00:00Z
thread: false
---

# Twitter Post

Testing my Golden Tier AI Employee! 🚀 Autonomous posting with human oversight. #AIEmployee #Automation
EOF

# Move to approved
mv AI_Employee_Vault/Pending_Approval/TWITTER_TEST.md AI_Employee_Vault/Approved/

# Post to Twitter
python .claude/skills/twitter-poster/scripts/post_to_twitter.py \
  --vault "AI_Employee_Vault" \
  --session "watchers/twitter/.browser-session" \
  --approval-file "AI_Employee_Vault/Approved/TWITTER_TEST.md"
```

### 6.5 Test CEO Briefing
```bash
cd .claude/skills/ceo-briefing

# Generate test briefing
python scripts/generate_briefing.py \
  --vault "../../AI_Employee_Vault" \
  --date-from "2026-03-15" \
  --date-to "2026-03-21"

# Check output
cat ../../AI_Employee_Vault/Briefings/*_Monday_Briefing.md
```

### 6.6 Test Ralph Wiggum Loop
```bash
# Create test task
cat > AI_Employee_Vault/Needs_Action/TEST_TASK.md << 'EOF'
---
type: test_task
created: 2026-03-21T20:00:00Z
---

# Test Task

This is a test task for Ralph Wiggum loop.
EOF

# Start Ralph loop
python .claude/skills/ralph-wiggum-loop/scripts/start_ralph_loop.py \
  --vault "AI_Employee_Vault" \
  --task "Process all files in Needs_Action and move to Done" \
  --max-iterations 5

# Check state
cat .claude/hooks/ralph_state.json
```

---

## Part 7: Schedule Automation (15 minutes)

### 7.1 Windows Task Scheduler

Create scheduled task for CEO Briefing:

```powershell
# Open Task Scheduler
taskschd.msc

# Create new task:
# Name: AI Employee CEO Briefing
# Trigger: Weekly, Sunday, 7:00 PM
# Action: Start a program
#   Program: python
#   Arguments: "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Golden Tier\.claude\skills\ceo-briefing\scripts\generate_briefing.py" --vault "C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Golden Tier\AI_Employee_Vault"
#   Start in: C:\Users\dell\Desktop\Hackathons-0-AI-Employees\Golden Tier
```

### 7.2 Linux/Mac Cron

```bash
# Edit crontab
crontab -e

# Add weekly CEO briefing (Sunday 7 PM)
0 19 * * 0 cd /path/to/Golden\ Tier && python .claude/skills/ceo-briefing/scripts/generate_briefing.py --vault AI_Employee_Vault
```

---

## Part 8: Verification Checklist

### ✅ Infrastructure
- [ ] Docker running
- [ ] Odoo accessible at http://localhost:8069
- [ ] PostgreSQL database created
- [ ] Odoo Accounting module installed

### ✅ Integrations
- [ ] Facebook session saved
- [ ] Instagram session saved
- [ ] Twitter session saved
- [ ] LinkedIn session saved (from Silver Tier)
- [ ] Gmail OAuth configured (from Silver Tier)
- [ ] WhatsApp session saved (from Silver Tier)

### ✅ MCP Servers
- [ ] Odoo MCP server installed
- [ ] Odoo MCP .env configured
- [ ] Email MCP working (from Silver Tier)

### ✅ Skills
- [ ] All 13 skills documented
- [ ] All Python dependencies installed
- [ ] All Node.js dependencies installed

### ✅ Testing
- [ ] Facebook test post successful
- [ ] Instagram test post successful
- [ ] Twitter test post successful
- [ ] CEO briefing generated
- [ ] Ralph loop state created

### ✅ Configuration
- [ ] Business_Goals.md configured
- [ ] Company_Handbook.md reviewed
- [ ] Dashboard.md exists
- [ ] Folder structure complete

---

## Part 9: Daily Operations

### Morning Routine (5 minutes)
1. Check Dashboard.md
2. Review Pending_Approval folder
3. Approve or reject actions
4. Check Logs for overnight activity

### Weekly Routine (15 minutes)
1. Review Monday CEO Briefing
2. Update Business_Goals.md
3. Review revenue in Odoo
4. Check for bottlenecks
5. Adjust automation thresholds

### Monthly Routine (30 minutes)
1. Full system audit
2. Review all logs
3. Update Company_Handbook.md
4. Rotate credentials
5. Backup Odoo database
6. Review subscription costs

---

## Troubleshooting

### Odoo Won't Start
```bash
# Check Docker
docker ps

# Check logs
docker-compose logs odoo

# Restart
docker-compose restart odoo

# Full reset (WARNING: deletes data)
docker-compose down -v
docker-compose up -d
```

### Social Media Session Expired
```bash
# Re-run setup for expired platform
python .claude/skills/facebook-poster/scripts/setup_facebook_session.py
python .claude/skills/instagram-poster/scripts/setup_instagram_session.py
python .claude/skills/twitter-poster/scripts/setup_twitter_session.py
```

### Ralph Loop Won't Stop
```bash
# Manual stop
touch .claude/hooks/STOP_RALPH_LOOP

# Check state
cat .claude/hooks/ralph_state.json

# Delete state (force stop)
rm .claude/hooks/ralph_state.json
```

### CEO Briefing No Revenue Data
```bash
# Check Odoo connection
cd .claude/skills/ceo-briefing
cat .env

# Test Odoo API
python -c "import xmlrpc.client; print('xmlrpc available')"

# Verify Odoo credentials
curl http://localhost:8069
```

---

## Security Checklist

### ✅ Credentials
- [ ] All .env files created from .env.example
- [ ] No credentials in git
- [ ] .gitignore includes .env, token.json, credential.json
- [ ] Browser sessions in .gitignore

### ✅ Approval Workflow
- [ ] All sensitive actions require approval
- [ ] Approval thresholds configured
- [ ] Human review process established

### ✅ Audit Logging
- [ ] All actions logged to /Logs
- [ ] Screenshots captured for social posts
- [ ] Revenue changes tracked

---

## Next Steps

### Immediate (Week 1)
1. Monitor all integrations daily
2. Adjust approval thresholds
3. Fine-tune Business_Goals.md
4. Test each workflow multiple times

### Short-term (Month 1)
1. Optimize automation rules
2. Add more customers to Odoo
3. Create content templates
4. Build reporting dashboards

### Long-term (Quarter 1)
1. Consider Platinum Tier (cloud deployment)
2. Add more integrations
3. Scale to multiple employees
4. Implement advanced analytics

---

## Support Resources

- **Odoo Documentation**: https://www.odoo.com/documentation/19.0/
- **Playwright Docs**: https://playwright.dev/python/
- **Claude Code Docs**: https://docs.anthropic.com/claude-code
- **MCP Protocol**: https://modelcontextprotocol.io/

---

## Congratulations! 🎉

Your Golden Tier AI Employee is now fully operational!

You have successfully implemented:
- ✅ 7 platform integrations
- ✅ 13 agent skills
- ✅ 3 MCP servers
- ✅ Odoo accounting system
- ✅ CEO briefing automation
- ✅ Ralph Wiggum autonomous loop
- ✅ Complete audit logging

**Your AI Employee can now:**
- Manage email, WhatsApp, and social media
- Create invoices and track revenue
- Generate weekly CEO briefings
- Work autonomously on multi-step tasks
- Operate 24/7 with human oversight

**Estimated Time Savings**: 20-30 hours per week

---

*Setup Guide Version: 1.0*
*Last Updated: 2026-03-21*
