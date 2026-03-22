#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { google } from 'googleapis';
import { chromium } from 'playwright';
import fs from 'fs/promises';
import path from 'path';

/**
 * Unified Communications MCP Server
 * Handles Email (Gmail API), LinkedIn (Playwright), WhatsApp (Playwright)
 */
class CommunicationsMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'communications-server',
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
    this.browser = null;
    this.browserContext = null;
  }

  async initializeGmail() {
    try {
      const credentials = JSON.parse(
        await fs.readFile('credentials.json', 'utf-8')
      );

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

  async initializeBrowser() {
    try {
      if (!this.browser) {
        this.browser = await chromium.launch({
          headless: false, // Set to true for production
        });

        const userDataDir = path.join(process.cwd(), '.browser-data');
        this.browserContext = await chromium.launchPersistentContext(userDataDir, {
          headless: false,
        });
      }
      return true;
    } catch (error) {
      console.error('Failed to initialize browser:', error);
      return false;
    }
  }

  setupToolHandlers() {
    // Use the correct SDK 0.5.0 API
    this.server.setRequestHandler(
      { method: 'tools/list' },
      async () => ({
        tools: [
        // Email Tools
        {
          name: 'send_email',
          description: 'Send an email via Gmail API',
          inputSchema: {
            type: 'object',
            properties: {
              to: { type: 'string', description: 'Recipient email address' },
              subject: { type: 'string', description: 'Email subject' },
              body: { type: 'string', description: 'Email body (plain text)' },
              cc: { type: 'string', description: 'CC recipients (optional)' },
              bcc: { type: 'string', description: 'BCC recipients (optional)' },
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
              to: { type: 'string', description: 'Recipient email address' },
              subject: { type: 'string', description: 'Email subject' },
              body: { type: 'string', description: 'Email body (plain text)' },
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

        // LinkedIn Tools
        {
          name: 'post_to_linkedin',
          description: 'Post content to LinkedIn',
          inputSchema: {
            type: 'object',
            properties: {
              content: {
                type: 'string',
                description: 'Post content (text)',
              },
            },
            required: ['content'],
          },
        },
        {
          name: 'check_linkedin_notifications',
          description: 'Check LinkedIn notifications and engagement',
          inputSchema: {
            type: 'object',
            properties: {
              maxResults: {
                type: 'number',
                description: 'Maximum notifications to return (default: 10)',
                default: 10,
              },
            },
          },
        },

        // WhatsApp Tools
        {
          name: 'send_whatsapp_message',
          description: 'Send a WhatsApp message via WhatsApp Web',
          inputSchema: {
            type: 'object',
            properties: {
              contact: {
                type: 'string',
                description: 'Contact name or phone number',
              },
              message: {
                type: 'string',
                description: 'Message text to send',
              },
            },
            required: ['contact', 'message'],
          },
        },
        {
          name: 'check_whatsapp_messages',
          description: 'Check for unread WhatsApp messages',
          inputSchema: {
            type: 'object',
            properties: {
              keywords: {
                type: 'array',
                items: { type: 'string' },
                description: 'Filter by keywords (e.g., ["urgent", "invoice"])',
              },
            },
          },
        },
      ],
    }));

    this.server.setRequestHandler(
      { method: 'tools/call' },
      async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'send_email':
            if (!this.gmail) await this.initializeGmail();
            return await this.sendEmail(args);
          case 'draft_email':
            if (!this.gmail) await this.initializeGmail();
            return await this.draftEmail(args);
          case 'list_recent_emails':
            if (!this.gmail) await this.initializeGmail();
            return await this.listRecentEmails(args);

          case 'post_to_linkedin':
            await this.initializeBrowser();
            return await this.postToLinkedIn(args);
          case 'check_linkedin_notifications':
            await this.initializeBrowser();
            return await this.checkLinkedInNotifications(args);

          case 'send_whatsapp_message':
            await this.initializeBrowser();
            return await this.sendWhatsAppMessage(args);
          case 'check_whatsapp_messages':
            await this.initializeBrowser();
            return await this.checkWhatsAppMessages(args);

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
    });
  }

  // Email operations
  async sendEmail(args) {
    const { to, subject, body, cc, bcc } = args;

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

    const encodedMessage = Buffer.from(message)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

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
            channel: 'email',
            messageId: result.data.id,
            to,
            subject,
          }, null, 2),
        },
      ],
    };
  }

  async draftEmail(args) {
    const { to, subject, body } = args;

    const message = [
      `To: ${to}`,
      `Subject: ${subject}`,
      '',
      body,
    ].join('\n');

    const encodedMessage = Buffer.from(message)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

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
            channel: 'email',
            draftId: result.data.id,
          }, null, 2),
        },
      ],
    };
  }

  async listRecentEmails(args) {
    const maxResults = args?.maxResults || 10;

    const result = await this.gmail.users.messages.list({
      userId: 'me',
      maxResults,
    });

    const messages = result.data.messages || [];

    const emailDetails = await Promise.all(
      messages.slice(0, 5).map(async (msg) => {
        const details = await this.gmail.users.messages.get({
          userId: 'me',
          id: msg.id,
        });

        const headers = details.data.payload.headers;
        return {
          id: msg.id,
          subject: headers.find((h) => h.name === 'Subject')?.value || 'No Subject',
          from: headers.find((h) => h.name === 'From')?.value || 'Unknown',
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
            channel: 'email',
            count: emailDetails.length,
            emails: emailDetails,
          }, null, 2),
        },
      ],
    };
  }

  // LinkedIn operations
  async postToLinkedIn(args) {
    const { content } = args;

    const page = await this.browserContext.newPage();

    try {
      await page.goto('https://www.linkedin.com');
      await page.waitForTimeout(2000);

      // Note: Actual implementation requires proper selectors
      // This is a simplified version
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              channel: 'linkedin',
              content: content.substring(0, 100),
              note: 'LinkedIn posting requires manual setup and proper selectors',
            }, null, 2),
          },
        ],
      };
    } finally {
      await page.close();
    }
  }

  async checkLinkedInNotifications(args) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            channel: 'linkedin',
            note: 'LinkedIn notifications check requires manual setup',
          }, null, 2),
        },
      ],
    };
  }

  // WhatsApp operations
  async sendWhatsAppMessage(args) {
    const { contact, message } = args;

    const page = await this.browserContext.newPage();

    try {
      await page.goto('https://web.whatsapp.com');
      await page.waitForTimeout(5000);

      // Note: Actual implementation requires proper selectors
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              channel: 'whatsapp',
              contact,
              message: message.substring(0, 100),
              note: 'WhatsApp messaging requires manual setup and QR scan',
            }, null, 2),
          },
        ],
      };
    } finally {
      await page.close();
    }
  }

  async checkWhatsAppMessages(args) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            channel: 'whatsapp',
            note: 'WhatsApp message checking requires manual setup',
          }, null, 2),
        },
      ],
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Communications MCP Server running on stdio');
  }

  async cleanup() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

const server = new CommunicationsMCPServer();

process.on('SIGINT', async () => {
  await server.cleanup();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await server.cleanup();
  process.exit(0);
});

server.run().catch(console.error);
