# Communications MCP Server

**Unified MCP server for all communication channels: Email, LinkedIn, WhatsApp**

## Quick Start

```bash
# Install dependencies
npm install

# Install Playwright browsers
npx playwright install chromium

# Start server
npm start
```

## Configuration

Add to Claude Code settings (`~/.config/claude-code/settings.json`):

```json
{
  "mcpServers": {
    "communications": {
      "command": "node",
      "args": ["/absolute/path/to/communications-mcp-server.js"],
      "cwd": "/path/to/vault"
    }
  }
}
```

## Available Tools

### Email (Gmail API)
- `send_email` - Send email
- `draft_email` - Create draft
- `list_recent_emails` - List inbox

### LinkedIn (Playwright)
- `post_to_linkedin` - Post content
- `check_linkedin_notifications` - Check notifications

### WhatsApp (Playwright)
- `send_whatsapp_message` - Send message
- `check_whatsapp_messages` - Check unread

## Prerequisites

- Node.js 18+
- Gmail API credentials (credentials.json, token.json)
- First-time login to LinkedIn and WhatsApp Web

## Testing

```bash
# Test email
claude "Send test email to yourself"

# Test LinkedIn
claude "Post to LinkedIn: Test post"

# Test WhatsApp
claude "Check WhatsApp for urgent messages"
```

## Silver Tier Requirement

✅ **One working MCP server for external action (e.g., sending emails, posting LinkedIn, WhatsApp)**

This unified server handles ALL external communication actions required for Silver Tier.

See SKILL.md for complete documentation.
