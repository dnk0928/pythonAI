# Топик B6. `pytest` для сетевых скриптов

## Цели

- Покрыть функции парсинга и нормализации тестами, чтобы изменения не ломали существующую логику.
- Использовать фикстуры и параметризацию для сетевых тестовых данных.

## Теория (тезисы)

- **`pytest`** — де-факто стандарт тестирования Python; функции-тесты именуются `test_*`, автообнаружение.
- **Фикстура (`@pytest.fixture`)** — переиспользуемый контекст: загрузить файл, создать объект, подменить соединение.
- **`@pytest.mark.parametrize`** — один тест с разными входными данными (множество MAC-строк, IP и т.д.).
- **`monkeypatch`** — встроенная фикстура; подменяет функции без реальных устройств.
- **Scope:** `function` (по умолчанию), `module`, `session` — для дорогих фикстур (загрузка файла один раз).

## Пример

```python
# tests/test_parsers.py
import pytest
from pathlib import Path
from parse import normalize_mac, extract_uptime

# --- фикстура ---
@pytest.fixture(scope="module")
def show_version_text():
    return Path("labs/sample_outputs/show_version_ios.txt").read_text(encoding="utf-8")

# --- базовый тест ---
def test_extract_uptime_found(show_version_text):
    result = extract_uptime(show_version_text)
    assert "weeks" in result or "days" in result

def test_extract_uptime_missing():
    assert extract_uptime("no uptime here") is None

# --- параметризация ---
@pytest.mark.parametrize("raw,expected", [
    ("aaaa.bbbb.cccc", "aa:aa:bb:bb:cc:cc"),
    ("AA:BB:CC:DD:EE:FF", "aa:bb:cc:dd:ee:ff"),
    ("aabb-ccdd-eeff", "aa:bb:cc:dd:ee:ff"),
])
def test_normalize_mac(raw, expected):
    assert normalize_mac(raw) == expected
```

## Шаблон `parse.py` для тестов

```python
import re

def normalize_mac(mac: str) -> str:
    digits = re.sub(r"[^0-9a-fA-F]", "", mac)
    if len(digits) != 12:
        raise ValueError(f"Неверный MAC: {mac!r}")
    return ":".join(digits[i:i+2] for i in range(0, 12, 2)).lower()

def extract_uptime(text: str) -> str | None:
    m = re.search(r"uptime is (.+)", text)
    return m.group(1).strip() if m else None
```

## Практика

1. Напишите `tests/test_ipaddress_utils.py` с параметризованными тестами для функции `is_rfc1918` из топика 10a — минимум 5 случаев (частные и публичные IP).
2. Протестируйте функцию из топика 7 (`normalize_interface_name`) через `@pytest.mark.parametrize` с 4–5 сокращёнными именами.
3. Напишите фикстуру `sample_mac_table`, читающую `labs/sample_outputs/show_mac_address_table.txt`, и тест, проверяющий, что парсер возвращает ровно 4 записи (по числу строк в файле).
4. Добавьте `pytest` в pre-commit hook или запускайте `pytest -v` перед каждым `git push` — проверьте, что все тесты проходят.

## Запуск

```bash
pytest -v                        # все тесты с подробным выводом
pytest tests/test_parsers.py -v  # конкретный файл
pytest -k "mac"                  # тесты с "mac" в имени
pytest --tb=short                # короткий traceback при ошибке
```

## Самопроверка

- 100% coverage не цель — покрывайте **критичные** пути: парсинг, нормализацию, загрузку инвентаря.
- Тест, который всегда проходит без изменений в коде, — бесполезный тест.

## Ссылки

- [pytest](https://docs.pytest.org/)
- [pytest parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html)
