# Топик 8. Работа с файлами

## Цели

- Открывать, читать и записывать текстовые и CSV файлы.
- Использовать `pathlib.Path` как современную замену `os.path`.
- Понимать контекстный менеджер `with` и почему он обязателен.

---

## Теория

### open() и режимы

```python
f = open("path/to/file.txt", mode="r", encoding="utf-8")
```

| Режим | Значение |
|-------|----------|
| `"r"` | Чтение (по умолчанию); файл должен существовать |
| `"w"` | Запись; создаёт файл или **перезаписывает** существующий |
| `"a"` | Дозапись в конец; создаёт если нет |
| `"x"` | Создать новый; ошибка если уже существует |
| `"r+"` | Чтение и запись |
| `"rb"` | Бинарное чтение (без кодировки) |

**Всегда** указывайте `encoding="utf-8"` при текстовых файлах на macOS.

### Контекстный менеджер with

```python
# Правильно — файл закрывается автоматически, даже при исключении
with open("data.txt", encoding="utf-8") as f:
    content = f.read()

# Неправильно — если возникнет исключение до close(), файл не закроется
f = open("data.txt")
content = f.read()
f.close()   # может не выполниться!
```

Конструкция `with ... as f:` гарантирует закрытие файла в любом случае — это **обязательный** стиль в Python.

### Чтение файлов

```python
with open("show_version.txt", encoding="utf-8") as f:
    # Способ 1: весь файл как одна строка
    content = f.read()

    # Способ 2: весь файл как список строк (с \n в конце)
    lines = f.readlines()

    # Способ 3: одна строка за раз
    line = f.readline()

    # Способ 4: итерация — самый эффективный для больших файлов
    for line in f:
        process(line.rstrip("\n"))  # убрать \n в конце
```

**Совет:** для разбора построчно используйте итерацию, а не `readlines()` — не грузит весь файл в память.

### Запись файлов

```python
with open("report.txt", "w", encoding="utf-8") as f:
    f.write("hostname,ip,status\n")    # write НЕ добавляет \n автоматически
    f.write(f"r1,10.0.0.1,up\n")

# Дозапись
with open("log.txt", "a", encoding="utf-8") as f:
    f.write(f"[2026-03-23] Connected to r1\n")

# print() в файл
with open("output.txt", "w", encoding="utf-8") as f:
    print("Line 1", file=f)       # добавляет \n автоматически
    print("Line 2", file=f)
```

### Чтение многострочного вывода

Типичная задача — разобрать вывод CLI, который лежит в файле:

```python
with open("labs/sample_outputs/show_ip_int_brief.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("Interface"):  # пропустить заголовок
            continue
        parts = line.split()
        iface, ip = parts[0], parts[1]
        print(f"{iface}: {ip}")
```

### Модуль csv

Встроенный модуль для CSV — надёжнее ручного `split(",")`:

```python
import csv

# Запись CSV
devices = [
    {"hostname": "r1",  "ip": "10.0.0.1", "status": "up"},
    {"hostname": "sw1", "ip": "10.0.0.2", "status": "down"},
]

with open("devices.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["hostname", "ip", "status"])
    writer.writeheader()
    writer.writerows(devices)

# Чтение CSV
with open("devices.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(dict(row))
```

### pathlib.Path — современный способ работы с путями

`pathlib` (Python 3.4+) заменяет `os.path` и делает работу с путями читаемой:

```python
from pathlib import Path

# Создание объекта пути
p = Path("labs/sample_outputs/show_version.txt")
p = Path.home() / "lab_project" / "data.txt"  # / — оператор для Path

# Информация о пути
p.name           # "data.txt"
p.stem           # "data"
p.suffix         # ".txt"
p.parent         # Path("labs/sample_outputs")
p.exists()       # True/False
p.is_file()      # True/False
p.is_dir()       # True/False

# Чтение и запись (удобные методы)
content = p.read_text(encoding="utf-8")   # весь файл
p.write_text("new content", encoding="utf-8")  # перезаписать

# Работа с директориями
output_dir = Path("artifacts")
output_dir.mkdir(exist_ok=True)    # создать если нет

# Перебор файлов
for f in Path("labs/sample_outputs").iterdir():
    if f.suffix == ".txt":
        print(f.name)

# Glob
for f in Path("labs").glob("**/*.txt"):  # рекурсивно
    print(f)
```

### Модуль os.path (для справки)

```python
import os

os.path.exists("file.txt")
os.path.join("labs", "data", "file.txt")   # "labs/data/file.txt"
os.path.dirname("/labs/data/file.txt")      # "/labs/data"
os.path.basename("/labs/data/file.txt")     # "file.txt"
os.makedirs("labs/output", exist_ok=True)
```

В новом коде предпочитайте `pathlib.Path` — он читаемее.

### Метка времени в имени файла

```python
from datetime import datetime
from pathlib import Path

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = Path("artifacts") / f"run_{timestamp}.log"
```

---

## Примеры (сетевые)

```python
import csv
from pathlib import Path
from datetime import datetime

def save_uptime_report(results: list[dict], output_dir: str = "artifacts") -> Path:
    """Сохранить результаты опроса в CSV."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"uptime_{timestamp}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["hostname", "ip", "uptime", "ok", "error"])
        writer.writeheader()
        writer.writerows(results)

    return output_file


def read_show_output(path: str) -> list[str]:
    """Прочитать вывод CLI из файла, вернуть непустые строки."""
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            clean = line.rstrip("\n")
            if clean.strip():
                lines.append(clean)
    return lines
```

---

## Практика

1. Прочитайте файл `labs/sample_outputs/sample_log.txt` построчно и выведите только строки с уровнем `ERROR`.
2. Скопируйте файл `sample_log.txt` в `artifacts/clean_log.txt`, пропустив строки-комментарии (начинающиеся с `#`).
3. Запишите список словарей устройств в CSV (`hostname, ip, role`) с помощью `csv.DictWriter`.
4. Используя `pathlib.Path`, найдите все `.txt` файлы в `labs/sample_outputs/` и выведите их имена и размеры в байтах.
5. Сохраните «вывод команды» (переменная `show_ver_output`) в файл `artifacts/show_version_r1.txt`, первой строкой поставив `# Generated: <timestamp>`.
6. Напишите функцию `read_inventory_csv(path: str) -> list[dict]`, читающую CSV файл и возвращающую список словарей.
7. Напишите функцию `append_log(message: str, log_file: str = "artifacts/script.log") -> None`, добавляющую строку с временной меткой в лог-файл (создать если нет).
8. **Pathlib-задача:** напишите функцию `latest_report(directory: str, suffix: str = ".csv") -> Path | None`, возвращающую путь к самому свежему файлу с заданным расширением (используйте `Path.stat().st_mtime`).

---

## Частые ошибки

```python
# Забыть указать кодировку
with open("file.txt") as f:        # может сломаться не на macOS
    ...
with open("file.txt", encoding="utf-8") as f:  # правильно

# write() не добавляет перевод строки
f.write("line1")
f.write("line2")   # запишет "line1line2"!
f.write("line1\n")
f.write("line2\n") # правильно

# Режим "w" перезаписывает файл без предупреждения
with open("important.txt", "w") as f:  # все данные потеряны!
    ...

# Чтение файла после закрытия контекста
with open("file.txt") as f:
    content = f.read()
# здесь f уже закрыт, но content — доступна
f.read()   # ValueError: I/O operation on closed file
```

---

## Самопроверка

- Всегда используете `with open(...)` вместо ручного `close()`.
- Указываете `encoding="utf-8"` при текстовых файлах.
- Знаете разницу между `"w"` и `"a"`.
- Умеете использовать `csv.DictWriter` и `csv.DictReader`.
- Используете `Path` для построения путей вместо конкатенации строк.
