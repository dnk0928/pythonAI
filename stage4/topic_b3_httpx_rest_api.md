# Топик B3. `httpx` и REST API сетевых контроллеров

## Цели

- Выполнять GET/POST к REST API сетевого контроллера или NMS.
- Работать с JSON-ответом, обрабатывать ошибки HTTP и таймауты.

## Теория (тезисы)

- **REST API** — стандартный интерфейс большинства современных контроллеров: Cisco DNA Center, NSO, IOS-XE RESTCONF, Aruba Central, и т.д.
- **`httpx`** — современная библиотека; поддерживает sync и async (`AsyncClient`), HTTP/2, похожа на `requests` по API.
- **`requests`** — более старая, широко используется; выбирайте `httpx` для async и HTTP/2.
- Аутентификация: Basic Auth (`auth=`), Bearer token (`headers={"Authorization": "Bearer <token>"}`), cookie.
- **RESTCONF** (RFC 8040) — REST поверх YANG-моделей: доступен на IOS-XE 16.x+; пути вида `/restconf/data/...`.

## Пример (синхронный)

```python
import httpx

BASE_URL = "https://192.0.2.100/dna/system/api/v1"

def get_auth_token(username: str, password: str) -> str:
    resp = httpx.post(
        f"{BASE_URL}/auth/token",
        auth=(username, password),
        verify=False,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["Token"]

def get_network_devices(token: str) -> list[dict]:
    resp = httpx.get(
        f"{BASE_URL}/network-device",
        headers={"X-Auth-Token": token},
        verify=False,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["response"]
```

## Пример (RESTCONF на IOS-XE)

```python
import httpx

resp = httpx.get(
    "https://192.0.2.1/restconf/data/ietf-interfaces:interfaces",
    auth=("admin", "secret"),
    headers={"Accept": "application/yang-data+json"},
    verify=False,
)
print(resp.json())
```

## Практика

1. Загрузите mock-ответ из `labs/mock_api/dnac_devices.json` (создан в рамках labs-mock-data) и напишите функцию `parse_device_list(data: dict) -> list[dict]` — извлеките `hostname` и `managementIpAddress`.
2. Напишите async-вариант с `httpx.AsyncClient` и `asyncio.gather` для опроса двух endpoint-ов одновременно.
3. Обработайте `httpx.HTTPStatusError` (4xx/5xx) и `httpx.TimeoutException` без падения скрипта.
4. **2026-задача:** пройдите документацию RESTCONF вашей платформы (IOS-XE, EOS, JunOS) и выполните `GET` к `/restconf/data/ietf-system:system` — залогируйте `system-name`.

## Когда `httpx` vs `netmiko`

| Устройство | Интерфейс | Инструмент |
|------------|-----------|------------|
| Cisco IOS (старый) | CLI SSH | Netmiko |
| IOS-XE 16+ | RESTCONF | httpx |
| Cisco DNA Center | REST API | httpx |
| Juniper JunOS | NETCONF / REST | ncclient / httpx |
| Wi-Fi контроллер | REST API | httpx |

## Ссылки

- [httpx](https://www.python-httpx.org/)
- [RESTCONF — RFC 8040](https://datatracker.ietf.org/doc/html/rfc8040)
