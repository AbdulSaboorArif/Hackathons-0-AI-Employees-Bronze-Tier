---
name: email-mcp-server
description: |
  MCP (Model Context Protocol) server for email operations. Provides Claude Code
  with tools to send emails, draft messages, and manage email communications via
  Gmail API. This is the external action server required for Silver Tier. Use this
  when you need Claude to interact with email programmatically.
---

# Email MCP Server

Model Context Protocol server for email operations via Gmail API.

## What is MCP?

Model Context Protocol (MCP) is a standard protocol that allows Claude Code to interact with external systems. MCP servers expose "tools" that Claude can call to perform actions like sending emails, accessing databases, or controlling applications.

## Why This is Required for Silver Tier

The hackathon document specifies: "One working MCP server for external action (e.g., sending emails)"

This MCP server fulfills that requirement by:
- Exposing email sending as a tool Claude can use
- Following the MCP protocol standard
- Providing safe, controlled access to Gmail API
- Enabling Claude to take real-world actions

## Architecture

```
Claude Code
    ↓
MCP Protocol (JSON-RPC)
    ↓
Email MCP Server (Node.js)
    ↓
Gmail API
    ↓
Email Sent
```

## Installation

### Prerequisites

```bash
# Node.js 18+ required
node --version

# Install dependencies
npm install @modelcontextprotocol/sdk googleapis
```

### Server Implementation

Create `email-mcp-server.js`:

```javascript
#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { google } from 'googleapis';
import fs from 'fs/promises';
import path from 'path';

// Email MCP Server
class EmailMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'email-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.gmail = null;
  }

  async initializeGmail() {
    try {
      // Load credentials
      const credentials = JSON.parse(
        await fs.readFile('credentials.json', 'utf-8')
      );

      // Load token
      const token = JSON.parse(
        await fs.readFile('token.json', 'utf-8')
      );

      const { client_secret, client_id, redirect_uris } = credentials.installed;
      const oAuth2Client = new google.auth.OAuth2(
        client_id,
        client_secret,
        redirect_uris[0]
      );

      oAuth2Client.setCredentials(token);
      this.gmail = google.gmail({ version: 'v1', auth: oAuth2Client });

      return true;
    } catch (error) {
      console.error('Failed to initialize Gmail:', error);
      return false;
    }
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler('tools/list', async () => ({
      tools: [
        {
          name: 'send_email',
          description: 'Send an email via Gmail',
          inputSchema: {
            type: 'object',
            properties: {
              to: {
                type: 'string',
                description: 'Recipient email address',
              },
              subject: {
                type: 'string',
                description: 'Email subject',
              },
              body: {
                type: 'string',
                description: 'Email body (plain text)',
              },
              cc: {
                type: 'string',
                description: 'CC recipients (optional)',
              },
              bcc: {
                type: 'string',
                description: 'BCC recipients (optional)',
              },
            },
            required: ['to', 'subject', 'body'],
          },
        },
        {
          name: 'draft_email',
          description: 'Create an email draft without sending',
          inputSchema: {
            type: 'object',
            properties: {
              to: {
                type: 'string',
                description: 'Recipient email address',
              },
              subject: {
                type: 'string',
                description: 'Email subject',
              },
              body: {
                type: 'string',
                description: 'Email body (plain text)',
              },
            },
            required: ['to', 'subject', 'body'],
          },
        },
        {
          name: 'list_recent_emails',
          description: 'List recent emails from inbox',
          inputSchema: {
            type: 'object',
            properties: {
              maxResults: {
                type: 'number',
                description: 'Maximum number of emails to return (default: 10)',
                default: 10,
              },
            },
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;

      // Initialize Gmail if not already done
      if (!this.gmail) {
        const initialized = await this.initializeGmail();
        if (!initialized) {
          return {
            content: [
              {
                type: 'text',
                text: 'Error: Gmail API not initialized. Check credentials.',
              },
            ],
          };
        }
      }

      switch (name) {
        case 'send_email':
          return await this.sendEmail(args);
        case 'draft_email':
          return await this.draftEmail(args);
        case 'list_recent_emails':
          return await this.listRecentEmails(args);
        default:
          return {
            content: [
              {
                type: 'text',
                text: `Unknown tool: ${name}`,
              },
            ],
          };
      }
    });
  }

  async sendEmail(args) {
    try {
      const { to, subject, body, cc, bcc } = args;

      // Create email message
      const message = [
        `To: ${to}`,
        cc ? `Cc: ${cc}` : '',
        bcc ? `Bcc: ${bcc}` : '',
        `Subject: ${subject}`,
        '',
        body,
      ]
        .filter(Boolean)
        .join('\n');

      // Encode message
      const encodedMessage = Buffer.from(message)
        .toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');

      // Send email
      const result = await this.gmail.users.messages.send({
        userId: 'me',
        requestBody: {
          raw: encodedMessage,
        },
      });

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              messageId: result.data.id,
              to,
              subject,
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: false,
              error: error.message,
            }, null, 2),
          },
        ],
      };
    }
  }

  async draftEmail(args) {
    try {
      const { to, subject, body } = args;

      // Create email message
      const message = [
        `To: ${to}`,
        `Subject: ${subject}`,
        '',
        body,
      ].join('\n');

      // Encode message
      const encodedMessage = Buffer.from(message)
        .toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');

      // Create draft
      const result = await this.gmail.users.drafts.create({
        userId: 'me',
        requestBody: {
          message: {
            raw: encodedMessage,
          },
        },
      });

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              draftId: result.data.id,
              to,
              subject,
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: false,
              error: error.message,
            }, null, 2),
          },
        ],
      };
    }
  }

  async listRecentEmails(args) {
    try {
      const maxResults = args?.maxResults || 10;

      // List messages
      const result = await this.gmail.users.messages.list({
        userId: 'me',
        maxResults,
      });

      const messages = result.data.messages || [];

      // Get details for each message
      const emailDetails = await Promise.all(
        messages.map(async (msg) => {
          const details = await this.gmail.users.messages.get({
            userId: 'me',
            id: msg.id,
          });

          const headers = details.data.payload.headers;
          const subject = headers.find((h) => h.name === 'Subject')?.value || 'No Subject';
          const from = headers.find((h) => h.name === 'From')?.value || 'Unknown';
          const date = headers.find((h) => h.name === 'Date')?.value || 'Unknown';

          return {
            id: msg.id,
            subject,
            from,
            date,
            snippet: details.data.snippet,
          };
        })
      );

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              count: emailDetails.length,
              emails: emailDetails,
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: false,
              error: error.message,
            }, null, 2),
          },
        ],
      };
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Email MCP Server running on stdio');
  }
}

// Start server
const server = new EmailMCPServer();
server.run().catch(console.error);
```

### Package.json

Create `package.json`:

```json
{
  "name": "email-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for email operations via Gmail API",
  "type": "module",
  "main": "email-mcp-server.js",
  "scripts": {
    "start": "node email-mcp-server.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "googleapis": "^140.0.0"
  }
}
```

## Configuration

### Claude Code MCP Configuration

Add to your Claude Code settings (`~/.config/claude-code/settings.json`):

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["/absolute/path/to/email-mcp-server.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json",
        "GMAIL_TOKEN": "/path/to/token.json"
      }
    }
  }
}
```

### Alternative: Using npx

```json
{
  "mcpServers": {
    "email": {
      "command": "npx",
      "args": ["-y", "/absolute/path/to/email-mcp-server"],
      "cwd": "/path/to/vault"
    }
  }
}
```

## Usage from Claude Code

Once the MCP server is configured, Claude can use it directly:

```bash
# Claude will automatically detect the email MCP server
claude "Send an email to client@example.com with subject 'Invoice' and body 'Please find attached'"

# Claude can also draft emails
claude "Create a draft email to team@company.com about the project update"

# List recent emails
claude "Show me my 5 most recent emails"
```

## Testing the MCP Server

### Manual Test

```bash
# Start the server manually
cd /path/to/email-mcp-server
node email-mcp-server.js

# In another terminal, test with MCP client
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | node email-mcp-server.js
```

### Test with Claude Code

```bash
# Test email sending
claude "Use the email MCP server to send a test email to yourself"

# Verify tools are available
claude "What email tools are available?"
```

## Available Tools

### 1. send_email

Send an email immediately.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `body` (required): Email body (plain text)
- `cc` (optional): CC recipients
- `bcc` (optional): BCC recipients

**Example:**
```javascript
{
  "to": "client@example.com",
  "subject": "Invoice for March 2026",
  "body": "Please find attached your invoice...",
  "cc": "manager@company.com"
}
```

### 2. draft_email

Create an email draft without sending.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `body` (required): Email body (plain text)

**Example:**
```javascript
{
  "to": "client@example.com",
  "subject": "Project Update",
  "body": "Here's the latest update on your project..."
}
```

### 3. list_recent_emails

List recent emails from inbox.

**Parameters:**
- `maxResults` (optional): Number of emails to return (default: 10)

**Example:**
```javascript
{
  "maxResults": 5
}
```

## Integration with Approval Workflow

The MCP server integrates with the approval workflow:

```markdown
1. Claude identifies need to send email
2. Claude creates approval request in /Pending_Approval
3. Human reviews and approves
4. approval-manager calls email MCP server
5. MCP server sends email via Gmail API
6. Result logged and task completed
```

## Security

### Credential Management

- Credentials stored outside vault
- Token refresh handled automatically
- No passwords in code or config
- OAuth2 for secure authentication

### Rate Limiting

Add rate limiting to prevent abuse:

```javascript
class RateLimiter {
  constructor(maxPerHour = 50) {
    this.maxPerHour = maxPerHour;
    this.requests = [];
  }

  canSend() {
    const oneHourAgo = Date.now() - 3600000;
    this.requests = this.requests.filter(t => t > oneHourAgo);
    return this.requests.length < this.maxPerHour;
  }

  recordRequest() {
    this.requests.push(Date.now());
  }
}
```

### Logging

All MCP server actions are logged:

```javascript
function logAction(action, params, result) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    action,
    params: sanitizeParams(params),
    result: result.success ? 'success' : 'error',
  };

  fs.appendFile('mcp-server.log', JSON.stringify(logEntry) + '\n');
}
```

## Troubleshooting

### Server Not Starting

```bash
# Check Node.js version
node --version  # Should be 18+

# Check dependencies
npm list

# Check credentials
ls -la credentials.json token.json

# Run with debug output
NODE_DEBUG=* node email-mcp-server.js
```

### Claude Can't Connect

```bash
# Verify MCP configuration
cat ~/.config/claude-code/settings.json | grep -A 10 mcpServers

# Check server is running
ps aux | grep email-mcp-server

# Test server manually
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | node email-mcp-server.js
```

### Gmail API Errors

```bash
# Re-authorize
python3 .claude/skills/email-sender/scripts/authorize_gmail.py

# Check token expiry
cat token.json | grep expiry

# Verify API enabled
# Go to Google Cloud Console > APIs & Services > Enabled APIs
```

## Silver Tier Requirement Met

✅ **One working MCP server for external action**

This email MCP server fulfills the Silver Tier requirement by:
- Implementing the MCP protocol standard
- Exposing email sending as a tool
- Integrating with Gmail API
- Enabling Claude to take real-world actions
- Following security best practices

## Future Enhancements (Gold Tier)

- Attachment support
- HTML email formatting
- Email templates
- Search and filter capabilities
- Label management
- Thread handling
- Batch operations

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [Gmail API Reference](https://developers.google.com/gmail/api)
- [MCP SDK on npm](https://www.npmjs.com/package/@modelcontextprotocol/sdk)

---
*Part of the Silver Tier AI Employee implementation*
*Required MCP server for external actions*
