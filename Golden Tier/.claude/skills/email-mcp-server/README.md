# Email MCP Server

MCP (Model Context Protocol) server for email operations via Gmail API.

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

## Configuration

Add to Claude Code settings (`~/.config/claude-code/settings.json`):

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["/absolute/path/to/email-mcp-server.js"],
      "cwd": "/path/to/vault"
    }
  }
}
```

## Available Tools

- `send_email` - Send email via Gmail
- `draft_email` - Create email draft
- `list_recent_emails` - List recent inbox emails

See SKILL.md for complete documentation.
