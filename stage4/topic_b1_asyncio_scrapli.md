# Топик B1. `asyncio` и AsyncScrapli

## Цели

- Понять модель кооперативной многозадачности `asyncio` на практическом примере.
- Использовать **AsyncScrapli** для параллельного опроса десятков устройств.

## Теория (тезисы)

- **`asyncio`** — event loop, корутины (`async def`), ожидание (`await`), задачи (`asyncio.gather`).
- Сетевые IO-операции (SSH, TCP) — основной сценарий: пока одно соединение ждёт ответа, event loop запускает следующее.
- **Синхронно vs async:** 20 устройств × 3 с каждое = 60 с синхронно; ~3–4 с async.
- **`AsyncScrapli`** — drop-in замена `Scrapli`; добавляется `async with` и `await`.
- `asyncio.gather(*coros)` — запуск нескольких корутин «параллельно» (в рамках одного потока).

## Пример

```python
import asyncio
from scrapli import AsyncScrapli

HOSTS = [
    {"host": "192.0.2.1", "auth_username": "admin", "auth_password": "secret", "platform": "cisco_iosxe"},
    {"host": "192.0.2.2", "auth_username": "admin", "auth_password": "secret", "platform": "cisco_iosxe"},
]

async def collect_one(params: dict) -> dict:
    async with AsyncScrapli(**params) as conn:
        resp = await conn.send_command("show clock")
        return {"host": params["host"], "output": resp.result}

async def main():
    results = await asyncio.gather(*[collect_one(h) for h in HOSTS], return_exceptions=True)
    for r in results:
        if isinstance(r, Exception):
            print(f"Error: {r}")
        else:
            print(r["host"], r["output"][:30])

asyncio.run(main())
```

## Практика

1. **Офлайн:** сделайте заглушку `fake_collect_one(params)` с `await asyncio.sleep(1)` и убедитесь, что 10 вызовов через `gather` занимают ~1 с, а не 10 с.
2. Переведите **Мини-проект A** (топик 25) с Netmiko на AsyncScrapli; сравните время на lab или с заглушками.
3. Обработайте исключения: `return_exceptions=True` + проверка `isinstance(r, Exception)` — логируйте через `logging` из топика 10b.
4. Добавьте **семафор** `asyncio.Semaphore(10)` для ограничения числа одновременных подключений.

## Когда нужен async, а когда нет

| Ситуация | Решение |
|----------|---------|
| 1–5 устройств | Синхронный Netmiko / Scrapli |
| 10–100 устройств | AsyncScrapli или Nornir (threaded) |
| 100+ устройств | AsyncScrapli + Semaphore |
| Параллельные HTTP API | `httpx.AsyncClient` (топик B3) |

## Ссылки

- [AsyncScrapli](https://scrapli.github.io/scrapli/user_guide/async_usage/)
- [asyncio — Python docs](https://docs.python.org/3/library/asyncio.html)
