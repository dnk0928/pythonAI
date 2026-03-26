# Топик 24. Jinja2 и классы

## Цели

- Генерировать фрагменты конфигурации из **шаблонов** и словарей контекста.
- Инкапсулировать данные устройства в простом **классе** Python.

## Теория (тезисы)

- **Jinja2** — шаблоны с `{{ var }}`, `{% for %}`, `{% if %}`, фильтрами `| upper`, `| join`.
- Отделяйте **шаблон** (`.j2`) от **кода**; загружайте через `Environment` и `FileSystemLoader`.
- **Класс** в Python — соглашение `dataclass` для полей устройства: `hostname`, `interfaces`, `vlans`.
- Шаблон получает либо `dict`, либо объект с атрибутами (удобно передавать `asdict` из dataclass).

## Пример

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True)
tpl = env.get_template("interface_descriptions.j2")
print(tpl.render(hostname="sw1", interfaces=[{"name": "Gi0/1", "desc": "UPLINK"}]))
```

## Практика

1. Создайте шаблон `templates/vlans.j2`, генерирующий блок `vlan X` / `name Y` для списка VLAN из словаря.
2. Опишите класс `Device` с полями `hostname`, `interfaces: list[dict]`; метод `render_config(self, env) -> str`.
3. Добавьте в шаблон условие: если `shutdown` в данных интерфейса — строка `shutdown`, иначе `no shutdown`.
4. **Сеть:** сгенерируйте конфиг и **не применяйте** на прод без review; для lab сохраните в `artifacts/generated_config.txt`.

## Ссылки

- [Jinja2](https://jinja.palletsprojects.com/)
