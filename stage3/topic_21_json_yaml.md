# Топик 21. JSON и YAML

## Цели

- Читать и писать **JSON** (`json`) и **YAML** (`yaml.safe_load` / `safe_dump`).
- Использовать структурированные файлы для инвентаря и параметров шаблонов.

## Теория (тезисы)

- **JSON** — подмножество для обмена данными; ключи в кавычках; типы: object, array, string, number, bool, null.
- **`json.load` / `json.loads`** — из файла/строки; **`dump(s)`** — обратно; `indent=2` для читаемости.
- **YAML** удобен людям; **никогда** не используйте `yaml.load` без ограничений — только **`safe_load`**.
- Вложенные структуры отражают инвентарь: группы, хосты, переменные.

## Пример

```python
import json
from pathlib import Path

data = json.loads(Path("../labs/inventory.json").read_text(encoding="utf-8"))
```

## Практика

1. Прочитайте [`../labs/inventory.json`](../labs/inventory.json), добавьте поле `"site": "LAB"` каждому устройству и сохраните в `artifacts/inventory_patched.json`.
2. Конвертируйте тот же инвентарь в YAML (`pyyaml`) в `artifacts/inventory_patched.yaml`.
3. Напишите функцию `load_inventory(path: Path) -> list[dict]` с обработкой `JSONDecodeError`.
4. **Сеть:** сопоставьте ключи YAML-инвентаря Nornir с полями, нужными Netmiko (см. топик 14).

## Ссылки

- [json](https://docs.python.org/3/library/json.html)
- [PyYAML](https://pyyaml.org/)
