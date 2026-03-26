# Топик 23. JSONPath и JSON Schema

## Цели

- Доставать вложенные поля из большого JSON одним выражением (**JSONPath**).
- Валидировать структуру JSON от API/NAPALM по **схеме**.

## Теория (тезисы)

- **JSONPath** (реализация `jsonpath-ng`): выражения вроде `$.interfaces[*].name`, фильтры.
- **JSON Schema** описывает обязательные ключи, типы, перечисления; библиотека `jsonschema` проверяет `validate(instance, schema)`.
- Полезно для CI: «ответ устройства/контроллера соответствует контракту».

## Пример

```python
from jsonpath_ng import parse

expr = parse("$.facts.hostname")
match = expr.find(payload)
value = match[0].value if match else None
```

```python
import jsonschema

schema = {"type": "object", "required": ["hostname"], "properties": {"hostname": {"type": "string"}}}
jsonschema.validate({"hostname": "r1"}, schema)
```

## Практика

1. Возьмите сохранённый JSON фактов NAPALM и извлеките `hostname` и `os_version` через JSONPath.
2. Составьте минимальную JSON Schema для объекта `{"host": str, "ip": str, "role": "router"|"switch"}` и проверьте валидный и невалидный примеры.
3. Обработайте `jsonschema.ValidationError` и выведите человекочитаемое сообщение.

## Ссылки

- [jsonpath-ng](https://github.com/h2non/jsonpath-ng)
- [JSON Schema](https://json-schema.org/)
