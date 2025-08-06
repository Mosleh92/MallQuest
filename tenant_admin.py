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

