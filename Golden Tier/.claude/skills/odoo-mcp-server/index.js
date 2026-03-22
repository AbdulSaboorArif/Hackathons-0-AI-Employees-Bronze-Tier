#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import xmlrpc from 'xmlrpc';
import dotenv from 'dotenv';

dotenv.config();

// Odoo configuration
const ODOO_URL = process.env.ODOO_URL || 'http://localhost:8069';
const ODOO_DB = process.env.ODOO_DB || 'ai_employee_db';
const ODOO_USERNAME = process.env.ODOO_USERNAME || 'admin';
const ODOO_PASSWORD = process.env.ODOO_PASSWORD || '';

class OdooMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'odoo-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.uid = null;
    this.setupHandlers();
  }

  async authenticate() {
    if (this.uid) return this.uid;

    const common = xmlrpc.createClient({ url: `${ODOO_URL}/xmlrpc/2/common` });

    return new Promise((resolve, reject) => {
      common.methodCall('authenticate', [ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {}], (error, uid) => {
        if (error) {
          reject(new Error(`Authentication failed: ${error.message}`));
        } else if (!uid) {
          reject(new Error('Authentication failed: Invalid credentials'));
        } else {
          this.uid = uid;
          resolve(uid);
        }
      });
    });
  }

  async executeOdoo(model, method, args = [], kwargs = {}) {
    await this.authenticate();

    const models = xmlrpc.createClient({ url: `${ODOO_URL}/xmlrpc/2/object` });

    return new Promise((resolve, reject) => {
      models.methodCall('execute_kw', [
        ODOO_DB,
        this.uid,
        ODOO_PASSWORD,
        model,
        method,
        args,
        kwargs
      ], (error, result) => {
        if (error) {
          reject(new Error(`Odoo API error: ${error.message}`));
        } else {
          resolve(result);
        }
      });
    });
  }

  setupHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'odoo_create_invoice',
          description: 'Create a customer invoice in Odoo',
          inputSchema: {
            type: 'object',
            properties: {
              partner_name: {
                type: 'string',
                description: 'Customer name',
              },
              partner_email: {
                type: 'string',
                description: 'Customer email',
              },
              invoice_lines: {
                type: 'array',
                description: 'Invoice line items',
                items: {
                  type: 'object',
                  properties: {
                    product_name: { type: 'string' },
                    quantity: { type: 'number' },
                    price_unit: { type: 'number' },
                    description: { type: 'string' },
                  },
                  required: ['product_name', 'quantity', 'price_unit'],
                },
              },
            },
            required: ['partner_name', 'invoice_lines'],
          },
        },
        {
          name: 'odoo_get_invoices',
          description: 'Get list of invoices from Odoo',
          inputSchema: {
            type: 'object',
            properties: {
              state: {
                type: 'string',
                description: 'Invoice state: draft, posted, cancel',
                enum: ['draft', 'posted', 'cancel'],
              },
              limit: {
                type: 'number',
                description: 'Maximum number of invoices to return',
                default: 10,
              },
            },
          },
        },
        {
          name: 'odoo_get_partners',
          description: 'Get list of customers/partners from Odoo',
          inputSchema: {
            type: 'object',
            properties: {
              search_term: {
                type: 'string',
                description: 'Search by name or email',
              },
              limit: {
                type: 'number',
                description: 'Maximum number of partners to return',
                default: 10,
              },
            },
          },
        },
        {
          name: 'odoo_get_revenue',
          description: 'Get revenue summary for a period',
          inputSchema: {
            type: 'object',
            properties: {
              date_from: {
                type: 'string',
                description: 'Start date (YYYY-MM-DD)',
              },
              date_to: {
                type: 'string',
                description: 'End date (YYYY-MM-DD)',
              },
            },
            required: ['date_from', 'date_to'],
          },
        },
        {
          name: 'odoo_create_partner',
          description: 'Create a new customer/partner in Odoo',
          inputSchema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
                description: 'Partner name',
              },
              email: {
                type: 'string',
                description: 'Partner email',
              },
              phone: {
                type: 'string',
                description: 'Partner phone',
              },
              company_type: {
                type: 'string',
                description: 'Type: person or company',
                enum: ['person', 'company'],
                default: 'person',
              },
            },
            required: ['name'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        const { name, arguments: args } = request.params;

        switch (name) {
          case 'odoo_create_invoice':
            return await this.createInvoice(args);
          case 'odoo_get_invoices':
            return await this.getInvoices(args);
          case 'odoo_get_partners':
            return await this.getPartners(args);
          case 'odoo_get_revenue':
            return await this.getRevenue(args);
          case 'odoo_create_partner':
            return await this.createPartner(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  async createPartner(args) {
    const partnerData = {
      name: args.name,
      email: args.email || false,
      phone: args.phone || false,
      company_type: args.company_type || 'person',
    };

    const partnerId = await this.executeOdoo('res.partner', 'create', [partnerData]);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            partner_id: partnerId,
            message: `Partner created: ${args.name}`,
          }, null, 2),
        },
      ],
    };
  }

  async createInvoice(args) {
    // Find or create partner
    let partnerId;
    const partners = await this.executeOdoo('res.partner', 'search_read', [
      [['name', '=', args.partner_name]],
      { fields: ['id'], limit: 1 }
    ]);

    if (partners.length > 0) {
      partnerId = partners[0].id;
    } else {
      partnerId = await this.executeOdoo('res.partner', 'create', [{
        name: args.partner_name,
        email: args.partner_email || false,
      }]);
    }

    // Create invoice lines
    const invoiceLines = [];
    for (const line of args.invoice_lines) {
      invoiceLines.push([0, 0, {
        name: line.description || line.product_name,
        quantity: line.quantity,
        price_unit: line.price_unit,
      }]);
    }

    // Create invoice
    const invoiceData = {
      partner_id: partnerId,
      move_type: 'out_invoice',
      invoice_line_ids: invoiceLines,
    };

    const invoiceId = await this.executeOdoo('account.move', 'create', [invoiceData]);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            invoice_id: invoiceId,
            partner_id: partnerId,
            message: `Invoice created for ${args.partner_name}`,
          }, null, 2),
        },
      ],
    };
  }

  async getInvoices(args) {
    const domain = [];
    if (args.state) {
      domain.push(['state', '=', args.state]);
    }
    domain.push(['move_type', '=', 'out_invoice']);

    const invoices = await this.executeOdoo('account.move', 'search_read', [
      domain,
      {
        fields: ['name', 'partner_id', 'amount_total', 'state', 'invoice_date'],
        limit: args.limit || 10,
        order: 'invoice_date desc',
      }
    ]);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            count: invoices.length,
            invoices: invoices,
          }, null, 2),
        },
      ],
    };
  }

  async getPartners(args) {
    const domain = [];
    if (args.search_term) {
      domain.push('|', ['name', 'ilike', args.search_term], ['email', 'ilike', args.search_term]);
    }

    const partners = await this.executeOdoo('res.partner', 'search_read', [
      domain,
      {
        fields: ['name', 'email', 'phone', 'company_type'],
        limit: args.limit || 10,
      }
    ]);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            count: partners.length,
            partners: partners,
          }, null, 2),
        },
      ],
    };
  }

  async getRevenue(args) {
    const domain = [
      ['move_type', '=', 'out_invoice'],
      ['state', '=', 'posted'],
      ['invoice_date', '>=', args.date_from],
      ['invoice_date', '<=', args.date_to],
    ];

    const invoices = await this.executeOdoo('account.move', 'search_read', [
      domain,
      { fields: ['amount_total', 'invoice_date', 'partner_id'] }
    ]);

    const totalRevenue = invoices.reduce((sum, inv) => sum + inv.amount_total, 0);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            period: `${args.date_from} to ${args.date_to}`,
            total_revenue: totalRevenue,
            invoice_count: invoices.length,
            invoices: invoices,
          }, null, 2),
        },
      ],
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Odoo MCP server running on stdio');
  }
}

const server = new OdooMCPServer();
server.run().catch(console.error);
