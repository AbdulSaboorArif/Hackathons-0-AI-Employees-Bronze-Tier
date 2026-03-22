# Odoo MCP Server Skill

**Description**: MCP server for Odoo accounting integration via JSON-RPC API. Manages invoices, customers, and revenue tracking.

## Capabilities

- Create customer invoices
- Query invoices by state
- Manage customers/partners
- Calculate revenue for periods
- Full Odoo accounting integration

## Setup

1. **Start Odoo with Docker**:
```bash
docker-compose up -d
```

2. **Configure Odoo**:
- Access http://localhost:8069
- Create database: `ai_employee_db`
- Install Accounting module
- Note admin credentials

3. **Install Dependencies**:
```bash
cd .claude/skills/odoo-mcp-server
npm install
```

4. **Configure Environment**:
```bash
cp .env.example .env
# Edit .env with your Odoo credentials
```

5. **Test Connection**:
```bash
npm start
```

## MCP Tools

### odoo_create_invoice
Create a customer invoice in Odoo.

**Parameters**:
- `partner_name` (string, required): Customer name
- `partner_email` (string): Customer email
- `invoice_lines` (array, required): Line items
  - `product_name` (string): Product/service name
  - `quantity` (number): Quantity
  - `price_unit` (number): Unit price
  - `description` (string): Line description

**Example**:
```json
{
  "partner_name": "Client A",
  "partner_email": "client@example.com",
  "invoice_lines": [
    {
      "product_name": "Consulting Services",
      "quantity": 10,
      "price_unit": 150.00,
      "description": "January 2026 consulting hours"
    }
  ]
}
```

### odoo_get_invoices
Get list of invoices from Odoo.

**Parameters**:
- `state` (string): Filter by state (draft, posted, cancel)
- `limit` (number): Max results (default: 10)

### odoo_get_partners
Get list of customers/partners.

**Parameters**:
- `search_term` (string): Search by name or email
- `limit` (number): Max results (default: 10)

### odoo_get_revenue
Calculate revenue for a period.

**Parameters**:
- `date_from` (string, required): Start date (YYYY-MM-DD)
- `date_to` (string, required): End date (YYYY-MM-DD)

**Example**:
```json
{
  "date_from": "2026-01-01",
  "date_to": "2026-01-31"
}
```

### odoo_create_partner
Create a new customer/partner.

**Parameters**:
- `name` (string, required): Partner name
- `email` (string): Email address
- `phone` (string): Phone number
- `company_type` (string): "person" or "company"

## Usage in Claude Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "odoo": {
      "command": "node",
      "args": [
        "/path/to/.claude/skills/odoo-mcp-server/index.js"
      ],
      "env": {
        "ODOO_URL": "http://localhost:8069",
        "ODOO_DB": "ai_employee_db",
        "ODOO_USERNAME": "admin",
        "ODOO_PASSWORD": "your_password"
      }
    }
  }
}
```

## Workflow Integration

### Invoice Creation Flow
1. WhatsApp/Email request detected
2. Claude creates approval file in `/Pending_Approval/`
3. Human approves
4. Claude calls `odoo_create_invoice`
5. Invoice created in Odoo
6. Task moved to `/Done/`

### Weekly Revenue Audit
1. Scheduled task runs Sunday night
2. Claude calls `odoo_get_revenue` for past week
3. Generates CEO Briefing with revenue data
4. Saves to `/Briefings/`

## Security

⚠️ **Important**:
- Never commit `.env` file
- Use strong Odoo admin password
- Restrict Odoo access to localhost
- Enable audit logging
- Regular backups

## Troubleshooting

**Connection refused**:
```bash
# Check Odoo is running
docker-compose ps

# Check logs
docker-compose logs odoo
```

**Authentication failed**:
- Verify credentials in `.env`
- Check database name matches
- Ensure user has access rights

**Module not found**:
```bash
# Reinstall dependencies
npm install
```

## Resources

- [Odoo JSON-RPC API](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html)
- [MCP SDK Documentation](https://modelcontextprotocol.io/)
