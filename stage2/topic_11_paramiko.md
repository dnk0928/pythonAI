# Топик 11. SSH: Paramiko

## Цели

- Установить SSH-сессию и выполнить команду на сетевом устройстве (или Linux-хосте).
- Понимать разницу между `exec_command` и интерактивной оболочкой.

## Теория (тезисы)

- **Paramiko** — низкоуровневый SSH-клиент: транспорт, ключи, пароль, `SSHClient`.
- Типовой сценарий: `SSHClient()`, `set_missing_host_key_policy()`, `connect()`, `exec_command("show version")`, чтение `stdout`/`stderr`.
- **Exec channel** часто подходит для **одной** команды; интерактивные сессии (shell) сложнее и реже нужны при наличии Netmiko.
- Таймауты и буферизация: читайте `stdout` до EOF; для «длинных» выводов учитывайте время.

## Пример

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.0.2.1", username="admin", password="secret", timeout=10)
stdin, stdout, stderr = client.exec_command("show version")
output = stdout.read().decode()
client.close()
```

## Практика

1. Подключитесь к lab-устройству или Linux по SSH, выполните `uname -a` или `show version`, сохраните вывод в файл `artifacts/paramiko_show_version.txt`.
2. Добавьте обработку `socket.timeout` / `paramiko.SSHException` с понятным сообщением.
3. **Без железа:** прочитайте готовый текстовый файл с «выводом» и напишите функцию-заглушку `fake_exec(cmd) -> str`, чтобы тренировать остальной код офлайн.

## Самопроверка

- Пароль не в коде: `os.environ["LAB_SSH_PASSWORD"]`.

## Ссылки

- [Paramiko документация](https://docs.paramiko.org/)
