 codex/refactor-for-tenant-database-support
#!/usr/bin/env python3
"""Admin utility for managing tenant onboarding.

Allows adding new malls with custom domains, database schemas, and themes.
"""
import argparse

from config import TenantManager


def cmd_add(args: argparse.Namespace) -> None:
    TenantManager.add_tenant(args.domain, args.schema, args.name, args.theme)
    print(f"Tenant '{args.domain}' registered.")


def cmd_list(args: argparse.Namespace) -> None:
    tenants = TenantManager.load_tenants()
    for domain, data in tenants.items():
        theme = data.get("theme", "default")
        print(f"{domain}: {data['name']} (schema={data['schema']}, theme={theme})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tenant administration tool")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Add a new tenant")
    add_p.add_argument("--domain", required=True, help="Domain for the tenant")
    add_p.add_argument("--schema", required=True, help="Database path for tenant")
    add_p.add_argument("--name", required=True, help="Display name")
    add_p.add_argument("--theme", default="default", help="Theme identifier")
    add_p.set_defaults(func=cmd_add)

    list_p = sub.add_parser("list", help="List configured tenants")
    list_p.set_defaults(func=cmd_list)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
=======
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict

CONFIG_FILE = Path('tenants.json')


@dataclass
class TenantSettings:
    name: str
    domain: str
    schema: str
    theme: str = 'default'
    logo: str = ''


class TenantAdmin:
    """Utility class for managing tenant configurations."""

    def __init__(self, config_file: Path = CONFIG_FILE):
        self.config_file = config_file
        self.tenants: Dict[str, TenantSettings] = self.load()

    def load(self) -> Dict[str, TenantSettings]:
        if self.config_file.exists():
            data = json.loads(self.config_file.read_text())
            return {k: TenantSettings(**v) for k, v in data.items()}
        return {}

    def save(self) -> None:
        self.config_file.write_text(
            json.dumps({k: asdict(v) for k, v in self.tenants.items()}, indent=2)
        )

    def add_tenant(self, key: str, settings: TenantSettings) -> None:
        self.tenants[key] = settings
        self.save()

    def list_tenants(self) -> Dict[str, TenantSettings]:
        return self.tenants


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage tenant configurations")
    sub = parser.add_subparsers(dest="cmd")

    add_p = sub.add_parser("add", help="Add a new tenant")
    add_p.add_argument("key", help="Tenant identifier")
    add_p.add_argument("domain", help="Custom domain for tenant")
    add_p.add_argument("schema", help="Database schema name")
    add_p.add_argument("--name", default="", help="Display name")
    add_p.add_argument("--theme", default="default", help="Theme identifier")
    add_p.add_argument("--logo", default="", help="Path to logo image")

    sub.add_parser("list", help="List existing tenants")

    args = parser.parse_args()
    admin = TenantAdmin()

    if args.cmd == "add":
        settings = TenantSettings(
            name=args.name or args.key,
            domain=args.domain,
            schema=args.schema,
            theme=args.theme,
            logo=args.logo,
        )
        admin.add_tenant(args.key, settings)
        print(f"Tenant '{args.key}' added")
    elif args.cmd == "list":
        for key, tenant in admin.list_tenants().items():
            print(f"{key}: {asdict(tenant)}")
    else:
        parser.print_help()
 main
