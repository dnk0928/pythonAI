# Топик 7. Функции

## Цели

- Объявлять функции с позиционными, именованными аргументами и значениями по умолчанию.
- Понимать `*args`, `**kwargs` и аннотации типов.
- Знать области видимости, lambda и базовые паттерны проектирования функций.

---

## Теория

### Объявление функции

```python
def function_name(param1, param2):
    """Docstring: кратко о том, что делает функция."""
    result = param1 + param2
    return result
```

- `return` завершает функцию и возвращает значение.
- Без `return` (или с голым `return`) функция возвращает `None`.
- **Docstring** — строковый литерал сразу после `def`; доступен через `help()` и IDE.

### Аргументы

#### Позиционные и именованные

```python
def connect(host, port, timeout):
    ...

connect("r1", 22, 30)              # позиционные
connect("r1", timeout=30, port=22) # именованные (порядок не важен)
connect(host="r1", port=22, timeout=30)
```

#### Значения по умолчанию

```python
def connect(host, port=22, timeout=30, username="admin"):
    ...

connect("r1")                 # port=22, timeout=30, username="admin"
connect("r1", port=830)       # только port переопределён
```

**Антипаттерн:** изменяемые значения по умолчанию — создаются **один раз** при определении функции:

```python
# НЕПРАВИЛЬНО — список разделяется между всеми вызовами!
def add_device(device, inventory=[]):
    inventory.append(device)
    return inventory

add_device("r1")  # ["r1"]
add_device("sw1") # ["r1", "sw1"] — не ["sw1"]!

# ПРАВИЛЬНО:
def add_device(device, inventory=None):
    if inventory is None:
        inventory = []
    inventory.append(device)
    return inventory
```

#### *args — переменное число позиционных аргументов

```python
def send_commands(*commands):
    """commands — кортеж строк"""
    for cmd in commands:
        print(f"Sending: {cmd}")

send_commands("show version", "show ip int brief", "show clock")
```

#### **kwargs — переменное число именованных аргументов

```python
def build_device(**kwargs):
    """kwargs — словарь"""
    return kwargs

d = build_device(hostname="r1", ip="10.0.0.1", role="router")
# {"hostname": "r1", "ip": "10.0.0.1", "role": "router"}
```

#### Комбинирование аргументов

```python
def run(host, *commands, timeout=30, **extra):
    print(f"host={host}, cmds={commands}, timeout={timeout}, extra={extra}")

run("r1", "show ver", "show clock", timeout=60, username="admin")
```

#### Только именованные / только позиционные

```python
# * — всё после него только именованное
def connect(host, port, *, timeout=30, verbose=False):
    ...
connect("r1", 22, verbose=True)   # OK
connect("r1", 22, True)           # TypeError!

# / — всё до него только позиционное
def ping(host, count, /):
    ...
ping("8.8.8.8", 4)                # OK
ping(host="8.8.8.8", count=4)     # TypeError!
```

### Аннотации типов

Аннотации не обязательны для интерпретатора, но помогают IDE и читателю:

```python
def get_uptime(hostname: str, timeout: int = 30) -> str | None:
    ...

def normalize_mac(mac: str) -> str:
    ...

def load_inventory(path: str) -> list[dict]:
    ...
```

### Области видимости (LEGB)

Python ищет имена в порядке: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in.

```python
TIMEOUT = 30            # global

def connect(host):
    timeout = TIMEOUT   # читает global — OK
    timeout = 60        # создаёт local-переменную, global не меняется

def wrong():
    print(x)            # UnboundLocalError — Python видит x ниже
    x = 10

# global — изменить глобальную переменную (используйте редко!)
counter = 0
def increment():
    global counter
    counter += 1
```

Предпочитайте **передавать** данные через аргументы и возвращать через `return`, а не через `global`.

### Lambda — анонимные функции

Однострочная функция, удобна как аргумент (например, `key=` для `sorted`):

```python
double = lambda x: x * 2
double(5)  # 10

# Сортировка по ключу
devices = [{"hostname": "sw1", "ip": "10.0.0.2"}, {"hostname": "r1", "ip": "10.0.0.1"}]
sorted_devices = sorted(devices, key=lambda d: d["hostname"])

# Сортировка по последнему октету IP
sorted_by_ip = sorted(ip_list, key=lambda ip: int(ip.split(".")[-1]))
```

### Вложенные функции и closure

```python
def make_prefix_filter(prefix):
    """Фабрика фильтров — возвращает функцию."""
    def filter_fn(ip):
        return ip.startswith(prefix)
    return filter_fn

is_rfc1918_10 = make_prefix_filter("10.")
list(filter(is_rfc1918_10, ["10.0.0.1", "192.168.1.1", "10.1.1.1"]))
# ["10.0.0.1", "10.1.1.1"]
```

### Возврат нескольких значений

Технически — кортеж:

```python
def parse_cidr(cidr: str) -> tuple[str, int]:
    network, prefix = cidr.split("/")
    return network, int(prefix)

net, mask = parse_cidr("10.0.0.0/24")
# net = "10.0.0.0", mask = 24
```

---

## Примеры (сетевые)

```python
# Обёртка над Netmiko с разумными значениями по умолчанию
def run_show_command(
    host: str,
    command: str,
    username: str = "admin",
    timeout: int = 30,
    **device_kwargs,
) -> str:
    """Подключиться и выполнить show-команду, вернуть вывод."""
    # ... здесь будет Netmiko (топик 12)
    return output

# Нормализация названия интерфейса
IFACE_MAP = {
    "Gi": "GigabitEthernet",
    "Te": "TenGigabitEthernet",
    "Hu": "HundredGigE",
    "Lo": "Loopback",
    "Vl": "Vlan",
    "Mg": "Management",
}

def normalize_interface(name: str) -> str:
    name = name.strip()
    for short, full in IFACE_MAP.items():
        if name.startswith(short):
            return full + name[len(short):]
    return name  # вернуть как есть если неизвестный тип

# Сортировка инвентаря
inventory = [...]
# По hostname:
sorted(inventory, key=lambda d: d["hostname"])
# По IP (по последнему октету):
sorted(inventory, key=lambda d: int(d["ip"].split(".")[-1]))
```

---

## Практика

1. Напишите функцию `clamp(value: float, low: float, high: float) -> float`, ограничивающую значение диапазоном `[low, high]`.
2. Реализуйте `build_device(hostname: str, ip: str, **extra) -> dict`, возвращающую словарь с обязательными полями и всем из `extra`.
3. Напишите `normalize_interface(name: str) -> str` по таблице из примера выше — используйте значение из `IFACE_MAP` или возвращайте исходное.
4. Напишите `parse_cidr(cidr: str) -> tuple[str, int]` — разобрать `"10.0.0.0/24"` в `("10.0.0.0", 24)`.
5. Реализуйте функцию `filter_by_role(devices: list, *roles: str) -> list` — возвращает устройства, роль которых есть в `roles`.
6. Напишите `make_ssh_params(host: str, username: str = "admin", port: int = 22, **kwargs) -> dict` — формирует словарь для Netmiko/Paramiko.
7. Используя `sorted` с `key=lambda`, отсортируйте список IP-адресов `["10.0.0.5", "10.0.0.1", "10.0.0.20"]` **численно** по последнему октету.
8. **Codewars-стиль:** напишите функцию `deduplicate(lst: list) -> list`, удаляющую дубликаты **с сохранением порядка** первого вхождения (без использования `set` напрямую для итоговой коллекции).

---

## Частые ошибки

```python
# Изменяемое значение по умолчанию
def f(x, result=[]):
    result.append(x)
    return result
f(1)  # [1]
f(2)  # [1, 2] — не [2]!

# Забыть return
def double(x):
    x * 2            # вычислено, но не возвращено!
double(5)            # None

# Вызов без скобок
sorted_list = sorted(my_list)    # правильно
sorted_list = sorted             # это сама функция, не результат!

# Изменение глобального без global
counter = 0
def inc():
    counter += 1    # UnboundLocalError!
```

---

## Самопроверка

- Знаете, почему изменяемые значения по умолчанию — антипаттерн.
- Понимаете разницу между `*args` (кортеж) и `**kwargs` (словарь).
- Умеете использовать `sorted(lst, key=...)` с lambda.
- Знаете порядок LEGB и почему `global` нужен редко.
