# Топик 9. Исключения

## Цели

- Понимать иерархию исключений Python и ловить конкретные типы.
- Использовать `try/except/else/finally` грамотно.
- Создавать собственные исключения; знать `raise ... from`.

---

## Теория

### Что такое исключение

Исключение — это объект, сигнализирующий об ошибке. Если его не поймать, программа завершится с трассировкой стека (traceback).

```
Traceback (most recent call last):
  File "script.py", line 5, in <module>
    x = int("hello")
ValueError: invalid literal for int() with base 10: 'hello'
```

Трассировка читается **снизу вверх**: нижняя строка — непосредственная причина.

### Иерархия встроенных исключений (часть)

```
BaseException
 ├── SystemExit          # sys.exit()
 ├── KeyboardInterrupt   # Ctrl+C
 └── Exception
      ├── ValueError      # неверное значение (int("abc"))
      ├── TypeError       # неверный тип (1 + "a")
      ├── KeyError        # нет ключа в словаре
      ├── IndexError      # нет индекса в списке
      ├── AttributeError  # нет атрибута/метода
      ├── NameError       # имя не определено
      ├── FileNotFoundError (подкласс OSError)
      ├── PermissionError  (подкласс OSError)
      ├── ConnectionError  (подкласс OSError)
      │    ├── ConnectionRefusedError
      │    └── ConnectionTimeoutError
      ├── TimeoutError
      ├── StopIteration
      └── RuntimeError
```

### try / except

```python
try:
    port = int(user_input)          # может выбросить ValueError
except ValueError:
    print("Нужно целое число")      # обработка ошибки
```

#### Несколько except

```python
try:
    data = read_device(host)
except FileNotFoundError as e:
    print(f"Файл не найден: {e}")
except ConnectionRefusedError as e:
    print(f"Подключение отклонено: {e}")
except (ValueError, KeyError) as e:    # несколько типов в кортеже
    print(f"Ошибка данных: {e}")
except Exception as e:                 # все остальные — широкий catch
    print(f"Неожиданная ошибка: {type(e).__name__}: {e}")
```

Ловите максимально **конкретный** тип — не `except Exception` для предсказуемых ошибок.

#### else и finally

```python
try:
    result = int(user_input)
except ValueError:
    print("Неверный формат")
else:
    # Выполняется ТОЛЬКО если исключения не было
    print(f"Успех: {result}")
finally:
    # Выполняется ВСЕГДА — и при ошибке, и без
    print("Готово")
```

Типичное применение `finally` — освобождение ресурсов. На практике лучше использовать `with`.

### raise — выброс исключения

```python
# Выброс нового исключения
def validate_port(port: int) -> None:
    if not 0 <= port <= 65535:
        raise ValueError(f"Некорректный порт: {port}")

# Повторный выброс пойманного
try:
    connect(host)
except ConnectionError as e:
    log.error(f"Failed to connect to {host}")
    raise   # пробрасываем исключение дальше

# Цепочка исключений — сохраняем контекст
try:
    data = load_json(path)
except json.JSONDecodeError as e:
    raise ValueError(f"Invalid inventory file: {path}") from e
```

`raise X from Y` позволяет видеть оба исключения в трассировке — полезно для диагностики.

### Собственные исключения

Создавайте свои исключения для доменных ошибок вашего проекта:

```python
class NetworkAutomationError(Exception):
    """Базовый класс для ошибок автоматизации."""
    pass

class DeviceConnectionError(NetworkAutomationError):
    """Не удалось подключиться к устройству."""
    def __init__(self, hostname: str, reason: str):
        self.hostname = hostname
        self.reason = reason
        super().__init__(f"Cannot connect to {hostname}: {reason}")

class InvalidInventoryError(NetworkAutomationError):
    """Некорректный инвентарь."""
    pass


# Использование
try:
    connect_to(device)
except DeviceConnectionError as e:
    print(f"Host {e.hostname} unreachable: {e.reason}")
```

### Практические паттерны

#### Безопасное преобразование

```python
def safe_int(s: str, default: int = 0) -> int:
    try:
        return int(s)
    except (ValueError, TypeError):
        return default

safe_int("255")   # 255
safe_int("abc")   # 0
safe_int(None)    # 0
```

#### Результат с ошибкой

```python
def try_connect(host: str) -> tuple[bool, str]:
    try:
        # ... логика подключения ...
        return True, ""
    except ConnectionRefusedError as e:
        return False, str(e)
    except TimeoutError as e:
        return False, f"Timeout: {e}"
```

#### Сбор ошибок по группе устройств (не прерывать весь прогон)

```python
results = []
errors = []
for device in inventory:
    try:
        data = collect(device)
        results.append(data)
    except Exception as e:
        errors.append({"device": device["hostname"], "error": str(e)})

print(f"OK: {len(results)}, Failed: {len(errors)}")
```

### Что НЕ делать

```python
# Голый except — ловит всё, включая KeyboardInterrupt и SystemExit
try:
    ...
except:     # не делайте так!
    pass

# Глотать исключение без лога
try:
    ...
except Exception:
    pass    # ошибка потеряна молча — очень плохо!

# Слишком широкий catch там, где можно быть точным
try:
    port = int(user_input)
except Exception:   # ValueError достаточно
    ...
```

---

## Примеры (сетевые)

```python
import json
from pathlib import Path


class InventoryError(Exception):
    pass


def load_inventory(path: str) -> list[dict]:
    """Загрузить инвентарь из JSON-файла."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise InventoryError(f"Inventory file not found: {path}")
    except PermissionError:
        raise InventoryError(f"Cannot read file (permissions): {path}")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise InventoryError(f"Invalid JSON in {path}: {e}") from e

    if not isinstance(data, list):
        raise InventoryError(f"Expected list, got {type(data).__name__}")

    return data


def parse_mtu(line: str) -> int | None:
    """Извлечь MTU из строки вида 'MTU 1500'. Вернуть None если не найдено."""
    parts = line.split()
    for i, part in enumerate(parts):
        if part.upper() == "MTU" and i + 1 < len(parts):
            try:
                return int(parts[i + 1])
            except ValueError:
                return None
    return None
```

---

## Практика

1. Оберните чтение файла: при `FileNotFoundError` выведите понятное сообщение и верните пустой список строк.
2. Напишите `safe_int(s: str, default: int = 0) -> int` — возвращает `default` при `ValueError` или `TypeError`.
3. Создайте класс исключения `InvalidIPError(ValueError)` и функцию `validate_ip(ip: str)`, выбрасывающую его для явно некорректных IP (например, октет > 255).
4. Напишите функцию `load_json_file(path: str) -> dict | list`, которая при ошибках парсинга бросает `ValueError` с понятным текстом через `raise ... from e`.
5. Реализуйте `collect_all(inventory: list) -> tuple[list, list]`, возвращающую `(results, errors)` — прогоняет «подключение» для каждого устройства, ошибки не прерывают прогон.
6. Напишите функцию `read_config_line(line: str) -> tuple[str, str]` для строки `"key = value"` — при отсутствии `=` бросайте `ValueError` с описательным сообщением.
7. Реализуйте контекстный менеджер **без** `with` (учебно): откройте файл, в `finally` закройте — затем перепишите то же через `with` и убедитесь, что поведение идентично.

---

## Частые ошибки

```python
# Голый except
try:
    ...
except:   # ловит KeyboardInterrupt — нельзя прервать Ctrl+C!
    pass

# Молчаливое подавление
except Exception:
    pass   # ошибка потеряна!

# except Exception вместо конкретного типа
except Exception:   # слишком широко
    log.error("something failed")

# Исправление:
except (ValueError, KeyError) as e:
    log.error("data error: %s", e)

# raise без аргументов в неправильном месте
def f():
    try:
        x = int("abc")
    except ValueError:
        raise   # OK — пробрасывает текущее исключение

def g():
    raise   # SyntaxError/RuntimeError — нет активного исключения!
```

---

## Самопроверка

- Никогда не используете `except: pass` без крайней необходимости.
- Ловите **конкретный** тип исключения, а не `Exception` для предсказуемых ошибок.
- Знаете разницу между `else` (успех) и `finally` (всегда).
- Умеете создать свой класс исключения.
- Понимаете `raise X from Y` для цепочки причин.
