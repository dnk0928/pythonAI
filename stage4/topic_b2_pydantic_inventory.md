# Топик B2. `pydantic` v2 — инвентарь и валидация данных

## Цели

- Заменить «голые» `dict` в инвентаре и ответах API на **typed-модели** с автоматической валидацией.
- Ловить ошибки структуры данных на входе, а не в середине скрипта.

## Теория (тезисы)

- **`pydantic` v2** — де-факто стандарт для валидации данных в Python; значительно быстрее v1 (Rust-ядро).
- **`BaseModel`** — декларируете поля с типами; pydantic проверяет и приводит типы при создании объекта.
- **`model_validator`** / **`field_validator`** — кастомные проверки (например, диапазон порта, формат IP).
- Загрузка из dict: `Device.model_validate(d)`; из JSON: `Device.model_validate_json(json_str)`.
- **`ValidationError`** даёт список всех ошибок сразу — удобнее, чем последовательные `assert`.

## Пример

```python
from pydantic import BaseModel, field_validator
import ipaddress

class Device(BaseModel):
    hostname: str
    host: str
    device_type: str
    username: str
    role: str = "unknown"
    site: str = "UNSET"

    @field_validator("host")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        ipaddress.ip_address(v)  # ValueError если неверный IP
        return v

# Загрузка инвентаря
import json
from pathlib import Path
from pydantic import ValidationError

raw = json.loads(Path("labs/inventory.json").read_text())
devices: list[Device] = []
for item in raw:
    try:
        devices.append(Device.model_validate(item))
    except ValidationError as e:
        print(f"Невалидная запись: {e.errors()}")
```

## Практика

1. Замените загрузку `labs/inventory.json` на `Device.model_validate` в скрипте из топика 10 (или 25). Убедитесь, что запись с неверным IP (`"host": "999.999.999.999"`) даёт читаемую ошибку, а не `KeyError` позже.
2. Создайте модель `NapalmFacts` по структуре `labs/sample_outputs/napalm_facts_example.json` — все поля опциональные, но `hostname` обязателен.
3. Добавьте модель `CliCommand(command: str, timeout: int = 30)` и используйте её вместо `dict` при вызове Netmiko.
4. **2026-навык:** используйте `model.model_dump()` для передачи в Jinja2-шаблон вместо `asdict`.

## Когда использовать `pydantic`

- Инвентарь из внешних файлов (JSON / YAML / API).
- Ответы REST API контроллеров (топик B3).
- Конфигурационные объекты для Jinja2-шаблонов.

## Ссылки

- [Pydantic v2 docs](https://docs.pydantic.dev/latest/)
