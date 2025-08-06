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
