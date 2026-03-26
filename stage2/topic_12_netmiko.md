# Топик 12. Netmiko

## Цели

- Использовать `ConnectHandler` для CLI-сессий с сетевым оборудованием.
- Отправлять команды show и фрагменты конфигурации; понимать `device_type`.

## Теория (тезисы)

- **Netmiko** строится поверх Paramiko (и др.) и знает **prompt** разных вендоров (`cisco_ios`, `juniper_junos`, `arista_eos`, …).
- **`ConnectHandler(**device)`** — словарь с ключами `device_type`, `host`, `username`, `password`, опционально `secret` (enable), `port`, `timeout`.
- **`send_command()`** — одна show-команда; **`send_config_set()`** — список строк конфига; **`send_config_from_file()`** — из файла.
- **`enable()`** — переход в привилегированный режим на IOS-подобных.

## Пример

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.0.2.1",
    "username": "admin",
    "password": "secret",
}
with ConnectHandler(**device) as conn:
    out = conn.send_command("show version")
```

## Практика

1. Получите `hostname` и версию ПО из `show version` (парсинг вручную или простым `split` на первом этапе).
2. Сохраните полный вывод `show ip interface brief` в файл для последующего TextFSM (топик 20).
3. Выполните `send_config_set` на lab: описание интерфейса `description NETMIKO_LAB` (откатите после проверки).
4. **Офлайн:** используйте файл [`../labs/sample_outputs/show_version_ios.txt`](../labs/sample_outputs/show_version_ios.txt) и напишите скрипт, который только читает его (имитация без подключения).

## Самопроверка

- Всегда используйте `with` или явный `disconnect()`.

## Ссылки

- [Netmiko](https://github.com/ktbyers/netmiko)
