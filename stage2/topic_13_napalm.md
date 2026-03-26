# Топик 13. NAPALM

## Цели

- Получать структурированные **факты** с устройства единым API.
- Понимать идею **getters** и ограничения по драйверам.

## Теория (тезисы)

- **NAPALM** абстрагирует различия вендоров: `get_facts`, `get_interfaces`, `get_interfaces_ip`, `get_arp_table`, …
- Подключение через отдельный драйвер: `get_network_driver("ios")`, затем `driver(hostname, username, password)` и `device.open()`.
- **JSON-подобные** структуры — удобно отдавать в шаблоны и схемы.
- **load_merge_candidate / load_replace_candidate + commit** — конфигурационные операции (осторожно на проде).

## Пример

```python
from napalm import get_network_driver

driver = get_network_driver("ios")
device = driver("192.0.2.1", "admin", "secret")
device.open()
facts = device.get_facts()
device.close()
```

## Практика

1. Выведите `get_facts()` в JSON в stdout (`json.dumps(..., indent=2)`).
2. Сравните список интерфейсов из `get_interfaces()` с выводом `show ip int brief` (на одном устройстве).
3. Сохраните `get_arp_table()` в файл `artifacts/arp_r1.json`.
4. **Офлайн:** прочитайте заранее сохранённый JSON фактов и напишите скрипт, который печатает только `hostname` и `os_version`.

## Ссылки

- [NAPALM](https://napalm.readthedocs.io/)
