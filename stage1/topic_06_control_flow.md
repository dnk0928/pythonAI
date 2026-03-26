# Топик 6. Ветвления и циклы

## Цели

- Уверенно использовать `if/elif/else`, тернарный оператор, `match/case`.
- Писать `for` и `while` с `break`, `continue`, `else`.
- Знать `enumerate`, `zip`, `range` и когда применять каждый.

---

## Теория

### Условные конструкции

#### if / elif / else

```python
status = "up"

if status == "up":
    print("Interface is operational")
elif status == "down":
    print("Interface is down")
elif status == "administratively down":
    print("Interface is shutdown")
else:
    print(f"Unknown status: {status!r}")
```

Условие может быть любым truthy/falsy выражением:

```python
interfaces = []
if not interfaces:          # пустой список — falsy
    print("No interfaces!")

hostname = None
if hostname is None:        # явная проверка на None
    hostname = "unknown"
```

#### Тернарный оператор

```python
# value_if_true if condition else value_if_false
status = "up"
label = "UP" if status == "up" else "DOWN"

# В f-строке
print(f"Status: {'UP' if status == 'up' else 'DOWN'}")

# НЕ злоупотребляйте — если условие сложное, лучше обычный if
```

#### match / case (Python 3.10+)

```python
command = "show version"
match command.split()[0]:
    case "show":
        print("Read-only command")
    case "configure" | "conf":
        print("Configuration command")
    case _:
        print("Unknown command")
```

### Цикл for

Цикл `for` перебирает любой **итерируемый** объект (список, строку, словарь, файл, …).

```python
# Базовый обход
for iface in ["Gi0/1", "Gi0/2", "Te1/1"]:
    print(iface)

# range — числовой диапазон
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):       # 1, 2, 3, 4, 5
    pass

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8
    pass

for i in range(10, 0, -1):  # 10, 9, 8, ..., 1
    pass
```

#### enumerate — индекс + значение

```python
devices = ["r1", "sw1", "sw2"]
for i, device in enumerate(devices):
    print(f"{i}: {device}")
# 0: r1
# 1: sw1
# 2: sw2

for i, device in enumerate(devices, start=1):  # нумерация с 1
    print(f"{i}. {device}")
```

#### zip — параллельный обход

```python
hosts = ["r1", "sw1", "sw2"]
ips   = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

for host, ip in zip(hosts, ips):
    print(f"{host}: {ip}")

# Создание словаря из двух списков
device_map = dict(zip(hosts, ips))
# {"r1": "10.0.0.1", "sw1": "10.0.0.2", "sw2": "10.0.0.3"}
```

#### Обход словаря

```python
device = {"hostname": "r1", "ip": "10.0.0.1", "role": "router"}

for key in device:               # только ключи
for key in device.keys():        # то же явно
for val in device.values():      # только значения
for key, val in device.items():  # пары — чаще всего нужно это
    print(f"{key}: {val}")
```

#### break и continue

```python
# break — выйти из цикла немедленно
for line in log_lines:
    if "ERROR" in line:
        print(f"Found error: {line}")
        break   # дальше не смотрим

# continue — перейти к следующей итерации
for line in log_lines:
    if line.startswith("#") or not line.strip():
        continue    # пропустить пустые и комментарии
    process(line)   # остальные строки обрабатываем
```

#### for ... else

`else`-блок выполняется, если цикл завершился **без** `break`:

```python
target_host = "r1"
for device in inventory:
    if device["hostname"] == target_host:
        print(f"Found: {device['ip']}")
        break
else:
    print(f"{target_host} not found in inventory")
```

### Цикл while

Выполняется, пока условие истинно. Используйте там, где количество итераций заранее неизвестно.

```python
retries = 3
while retries > 0:
    success = try_connect(host)
    if success:
        break
    retries -= 1
    print(f"Retry... {retries} left")
else:
    print("Connection failed after all retries")

# Бесконечный цикл с break
while True:
    line = read_next_line()
    if not line:
        break
    process(line)
```

### Вложенные циклы и ранний выход

```python
# Ранний return из функции — вместо глубокой вложенности
def find_device(inventory, hostname):
    for device in inventory:
        if device["hostname"] == hostname:
            return device    # ранний выход
    return None              # не нашли

# any() и all() — чтобы не писать цикл вручную
up_ifaces = ["Gi0/1", "Gi0/2"]
if any(i.startswith("Te") for i in up_ifaces):
    print("Has TenGig")

if all(i.startswith("Gi") for i in up_ifaces):
    print("All Gigabit")
```

---

## Примеры (сетевые)

```python
# Разбор вывода show ip int brief
raw_output = """
Interface              IP-Address      OK? Method Status    Protocol
GigabitEthernet0/0     10.0.0.1        YES manual up        up
GigabitEthernet0/1     unassigned      YES unset  down      down
Loopback0              1.1.1.1         YES manual up        up
"""

up_interfaces = []
for line in raw_output.strip().splitlines():
    if not line or line.startswith("Interface"):
        continue
    parts = line.split()
    if len(parts) >= 6 and parts[4] == "up":
        up_interfaces.append({"name": parts[0], "ip": parts[1]})

print(f"UP interfaces: {len(up_interfaces)}")
for iface in up_interfaces:
    print(f"  {iface['name']:<30} {iface['ip']}")

# Генерация команд конфигурации
vlans = [(10, "USERS"), (20, "SERVERS"), (30, "MGMT")]
for vlan_id, vlan_name in vlans:
    print(f"vlan {vlan_id}")
    print(f" name {vlan_name}")
print("!")
```

---

## Практика

1. Разберите список строк лога: пропустите пустые и строки-комментарии (`#`), остальные соберите в список `clean_lines`.
2. Используя `enumerate`, выведите нумерованный список устройств из инвентаря (нумерация с 1).
3. Используя `zip`, создайте словарь `{hostname: ip}` из двух отдельных списков `hostnames` и `ips`.
4. Напишите функцию `find_device(inventory: list, hostname: str) -> dict | None`, возвращающую запись устройства или `None` (используйте `for ... else`).
5. Реализуйте `retry_connect(host: str, attempts: int = 3) -> bool` через `while`: имитируйте случайный успех (используйте `random.random() > 0.5`), логируйте попытки.
6. Из вывода `show ip int brief` (файл `labs/sample_outputs/show_ip_int_brief.txt`) выведите только строки со статусом `up` — используйте `continue` для пропуска остальных.
7. Напишите функцию `ip_range(start: str, count: int) -> list[str]`, генерирующую список IP-адресов начиная с `start` (только последний октет, без проверки переполнения): `ip_range("10.0.0.1", 5)` → `["10.0.0.1", ..., "10.0.0.5"]`.
8. **Сложнее:** реализуйте `flatten(nested: list) -> list`, разворачивающую список любой глубины вложенности в плоский список (через `isinstance` и рекурсию или `while` с очередью).

---

## Частые ошибки

```python
# Изменение списка во время итерации
for item in my_list:
    my_list.remove(item)  # пропускает элементы!

# Правильно — итерироваться по копии:
for item in my_list[:]:
    my_list.remove(item)

# Бесконечный цикл без выхода
while True:
    data = get_data()
    # забыли break или условие выхода!

# range не включает конечное значение
for i in range(5):    # 0, 1, 2, 3, 4 — без 5!
for i in range(1, 6): # 1, 2, 3, 4, 5

# Неправильное использование else у цикла
for x in []:       # пустой список
    pass
else:
    print("else выполнится!")  # да, выполнится — break не было
```

---

## Самопроверка

- Умеете объяснить, когда `break` vs `continue`.
- Знаете, что делает `for ... else`.
- Используете `enumerate` вместо `range(len(...))`.
- Используете `zip` для параллельного обхода вместо индексации.
