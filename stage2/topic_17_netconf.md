# Топик 17. NETCONF (ncclient)

## Цели

- Получить фрагмент **running-config** или данных модели через NETCONF.
- Понимать XML-ответ и связь с YANG (без углубления в все модули).

## Теория (тезисы)

- **NETCONF** — RPC поверх SSH (обычно порт 830); обмен **XML** сообщениями.
- **ncclient** — Python-клиент: `manager.connect()`, `get_config`, `get`, `edit_config`.
- Источник данных: `running`, `candidate`, `startup` (зависит от платформы).
- Для фильтрации используют **subtree** или **XPath** фильтр в теле RPC.

## Пример

```python
from ncclient import manager

with manager.connect(
    host="192.0.2.1",
    port=830,
    username="admin",
    password="secret",
    hostkey_verify=False,
) as m:
    c = m.get_config(source="running")
    print(c.xml)
```

## Практика

1. Подключитесь к устройству с включённым NETCONF, сохраните **сырой XML** `get_config` в `artifacts/running_netconf.xml`.
2. Найдите в XML узел hostname (имя тега зависит от модели — используйте поиск по подстроке или XPath в топике 22).
3. Сравните трудозатраты NETCONF vs CLI для **той же** задачи на вашей платформе.
4. **Офлайн:** используйте файл [`../labs/sample_outputs/netconf_get_config_snippet.xml`](../labs/sample_outputs/netconf_get_config_snippet.xml) и извлеките текст hostname программно.

## Самопроверка

- `hostkey_verify=False` только в lab; в проде — доверенные ключи.

## Ссылки

- [ncclient](https://ncclient.readthedocs.io/)
