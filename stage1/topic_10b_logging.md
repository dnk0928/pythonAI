# Топик 10b. Модуль `logging`

## Цели

- Заменить `print()` на структурированное логирование с уровнями и сохранением в файл.
- Сконфигурировать логгер один раз на старте скрипта; применять во всех модулях.

## Теория (тезисы)

- `logging` — стандартная библиотека; уровни по возрастанию: `DEBUG < INFO < WARNING < ERROR < CRITICAL`.
- **`logging.basicConfig`** — быстрая настройка; для нескольких хендлеров используют `addHandler`.
- **`getLogger(__name__)`** в каждом модуле — стандартная практика; иерархия логгеров.
- **Форматтер** задаёт строку записи: время, уровень, имя логгера, сообщение.
- В **сетевых скриптах** логируйте: попытку подключения, результат, ошибку с hostname и подробностями.

## Шаблон «конфигурация на старте»

```python
import logging
from pathlib import Path

def setup_logging(level: str = "INFO", log_file: Path | None = None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        handlers=handlers,
    )
```

```python
# в любом модуле проекта:
import logging
log = logging.getLogger(__name__)

log.info("Connecting to %s", hostname)
log.error("Failed: %s — %s", hostname, exc)
```

## Практика

1. Добавьте `setup_logging` в скрипт из мини-проекта A (топик 25): логируйте начало/конец подключения и ошибки на уровне `ERROR`.
2. Запустите скрипт с `level="DEBUG"` и убедитесь, что видите подробный вывод; с `level="WARNING"` — только ошибки.
3. Сохраните лог в файл `artifacts/run_YYYYMMDD.log`; имя файла генерируйте через `datetime.now()`.
4. **Антипаттерн:** найдите в своих скриптах из предыдущих топиков `print(f"Error: {e}")` и замените на `log.error(...)`.

## Самопроверка

- Никогда не используйте `logging.debug(f"..{val}")` — передавайте `%s`-стиль: `log.debug("val=%s", val)` — ленивое вычисление строки.
- Не вызывайте `basicConfig` в библиотечном коде (модулях), только в точке входа (`main.py` / `__main__`).

## Ссылки

- [logging — Python docs](https://docs.python.org/3/library/logging.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
