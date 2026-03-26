# Топик 4. Списки и словари

## Цели

- Уверенно работать со списком как с основной коллекцией для массивов данных.
- Использовать словарь для структурированного хранения данных «устройство → данные».
- Знать list/dict comprehension и полезные встроенные функции.

---

## Теория

### Список (list)

Список — **упорядоченная изменяемая** коллекция. Элементы могут быть любого типа, включая другие списки.

```python
# Создание
empty = []
ports = [22, 80, 443]
ifaces = ["Gi0/1", "Gi0/2", "Te1/1"]
mixed = [1, "hello", True, None]   # возможно, но редко полезно

# Доступ и срезы — как у строк
ifaces[0]      # "Gi0/1"
ifaces[-1]     # "Te1/1"
ifaces[1:]     # ["Gi0/2", "Te1/1"]
```

#### Основные методы списка

```python
lst = [3, 1, 4, 1, 5]

# Добавление
lst.append(9)           # [3, 1, 4, 1, 5, 9] — один элемент в конец
lst.extend([2, 6])      # [3, 1, 4, 1, 5, 9, 2, 6] — несколько
lst.insert(0, 99)       # вставить 99 на позицию 0

# Удаление
lst.pop()               # удалить и вернуть последний
lst.pop(0)              # удалить и вернуть по индексу
lst.remove(1)           # удалить первое вхождение значения
del lst[2]              # удалить по индексу

# Поиск
lst.index(4)            # индекс первого вхождения (ValueError если нет)
lst.count(1)            # сколько раз встречается
4 in lst                # True/False

# Сортировка
lst.sort()              # сортировка на месте (in-place), изменяет lst
lst.sort(reverse=True)  # по убыванию
sorted(lst)             # новый отсортированный список, lst не меняется
lst.reverse()           # развернуть на месте

# Прочее
len(lst)                # длина
lst.copy()              # поверхностная копия
lst.clear()             # очистить
```

#### enumerate и zip

```python
# enumerate — индекс + значение
for i, iface in enumerate(["Gi0/1", "Gi0/2"], start=1):
    print(f"{i}. {iface}")
# 1. Gi0/1
# 2. Gi0/2

# zip — параллельный обход нескольких списков
hosts = ["r1", "sw1", "sw2"]
ips   = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
for host, ip in zip(hosts, ips):
    print(f"{host}: {ip}")
```

#### List comprehension

Краткая запись для создания нового списка:

```python
# Без comprehension
ups = []
for iface in interfaces:
    if iface["status"] == "up":
        ups.append(iface["name"])

# С comprehension
ups = [iface["name"] for iface in interfaces if iface["status"] == "up"]

# Примеры
squares = [x**2 for x in range(10)]
upper_ifaces = [s.upper() for s in ["gi0/1", "gi0/2"]]
only_valid = [ip for ip in ip_list if ip.startswith("10.")]
```

### Словарь (dict)

Словарь — **неупорядоченное** (в Python 3.7+ порядок вставки сохраняется) отображение **ключ → значение**. Ключи хешируемые (обычно строки, числа, кортежи).

```python
# Создание
device = {
    "hostname": "r1",
    "ip": "10.0.0.1",
    "role": "router",
    "interfaces": ["Gi0/0", "Gi0/1"],
}

# Доступ
device["hostname"]          # "r1"
device.get("vendor")        # None — безопасно (нет KeyError)
device.get("vendor", "N/A") # "N/A" — значение по умолчанию

# Изменение
device["ip"] = "10.0.0.2"  # изменить или добавить
device.setdefault("site", "HQ")  # добавить только если нет

# Удаление
del device["role"]
device.pop("role")          # удалить и вернуть значение
device.pop("role", None)    # удалить или вернуть None (без KeyError)

# Итерация
for key in device:                      # только ключи
for key in device.keys():              # то же
for val in device.values():            # только значения
for key, val in device.items():        # пары ключ-значение

# Проверка наличия ключа
"hostname" in device        # True
"vendor" not in device      # True

# Слияние (Python 3.9+)
merged = device | {"site": "DC1"}   # новый словарь
device |= {"site": "DC1"}           # обновить на месте

# Для старых версий
device.update({"site": "DC1"})
```

#### Dict comprehension

```python
# Инвертировать словарь
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}

# Список устройств → словарь hostname → device
devices = [{"hostname": "r1", "ip": "10.0.0.1"}, {"hostname": "sw1", "ip": "10.0.0.2"}]
by_host = {d["hostname"]: d for d in devices}
# {"r1": {"hostname": "r1", "ip": "10.0.0.1"}, ...}
```

### Вложенные структуры

Типичный результат парсинга CLI или API — список словарей:

```python
interfaces = [
    {"name": "Gi0/0", "ip": "10.0.0.1", "status": "up",   "speed": 1000},
    {"name": "Gi0/1", "ip": "unassigned", "status": "down", "speed": 1000},
    {"name": "Te1/0", "ip": "10.1.1.1",  "status": "up",   "speed": 10000},
]

# Получить имена всех up-интерфейсов
up_ifaces = [i["name"] for i in interfaces if i["status"] == "up"]

# Словарь name → ip для up
ip_map = {i["name"]: i["ip"] for i in interfaces if i["status"] == "up"}
```

### Полезные встроенные функции

```python
lst = [3, 1, 4, 1, 5, 9]

len(lst)       # 6
sum(lst)       # 23
min(lst)       # 1
max(lst)       # 9
sorted(lst)    # [1, 1, 3, 4, 5, 9]
list(set(lst)) # [1, 3, 4, 5, 9] — убрать дубликаты (порядок не гарантирован)

any(x > 8 for x in lst)    # True  — есть ли хоть одно
all(x > 0 for x in lst)    # True  — все ли
```

### Копирование — поверхностное и глубокое

```python
import copy

a = [1, 2, [3, 4]]
b = a             # b и a — один объект!
b = a.copy()      # поверхностная копия — вложенные объекты общие
b = copy.deepcopy(a)  # глубокая копия — всё независимо

d = {"x": [1, 2]}
d2 = d.copy()          # поверхностная — d["x"] и d2["x"] — одно и то же
d2 = copy.deepcopy(d)  # глубокая
```

---

## Примеры (сетевые)

```python
# Инвентарь устройств
inventory = [
    {"hostname": "r1",  "ip": "10.0.0.1", "role": "router"},
    {"hostname": "sw1", "ip": "10.0.0.2", "role": "switch"},
    {"hostname": "sw2", "ip": "10.0.0.3", "role": "switch"},
]

# Только коммутаторы
switches = [d for d in inventory if d["role"] == "switch"]

# Быстрый поиск по hostname
by_host = {d["hostname"]: d for d in inventory}
print(by_host["sw1"]["ip"])  # "10.0.0.2"

# Подсчёт устройств по роли
from collections import Counter
role_count = Counter(d["role"] for d in inventory)
# Counter({'switch': 2, 'router': 1})

# Группировка по роли вручную
by_role = {}
for d in inventory:
    by_role.setdefault(d["role"], []).append(d["hostname"])
# {"router": ["r1"], "switch": ["sw1", "sw2"]}
```

---

## Практика

1. Из списка словарей `inventory` (выше) создайте новый список, содержащий только имена (`hostname`) коммутаторов.
2. Подсчитайте количество интерфейсов по типу (первые 2 символа: `Gi`, `Te`, `Lo`) из списка строк `["Gi0/1", "Gi0/2", "Te1/1", "Lo0"]` — результат должен быть словарём.
3. Напишите функцию `merge_facts(base: dict, updates: dict) -> dict`, возвращающую новый словарь, где значения из `updates` перезаписывают `base`.
4. Из списка `interfaces` (выше) создайте словарь `{name: speed}` только для up-интерфейсов через dict comprehension.
5. Напишите функцию `unique_sorted(lst: list) -> list`, удаляющую дубликаты и возвращающую отсортированный список.
6. Реализуйте `group_by_role(devices: list) -> dict`, группирующую устройства в словарь `{role: [hostname, ...]}`.
7. Из следующего списка строк (вывод `show mac address-table`) извлеките список словарей `[{"vlan": int, "mac": str, "port": str}]`:
   ```
   "  10    aabb.cc00.6500    DYNAMIC     Gi0/1"
   "  20    dead.beef.0001    DYNAMIC     Gi0/2"
   ```
8. **Сложнее:** дан вложенный словарь. Напишите функцию `flatten_dict(d: dict, sep: str = ".") -> dict`, «выравнивающую» его: `{"a": {"b": 1, "c": 2}}` → `{"a.b": 1, "a.c": 2}`.

---

## Частые ошибки

```python
# Изменение списка во время итерации
for item in lst:
    lst.remove(item)   # пропускает элементы! итерируйтесь по копии

# Правильно:
for item in lst[:]:    # срез — копия
    lst.remove(item)

# Мутабельное значение по умолчанию в функции (антипаттерн)
def add(item, lst=[]):     # [] создаётся ОДИН РАЗ!
    lst.append(item)
    return lst

# Правильно:
def add(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

# dict.get() — используйте его чтобы избежать KeyError
d = {"a": 1}
d["b"]           # KeyError
d.get("b")       # None
d.get("b", 0)    # 0
```

---

## Самопроверка

- Знаете разницу между `append` и `extend`.
- Умеете писать list/dict comprehension с условием.
- Понимаете, что `d.get("key")` безопаснее `d["key"]` для потенциально отсутствующих ключей.
- Знаете, когда нужна глубокая копия, а когда достаточно поверхностной.
