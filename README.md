# Интенсивный практический курс: Python для сетевого инженера

## Почему появился этот курс и кто его создал

Этот курс написан в марте 2026 года с помощью **AI-ассистента Cursor** (модель Claude) по запросу сетевого инженера.

Курс создавался итерационно: сначала был сформирован план (три этапа: Core → Сети → Интеграция), затем реализованы все топики, добавлены лабораторные данные для офлайн-практики, выпускной проект и — в ходе доработки — бонус-трек для современного стека 2026 года (async, pydantic, REST API, gNMI, LLM).

**Целевая аудитория:** сетевой инженер с нулём или минимумом Python, которому нужно в сжатые сроки преодолеть порог вхождения и начать автоматизировать реальные задачи.

**Рекомендованный стек по фидбеку работодателя:** Paramiko, Netmiko, NAPALM, Nornir, Scrapli, pysnmp, ncclient, pyATS, PyEZ, Jinja2, TextFSM, regex, JSON/YAML, XML/XPath, lxml, JSONPath, JSON Schema.

**Принцип всего курса:** короткая тезисная теория → сразу практика, имитирующая реальную рабочую задачу.

---

## О структуре и навигации

Краткая теория + максимум практики. Проходите топики по порядку; параллельно этапу 1 полезна практика на [Codewars](https://www.codewars.com/) (8–7 kyu, Python).

**Структура:** в каждом файле топика — тезисы теории, примеры и **практические задания**. Дополнительные вводные и примеры выводов CLI — в каталоге [`labs/`](labs/).

**Прогресс и навыки (2026):** отмечайте пройденное и уровень компетенций в [PROGRESS.md](PROGRESS.md). Рекомендации по усилению курса, современному стеку и работе с ИИ — в [COURSE_ENHANCEMENTS_2026.md](COURSE_ENHANCEMENTS_2026.md).

### Как повысить эффективность прохождения

- Держите **один репозиторий** с кодом и обновляйте [PROGRESS.md](PROGRESS.md) раз в неделю.
- **Core Python** не пропускайте: без него библиотеки сети и ИИ-ассистенты дают «ложное чувство умения».
- Используйте нейросети для **объяснений** и **рефакторинга**, но решайте live-coding и разбор traceback **самостоятельно** до подсказок.
- Для 2026 года полезно параллельно освоить **Git**, **pytest** на одной функции и **HTTP API** (`httpx`) — см. таблицу в [PROGRESS.md](PROGRESS.md).

---

## Этап 1 — Core Python

| № | Топик | Файл |
|---|--------|------|
| 1 | Окружение и первый скрипт | [stage1/topic_01_environment.md](stage1/topic_01_environment.md) |
| 2 | Типы и переменные | [stage1/topic_02_types_variables.md](stage1/topic_02_types_variables.md) |
| 3 | Строки и f-strings | [stage1/topic_03_strings_fstrings.md](stage1/topic_03_strings_fstrings.md) |
| 4 | Списки и словари | [stage1/topic_04_lists_dicts.md](stage1/topic_04_lists_dicts.md) |
| 5 | Кортежи и множества | [stage1/topic_05_tuples_sets.md](stage1/topic_05_tuples_sets.md) |
| 6 | Ветвления и циклы | [stage1/topic_06_control_flow.md](stage1/topic_06_control_flow.md) |
| 7 | Функции | [stage1/topic_07_functions.md](stage1/topic_07_functions.md) |
| 8 | Работа с файлами | [stage1/topic_08_files.md](stage1/topic_08_files.md) |
| 9 | Исключения | [stage1/topic_09_exceptions.md](stage1/topic_09_exceptions.md) |
| 10 | Модули и пакеты | [stage1/topic_10_modules.md](stage1/topic_10_modules.md) |
| 10a | `ipaddress` — адреса и сети | [stage1/topic_10a_ipaddress.md](stage1/topic_10a_ipaddress.md) |
| 10b | `logging` — структурированные логи | [stage1/topic_10b_logging.md](stage1/topic_10b_logging.md) |

**Задания этапа 1 (сводка):** [assignments/stage1/README.md](assignments/stage1/README.md)

---

## Этап 2 — Сетевые библиотеки

| № | Топик | Файл |
|---|--------|------|
| 11 | SSH: Paramiko | [stage2/topic_11_paramiko.md](stage2/topic_11_paramiko.md) |
| 12 | Netmiko | [stage2/topic_12_netmiko.md](stage2/topic_12_netmiko.md) |
| 13 | NAPALM | [stage2/topic_13_napalm.md](stage2/topic_13_napalm.md) |
| 14 | Nornir и инвентарь | [stage2/topic_14_nornir.md](stage2/topic_14_nornir.md) |
| 15 | Scrapli | [stage2/topic_15_scrapli.md](stage2/topic_15_scrapli.md) |
| 16 | SNMP (pysnmp) | [stage2/topic_16_snmp.md](stage2/topic_16_snmp.md) |
| 17 | NETCONF (ncclient) | [stage2/topic_17_netconf.md](stage2/topic_17_netconf.md) |
| 18 | Вендор-инструменты (pyATS / PyEZ) | [stage2/topic_18_vendor_tools.md](stage2/topic_18_vendor_tools.md) |

**Задания этапа 2:** [assignments/stage2/README.md](assignments/stage2/README.md)

---

## Этап 3 — Парсинг, шаблоны, проекты

| № | Топик | Файл |
|---|--------|------|
| 19 | Регулярные выражения (`re`) | [stage3/topic_19_regex.md](stage3/topic_19_regex.md) |
| 20 | TextFSM и ntc-templates | [stage3/topic_20_textfsm.md](stage3/topic_20_textfsm.md) |
| 21 | JSON и YAML | [stage3/topic_21_json_yaml.md](stage3/topic_21_json_yaml.md) |
| 22 | XML, XPath, lxml | [stage3/topic_22_xml_lxml.md](stage3/topic_22_xml_lxml.md) |
| 23 | JSONPath и JSON Schema | [stage3/topic_23_jsonpath_schema.md](stage3/topic_23_jsonpath_schema.md) |
| 24 | Jinja2 и классы | [stage3/topic_24_jinja2_classes.md](stage3/topic_24_jinja2_classes.md) |
| 25 | Мини-проект A (uptime → CSV) | [stage3/topic_25_project_a.md](stage3/topic_25_project_a.md) |
| 26 | Мини-проект B (шаблон + выкат) | [stage3/topic_26_project_b.md](stage3/topic_26_project_b.md) |
| 27 | Мини-проект C (парсер отчёта) | [stage3/topic_27_project_c.md](stage3/topic_27_project_c.md) |

**Задания этапа 3:** [assignments/stage3/README.md](assignments/stage3/README.md)

---

## Этап 4 — Бонус-трек 2026 (необязательный)

Проходите параллельно с выпускным проектом или после. Каждый топик самодостаточен.

| № | Топик | Файл |
|---|--------|------|
| B1 | `asyncio` + AsyncScrapli | [stage4/topic_b1_asyncio_scrapli.md](stage4/topic_b1_asyncio_scrapli.md) |
| B2 | `pydantic` v2 — валидация инвентаря | [stage4/topic_b2_pydantic_inventory.md](stage4/topic_b2_pydantic_inventory.md) |
| B3 | `httpx` и REST API контроллеров | [stage4/topic_b3_httpx_rest_api.md](stage4/topic_b3_httpx_rest_api.md) |
| B4 | gNMI и streaming telemetry | [stage4/topic_b4_gnmi_telemetry.md](stage4/topic_b4_gnmi_telemetry.md) |
| B5 | ИИ-ассистент в NetOps (LLM API) | [stage4/topic_b5_ai_llm_netops.md](stage4/topic_b5_ai_llm_netops.md) |
| B6 | `pytest` для сетевых скриптов | [stage4/topic_b6_pytest_network.md](stage4/topic_b6_pytest_network.md) |

Mock-данные для офлайн-практики Stage 4: [`labs/mock_api/`](labs/mock_api/)

---

## Выпускной проект и собеседование

- [CAPSTONE.md](CAPSTONE.md) — итоговое ТЗ и критерии приёмки  
- [LIVE_CODING_INTERVIEW.md](LIVE_CODING_INTERVIEW.md) — live-coding, задачи в стиле собеседования  

---

## Зависимости (этапы 2–4)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Документация стандартной библиотеки: [Python 3 Library](https://docs.python.org/3/library/).
