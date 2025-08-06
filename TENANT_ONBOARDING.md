# Tenant Onboarding Guide

 codex/refactor-for-tenant-database-support
This guide describes how to onboard new mall tenants with custom domains and themes.

## Adding a New Tenant

1. Create a database schema or file for the tenant.
2. Register the tenant using the admin tool:
   ```bash
   python tenant_admin.py add --domain mall.example.com \
       --schema mall_example.db --name "Example Mall" --theme ocean
   ```
3. Configure DNS so the custom domain points to the application server.
4. Provide theme assets in your templates or static files according to the `tenant_theme` value.

## Listing Tenants

To view configured tenants, run:
```bash
python tenant_admin.py list
```

## Request Handling

The web interface inspects the request domain and loads the matching tenant. Each tenant uses its own database schema and branding, allowing isolated data storage and custom themes.
=======
This guide explains how to onboard a new mall (tenant) into the MallQuest platform with its own database schema, domain, and branding.

## 1. Configure Tenant Settings
Tenant settings are stored in `tenants.json`. Each tenant includes a domain, database schema, and branding details such as name, theme, and logo.

Example entry:
```json
{
  "deerfields": {
    "name": "Deerfields Mall",
    "domain": "mystore.example.com",
    "schema": "deerfields",
    "theme": "default",
    "logo": "/static/img/deerfields.png"
  }
}
```

## 2. Use the Tenant Admin Tool
The `tenant_admin.py` utility simplifies adding and listing tenants.

### Add a Tenant
```bash
python tenant_admin.py add deerfields mystore.example.com deerfields \
    --name "Deerfields Mall" --theme default --logo /static/img/deerfields.png
```

### List Tenants
```bash
python tenant_admin.py list
```

## 3. Restart the Web Application
After updating tenant settings, restart the web application to load the new configuration. Incoming requests will automatically map to the correct tenant based on the request host and apply the appropriate branding.
 main
