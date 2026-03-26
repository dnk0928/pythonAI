# Топик 10. Модули и пакеты

## Цели

- Разделять код по файлам с правильной структурой импортов.
- Понимать `if __name__ == "__main__"` и когда это нужно.
- Знать стандартную библиотеку Python достаточно, чтобы не изобретать велосипед.

---

## Теория

### Модуль

**Модуль** — любой файл `.py`. Имя модуля = имя файла без расширения.

```python
# netutils.py — это модуль с именем "netutils"
def normalize_interface(name: str) -> str:
    ...

DEFAULT_TIMEOUT = 30
```

### Импорт

```python
# Импорт всего модуля — доступ через имя модуля
import netutils
netutils.normalize_interface("Gi0/1")
netutils.DEFAULT_TIMEOUT

# Импорт конкретных имён
from netutils import normalize_interface, DEFAULT_TIMEOUT
normalize_interface("Gi0/1")   # без prefix

# Псевдоним
import netutils as nu
nu.normalize_interface("Gi0/1")

from netutils import normalize_interface as norm
norm("Gi0/1")
```

**Избегайте** `from module import *` — засоряет пространство имён и делает код непредсказуемым.

### Порядок импортов (PEP 8)

```python
# 1. Стандартная библиотека
import json
import csv
from pathlib import Path
from datetime import datetime

# 2. Сторонние пакеты (через pip)
import netmiko
import jinja2

# 3. Локальные модули проекта
from netutils import normalize_interface
from inventory import load_devices
```

### Пакет

**Пакет** — каталог с файлом `__init__.py`:

```
my_project/
├── __init__.py          # делает каталог пакетом
├── collector.py
├── parser.py
└── report.py
```

```python
from my_project.collector import collect_uptime
from my_project import parser
```

`__init__.py` может быть пустым или содержать экспортируемые имена пакета.

### if __name__ == "__main__"

Python устанавливает `__name__` в:
- `"__main__"` — если файл запущен напрямую (`python3 script.py`).
- Имя модуля — если файл импортирован (`import script`).

```python
# utils.py
def normalize_interface(name: str) -> str:
    ...

if __name__ == "__main__":
    # Этот блок выполняется ТОЛЬКО при python3 utils.py
    # НЕ выполняется при import utils
    print(normalize_interface("Gi0/1"))
```

Это позволяет одновременно использовать файл как модуль (для импорта) и как скрипт (для запуска).

### python3 -m

```bash
python3 -m module_name        # запуск модуля из пакета
python3 -m json.tool          # форматировать JSON (stdlib)
python3 -m http.server 8080   # простой HTTP-сервер
python3 -m pip install netmiko
```

### Обзор стандартной библиотеки (важное для сетевика)

| Модуль | Зачем |
|--------|-------|
| `json` | Чтение/запись JSON (инвентарь, API) |
| `csv` | Работа с CSV-файлами |
| `pathlib` | Удобная работа с путями |
| `os` / `sys` | Переменные окружения, аргументы командной строки |
| `re` | Регулярные выражения (топик 19) |
| `datetime` | Временные метки |
| `logging` | Структурированные логи (топик 10b) |
| `ipaddress` | Работа с IP и подсетями (топик 10a) |
| `collections` | `Counter`, `defaultdict`, `namedtuple` |
| `itertools` | `chain`, `groupby`, `product` — для сложных итераций |
| `functools` | `partial`, `lru_cache` |
| `argparse` | Аргументы командной строки |
| `subprocess` | Запуск внешних команд |
| `socket` | Низкоуровневые сетевые операции |
| `hashlib` | Хэши (md5, sha256) |
| `copy` | Копирование объектов |
| `pprint` | Красивая печать вложенных структур |

### Полезные модули: примеры

#### collections.defaultdict

```python
from collections import defaultdict

# Группировка без setdefault()
by_role = defaultdict(list)
for device in inventory:
    by_role[device["role"]].append(device["hostname"])
# defaultdict автоматически создаёт [] для нового ключа
```

#### collections.Counter

```python
from collections import Counter

roles = [d["role"] for d in inventory]
count = Counter(roles)
# Counter({"switch": 5, "router": 2, "firewall": 1})
count.most_common(2)
# [("switch", 5), ("router", 2)]
```

#### argparse — CLI аргументы

```python
import argparse

parser = argparse.ArgumentParser(description="Network inventory tool")
parser.add_argument("--inventory", default="labs/inventory.json", help="Path to inventory")
parser.add_argument("--output", default="artifacts/", help="Output directory")
parser.add_argument("--verbose", action="store_true")

args = parser.parse_args()
print(args.inventory)   # значение аргумента
```

#### os.environ — переменные окружения (для секретов!)

```python
import os

username = os.environ.get("LAB_SSH_USER", "admin")
password = os.environ["LAB_SSH_PASS"]   # KeyError если не задана
```

#### pprint — отладка вложенных структур

```python
from pprint import pprint

data = {"interfaces": [{"name": "Gi0/1", "ip": "10.0.0.1"}, ...]}
pprint(data)     # читаемый многострочный вывод
pprint(data, width=60, depth=2)  # ограничить глубину
```

### Структура небольшого проекта

```
lab_project/
├── .venv/
├── .gitignore
├── requirements.txt
├── README.md
├── main.py              # точка входа: парсинг args, вызов модулей
├── config.py            # константы: DEFAULT_TIMEOUT, IFACE_MAP
├── inventory.py         # load_inventory(), validate()
├── collector.py         # collect_data() — Netmiko/NAPALM
├── parser.py            # parse_show_output() — TextFSM/regex
├── report.py            # generate_report() — Jinja2/CSV
└── labs/
    └── sample_outputs/
```

---

## Примеры

```python
# config.py
DEFAULT_TIMEOUT = 30
DEFAULT_USERNAME = "admin"
IFACE_MAP = {
    "Gi": "GigabitEthernet",
    "Te": "TenGigabitEthernet",
    "Lo": "Loopback",
}
```

```python
# inventory.py
import json
from pathlib import Path


def load_inventory(path: str = "labs/inventory.json") -> list[dict]:
    """Загрузить список устройств из JSON."""
    text = Path(path).read_text(encoding="utf-8")
    return json.loads(text)


if __name__ == "__main__":
    from pprint import pprint
    pprint(load_inventory())
```

```python
# main.py
import argparse
from inventory import load_inventory
from config import DEFAULT_TIMEOUT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default="labs/inventory.json")
    args = parser.parse_args()

    devices = load_inventory(args.inventory)
    print(f"Loaded {len(devices)} devices, timeout={DEFAULT_TIMEOUT}s")


if __name__ == "__main__":
    main()
```

---

## Практика

1. Создайте структуру проекта: `config.py` с константами `DEFAULT_TIMEOUT = 30` и `DEFAULT_PORT = 22`; `inventory.py` с функцией `load_inventory(path)` — импортируйте константы из `config.py`.
2. Добавьте `if __name__ == "__main__"` в `inventory.py` для тестового вывода инвентаря; убедитесь, что при `import inventory` блок не выполняется.
3. Создайте `main.py` с `argparse`: аргументы `--inventory` (путь к файлу) и `--verbose` (флаг).
4. Используйте `collections.Counter` для подсчёта устройств по `device_type` из `labs/inventory.json`.
5. Используйте `os.environ.get("LAB_SSH_USER", "admin")` в `config.py` для получения логина из окружения.
6. Напишите `pprint` вывод для вложенного словаря с данными об интерфейсах — убедитесь, что он читаемее чем `print`.
7. Перенесите функцию `normalize_interface` из топика 7 в `netutils.py`, напишите к ней `if __name__ == "__main__"` с тестовыми вызовами.
8. **Итог:** соберите все написанные функции в структуру проекта: `config.py`, `inventory.py`, `netutils.py`, `main.py` — запустите `python3 main.py --inventory labs/inventory.json`.

---

## Частые ошибки

```python
# from module import * — плохо
from netutils import *     # что именно импортировано? Неясно!
from netutils import normalize_interface  # явно и понятно

# Циклический импорт
# a.py: from b import something
# b.py: from a import something_else
# → ImportError! Решение: вынести общее в c.py

# Код на уровне модуля без if __name__
# utils.py:
connect_to_device()   # выполнится при любом import utils!

# Правильно:
if __name__ == "__main__":
    connect_to_device()

# Имя модуля совпадает со стандартной библиотекой
# Файл json.py в проекте «затенит» встроенный json!
```

---

## Самопроверка

- Понимаете разницу между `import module` и `from module import name`.
- Знаете, что делает `if __name__ == "__main__"`.
- Умеете использовать `argparse` для простого CLI-интерфейса.
- Знаете хотя бы 5-7 полезных модулей стандартной библиотеки по назначению.
- Организуете проект по модулям, а не пишете всё в один файл.
