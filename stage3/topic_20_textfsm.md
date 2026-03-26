# Топик 20. TextFSM и ntc-templates

## Цели

- Парсить табличный вывод CLI в **список словарей** с помощью TextFSM.
- Использовать готовые шаблоны из **ntc-templates** там, где они есть.

## Теория (тезисы)

- **TextFSM** — шаблон: **Value** строки (переменные) + **Start/Record** состояния.
- Каждая **запись** (строка таблицы) становится словарём с ключами из `Value`.
- **ntc-templates** — коллекция шаблонов под `netmiko`/`napalm`; путь задаётся переменной окружения `NTC_TEMPLATES` или через API библиотеки.
- Альтернатива: **TTP**, Genie — по ситуации.

## Пример

```python
import io
import textfsm
from pathlib import Path

template = Path("templates/cisco_ios_show_ip_interface_brief.textfsm").read_text()
raw = Path("../labs/sample_outputs/show_ip_int_brief.txt").read_text()
fsm = textfsm.TextFSM(io.StringIO(template))
rows = fsm.ParseText(raw)
# rows — list[list[str]]; заголовки — fsm.header
```

## Практика

1. Установите `ntc-templates`, найдите шаблон для `cisco_ios_show_ip_interface_brief` в пакете и распарсите файл из лабы в список словарей (через `ntc_templates.parse` если используете обёртку из документации).
2. Сохраните результат в `artifacts/interfaces_r1.json`.
3. Напишите **минимальный** собственный `.textfsm` для упрощённого вывода из 3–4 строк (учебный шаблон).
4. Сравните трудоёмкость с regex-only подходом для той же таблицы.

## Ссылки

- [TextFSM](https://github.com/google/textfsm)
- [ntc-templates](https://github.com/networktocode/ntc-templates)
