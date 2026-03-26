# Топик 15. Scrapli

## Цели

- Понимать Scrapli как современную альтернативу Netmiko с единым API и опциональным **async**.
- Перенести простой сценарий с Netmiko на Scrapli.

## Теория (тезисы)

- **Scrapli** поддерживает SSH (system/openssh, paramiko, ssh2), Telnet; драйверы `cisco_iosxe`, `junos`, и т.д.
- Паттерн: `Scrape(**conn_data)` или фабрика `AsyncScrape`; методы `send_command`, `send_configs`.
- **Async** полезен при сотнях устройств — изучите после синхронного варианта.
- Совместимость с Nornir через `nornir_scrapli`.

## Пример

```python
from scrapli import Scrapli

conn = Scrapli(
    host="192.0.2.1",
    auth_username="admin",
    auth_password="secret",
    platform="cisco_iosxe",
)
conn.open()
response = conn.send_command("show version")
conn.close()
print(response.result)
```

## Практика

1. Повторите лабу из топика 12: получите `show version` через Scrapli и сравните время выполнения (не строго, на глаз).
2. Оберните вызов в функцию `run_show_command(host, command) -> str` с контекстом `open/close` или context manager.
3. **Офлайн:** изучите API без подключения — напишите unit-тест с подменой ответа (мок объекта `response.result`).

## Ссылки

- [Scrapli](https://scrapli.github.io/scrapli/)
