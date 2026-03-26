"""Пример для топика 10: загрузка инвентаря из JSON."""
from __future__ import annotations

import json
from pathlib import Path


def load_inventory(path: Path) -> list[dict]:
    """Читает список устройств из JSON. Путь — относительно корня курса pythonAI."""
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("Ожидался JSON-массив устройств")
    return data


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    inv = load_inventory(root / "labs" / "inventory.json")
    for d in inv:
        print(d["hostname"], d.get("host"), d.get("role"))
