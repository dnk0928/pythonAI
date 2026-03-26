# Топик B4. gNMI и потоковая телеметрия

## Цели

- Понять концепцию **gNMI** и **streaming telemetry** как замену периодическому опросу SNMP.
- Выполнить `Get` и `Subscribe` через `pygnmi` на lab-устройстве.

## Теория (тезисы)

- **gNMI** (gRPC Network Management Interface) — бинарный протокол поверх gRPC/HTTP2; работает с YANG-моделями.
- **Четыре операции:** `Get`, `Set`, `Subscribe`, `Capabilities`.
- **Subscribe** режимы: `ONCE` (как Get, но поток), `POLL`, `STREAM` (непрерывная телеметрия).
- Пути данных — **gNMI path** вида `openconfig-interfaces:interfaces/interface[name=Gi0/0]/state/counters`.
- **`pygnmi`** — Python-клиент; **`cisco-gnmi-python`** — Cisco-специфичный (поддерживает gRPC channel options).
- В отличие от SNMP нет polling overhead — устройство **само толкает** данные.

## Пример (pygnmi, синхронный Get)

```python
from pygnmi.client import gNMIclient

TARGET = ("192.0.2.1", 57400)

with gNMIclient(target=TARGET, username="admin", password="secret", insecure=True) as gc:
    capabilities = gc.capabilities()
    print([m["name"] for m in capabilities["supported_models"][:3]])

    result = gc.get(path=["openconfig-interfaces:interfaces"])
    print(result)
```

## Пример (Subscribe ONCE)

```python
with gNMIclient(target=TARGET, username="admin", password="secret", insecure=True) as gc:
    subscriptions = [
        {"path": "openconfig-interfaces:interfaces/interface[name=GigabitEthernet1]/state/counters/in-octets"}
    ]
    for update in gc.subscribe(subscribe={"subscription": subscriptions, "mode": "once"}):
        print(update)
```

## Практика

1. **Офлайн:** изучите mock-ответ `labs/mock_api/gnmi_get_interfaces.json` и напишите функцию, извлекающую список имён интерфейсов из структуры gNMI-ответа.
2. На lab-устройстве с включённым gNMI (IOS-XE: `gnxi`, Arista EOS: `management api gnmi`) выполните `gc.capabilities()` и `gc.get(path=["ietf-interfaces:interfaces"])`.
3. Сравните структуру gNMI-ответа с NETCONF XML из топика 17 — какой удобнее парсить?
4. **Stretch:** реализуйте подписку `STREAM` на счётчики интерфейса и записывайте значения в CSV каждые 10 секунд.

## gNMI vs SNMP vs NETCONF

| Критерий | SNMP | NETCONF | gNMI |
|----------|------|---------|------|
| Транспорт | UDP | SSH | gRPC/HTTP2 |
| Формат | BER | XML | Protobuf / JSON |
| Push-телеметрия | Только traps | Нет | Да (Subscribe STREAM) |
| Модели | MIB | YANG | YANG |
| Скорость | Медленно | Средне | Быстро |

## Ссылки

- [pygnmi](https://github.com/akarneliuk/pygnmi)
- [OpenConfig](https://www.openconfig.net/)
- [gNMI spec](https://github.com/openconfig/gnmi)
