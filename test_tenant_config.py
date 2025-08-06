import json
from config import TenantManager


def reset_manager():
    TenantManager._tenants = {}


def test_load_and_get_tenant(tmp_path, monkeypatch):
    data = {"example.com": {"schema": "example.db", "name": "Example", "theme": "dark"}}
    cfg = tmp_path / "tenants.json"
    cfg.write_text(json.dumps(data))
    monkeypatch.setenv("TENANT_CONFIG_PATH", str(cfg))
    from config import BaseConfig
    BaseConfig.TENANT_CONFIG_PATH = str(cfg)
    reset_manager()

    tenants = TenantManager.load_tenants()
    assert tenants["example.com"]["schema"] == "example.db"

    tenant = TenantManager.get_tenant("example.com")
    assert tenant["theme"] == "dark"


def test_add_tenant(tmp_path, monkeypatch):
    cfg = tmp_path / "tenants.json"
    monkeypatch.setenv("TENANT_CONFIG_PATH", str(cfg))
    from config import BaseConfig
    BaseConfig.TENANT_CONFIG_PATH = str(cfg)
    reset_manager()

    TenantManager.add_tenant("mymall.com", "mall.db", "My Mall", theme="light")
    assert json.loads(cfg.read_text())["mymall.com"]["name"] == "My Mall"
