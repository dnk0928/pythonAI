# Топик 27. Мини-проект C — единый парсер отчёта

## Цель

Объединить **TextFSM** (или regex) и **Jinja2** для превращения сырого CLI в **читаемый отчёт** (Markdown/HTML).

## Постановка

1. Возьмите файлы [`../labs/sample_outputs/show_ip_int_brief.txt`](../labs/sample_outputs/show_ip_int_brief.txt) и [`../labs/sample_outputs/show_mac_address_table.txt`](../labs/sample_outputs/show_mac_address_table.txt).
2. Распарсите таблицы в **список словарей** (TextFSM или аккуратный regex).
3. С помощью Jinja2 сгенерируйте `report.html` или `report.md` с таблицами и заголовком «Lab report».
4. Добавьте в отчёт сводку: сколько интерфейсов в состоянии `up/up`, сколько уникальных MAC.

## Критерии приёмки

- Парсер вынесен в отдельный модуль `parse.py`, шаблон — в `templates/report.j2`.
- Запуск `python3 build_report.py` создаёт артефакт в `artifacts/`.

## Связь с выпускным проектом

- Этот мини-проект — частный случай [CAPSTONE.md](../CAPSTONE.md); можно расширить до сборки с реальных устройств.
