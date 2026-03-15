# Personal AI Employee - Bronze Tier

A local-first, autonomous AI assistant built with Claude Code and Obsidian for the Hackathon 0: Building Autonomous FTEs in 2026.

## 🎯 Project Overview

This is a **Bronze Tier** implementation of a Personal AI Employee that:
- Monitors file system for new tasks
- Processes tasks according to defined rules
- Maintains an organized knowledge base in Obsidian
- Provides audit trails and activity logging
- Operates 24/7 with human-in-the-loop oversight

## ✨ Features

### Bronze Tier (Current)
- ✅ Obsidian vault with structured folders
- ✅ Dashboard.md for real-time status
- ✅ Company_Handbook.md for AI behavior rules
- ✅ File System Watcher (monitors Inbox folder)
- ✅ Claude Code integration via Agent Skills
- ✅ Automatic task detection and processing
- ✅ Basic folder workflow (Inbox → Needs_Action → Done)

## 📁 Project Structure

```
Hackathon 0 AI Employees/
├── AI_Employee_Vault/          # Obsidian knowledge base
│   ├── Dashboard.md            # System status dashboard
│   ├── Company_Handbook.md     # AI behavior rules
│   ├── Inbox/                  # Drop zone for new items
│   ├── Needs_Action/           # Pending tasks
│   ├── Done/                   # Completed tasks
│   ├── Plans/                  # Multi-step plans
│   ├── Logs/                   # Audit logs
│   ├── Pending_Approval/       # Awaiting approval
│   ├── Approved/               # Approved actions
│   ├── Rejected/               # Rejected actions
│   ├── Accounting/             # Financial records
│   └── Briefings/              # Generated reports
│
├── watchers/                   # Perception layer
│   ├── base_watcher.py         # Base watcher class
│   ├── filesystem_watcher.py   # File system monitor
│   └── requirements.txt        # Python dependencies
│
├── .claude/skills/             # Claude Code skills
│   └── ai-employee-processor/  # Task processing skill
│
├── SETUP_GUIDE.md              # Installation instructions
├── BRONZE_TIER_COMPLETE.md     # Architecture documentation
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Start the Watcher
```bash
cd watchers
python filesystem_watcher.py ../AI_Employee_Vault
```

### 2. Drop a Test File
```bash
echo "Test task" > AI_Employee_Vault/Inbox/test.txt
```

### 3. Process with Claude Code
```bash
claude "Process all items in Needs_Action following Company_Handbook rules"
```

### 4. Check Results
- View `AI_Employee_Vault/Dashboard.md`
- Check `AI_Employee_Vault/Done/` folder

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed installation and setup
- **[BRONZE_TIER_COMPLETE.md](BRONZE_TIER_COMPLETE.md)** - Architecture and requirements
- **[AI_Employee_Vault/README.md](AI_Employee_Vault/README.md)** - Vault structure
- **[watchers/README.md](watchers/README.md)** - Watcher documentation

## 🏗️ Architecture

```
Files → Watcher → Vault → Claude Code → Actions
         ↓          ↓         ↓           ↓
      Detect    Store     Reason      Execute
```

**Perception Layer**: File System Watcher monitors Inbox/
**Storage Layer**: Obsidian vault stores all data locally
**Reasoning Layer**: Claude Code processes tasks via Agent Skills
**Action Layer**: Updates Dashboard, moves files, creates plans

## 🎓 Hackathon Context

This project is part of **Hackathon 0: Building Autonomous FTEs in 2026** organized by Panaversity.

**Bronze Tier Requirements:**
- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script
- ✅ Claude Code integration
- ✅ Basic folder structure
- ✅ All AI functionality as Agent Skills

**Estimated Time**: 8-12 hours
**Status**: ✅ Complete

## 🔮 Future Enhancements

### Silver Tier
- Gmail watcher
- WhatsApp watcher
- MCP servers for external actions
- Human-in-the-loop approval workflow
- Automated scheduling

### Gold Tier
- Full cross-domain integration
- Odoo accounting system
- Social media automation (LinkedIn, Facebook, Instagram, Twitter)
- Weekly CEO briefings
- Ralph Wiggum autonomous loop

### Platinum Tier
- Cloud deployment (24/7 operation)
- Multi-agent architecture (Cloud + Local)
- Advanced security and monitoring
- Production-ready deployment

## 🛠️ Tech Stack

- **Brain**: Claude Code (Sonnet 4.6)
- **Memory**: Obsidian (Local Markdown)
- **Senses**: Python Watchers
- **Language**: Python 3.13+
- **Architecture**: Local-first, privacy-focused

## 📊 System Status

| Component | Status |
|-----------|--------|
| Vault Structure | ✅ Complete |
| File Watcher | ✅ Working |
| Claude Integration | ✅ Active |
| Agent Skills | ✅ Implemented |
| Documentation | ✅ Complete |

## 🤝 Contributing

This is a hackathon project for learning and experimentation. Feel free to:
- Fork and customize for your needs
- Add new watchers (Gmail, WhatsApp, etc.)
- Implement MCP servers
- Share improvements with the community

## 📅 Weekly Research Meetings

Join the community every Wednesday at 10:00 PM:
- Zoom: https://us06web.zoom.us/j/87188707642
- YouTube: https://www.youtube.com/@panaversity

## 📄 License

This project is built for educational purposes as part of the Panaversity AI Employee Hackathon.

## 🙏 Acknowledgments

- Anthropic for Claude Code
- Obsidian for the knowledge base platform
- Panaversity for organizing the hackathon
- The AI Agent community for inspiration

---

**Built with ❤️ for Hackathon 0: Building Autonomous FTEs in 2026**

*Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*
