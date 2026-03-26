# Топик 14. Nornir и инвентарь

## Цели

- Описать устройства в **инвентаре** и выполнить задачу **параллельно** для группы хостов.
- Разделять данные (YAML/hosts) и код задачи.

## Теория (тезисы)

- **Nornir** — оркестратор: инвентарь + плагины (Netmiko, Napalm, HTTP).
- **`InitNornir(config_file="config.yaml")`** — загрузка настроек; хосты из YAML/других источников.
- **Task** — функция `(task, **kwargs)`; результат в `task.host` и `MultiResult`.
- **Параллелизм:** `nr.run(task=netmiko_task)`; настраивайте `num_workers` разумно для SSH.

## Пример (упрощённо)

```python
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

nr = InitNornir(config_file="nornir_config.yaml")
result = nr.run(task=netmiko_send_command, command_string="show clock")
```

## Практика

1. Используйте [`../labs/nornir_config.yaml`](../labs/nornir_config.yaml) и хосты в [`../labs/nornir/hosts.yaml`](../labs/nornir/hosts.yaml). Запускайте из каталога `pythonAI/`, чтобы относительные пути совпали; добавьте пароль через переменные окружения и `defaults` в коде или расширьте инвентарь по документации Nornir.
2. Задача: собрать `show clock` со всех хостов группы `switches` и записать в отдельные файлы `artifacts/{host}_clock.txt`.
3. Обработайте ошибки подключения: выведите список хостов, где задача упала (`result.failed_hosts`).
4. **Офлайн:** замените task на чтение локального файла с выводом по имени хоста из [`../labs/sample_outputs/`](../labs/sample_outputs/).

## Ссылки

- [Nornir](https://nornir.readthedocs.io/)
