import importlib
import database

database.db = None
create_metagross_belt_quest = importlib.import_module(
    "3d_graphics_module"
).create_metagross_belt_quest


def test_metagross_belt_quest_has_red_glint():
    result = create_metagross_belt_quest()
    assert result["status"] == "success"
    quest = result["quest"]
    items = quest["rewards"].get("special_items", [])
    assert any(item.get("name") == "metagross_belt" for item in items)
    belt = next(item for item in items if item.get("name") == "metagross_belt")
    assert "red glint" in belt.get("description", "").lower()
    assert "red_glint" in belt.get("visual_effects", [])
