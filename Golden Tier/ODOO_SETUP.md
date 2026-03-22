# Odoo Community Edition Setup Guide

## Quick Start

### 1. Start Odoo with Docker Compose

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f odoo
```

### 2. Access Odoo

- **URL**: http://localhost:8069
- **Master Password**: admin_master_password
- **Database Name**: Create new database (e.g., "ai_employee_db")
- **Admin Email**: your-email@example.com
- **Admin Password**: Choose a strong password

### 3. Initial Configuration

1. Create a new database through the web interface
2. Install required modules:
   - **Accounting** (account)
   - **Invoicing** (account_invoicing)
   - **Contacts** (contacts)
   - **Sales** (sale_management)

### 4. Enable JSON-RPC API Access

The Odoo JSON-RPC API is enabled by default on port 8069.

**Test API Connection**:
```python
import xmlrpc.client

url = 'http://localhost:8069'
db = 'ai_employee_db'
username = 'admin@example.com'
password = 'your_admin_password'

# Authenticate
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
print(f"User ID: {uid}")

# Test access
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
partners = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[]], {'fields': ['name', 'email'], 'limit': 5})
print(f"Partners: {partners}")
```

## Docker Commands

```bash
# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v

# Restart Odoo only
docker-compose restart odoo

# View Odoo logs
docker-compose logs -f odoo

# Access Odoo container shell
docker exec -it odoo_app bash

# Access PostgreSQL
docker exec -it odoo_db psql -U odoo -d postgres
```

## Backup and Restore

### Backup Database
```bash
# Backup via Odoo web interface
# Settings > Database Manager > Backup

# Or via command line
docker exec odoo_db pg_dump -U odoo ai_employee_db > backup.sql
```

### Restore Database
```bash
# Via web interface
# Settings > Database Manager > Restore

# Or via command line
docker exec -i odoo_db psql -U odoo -d ai_employee_db < backup.sql
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8069
netstat -ano | findstr :8069

# Change port in docker-compose.yml
ports:
  - "8070:8069"  # Use 8070 instead
```

### Database Connection Issues
```bash
# Check database health
docker-compose logs db

# Restart database
docker-compose restart db
```

### Reset Everything
```bash
# Stop and remove all data
docker-compose down -v

# Start fresh
docker-compose up -d
```

## Security Notes

⚠️ **Important**: This setup is for local development only.

For production:
1. Change all default passwords
2. Use environment variables for secrets
3. Enable SSL/TLS
4. Configure firewall rules
5. Regular backups
6. Update Odoo regularly

## Next Steps

After Odoo is running:
1. Configure company information
2. Set up chart of accounts
3. Create products/services
4. Add customers
5. Test the MCP server integration

## Resources

- [Odoo Documentation](https://www.odoo.com/documentation/19.0/)
- [Odoo JSON-RPC API](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
