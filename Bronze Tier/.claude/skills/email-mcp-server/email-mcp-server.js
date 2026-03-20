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
