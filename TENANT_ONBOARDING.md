# Tenant Onboarding Guide

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
