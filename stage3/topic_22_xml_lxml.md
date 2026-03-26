# Топик 22. XML, XPath, lxml

## Цели

- Находить узлы в XML ответе NETCONF или API с помощью **XPath**.
- Понимать разницу между `xml.etree.ElementTree` и `lxml` (скорость, XPath).

## Теория (тезисы)

- **XML** — иерархия элементов с атрибутами и пространствами имён (**ns**). NETCONF часто использует префиксы `nc:`, `config:`.
- **XPath** — язык запросов к XML: `/top/device/hostnames`, `//hostname`, условия `[@name='r1']`.
- С **пространствами имён** проще работать через полные URI в словаре префиксов или обход с `lxml.etree`.

## Пример (ElementTree + namespaces)

```python
import xml.etree.ElementTree as ET

root = ET.fromstring(xml_text)
ns = {"nc": "urn:ietf:params:xml:ns:netconf:base:1.0"}
node = root.find(".//nc:rpc-reply", ns)
```

## Практика

1. Откройте [`../labs/sample_outputs/netconf_get_config_snippet.xml`](../labs/sample_outputs/netconf_get_config_snippet.xml) и извлеките текст hostname (подстройте XPath под фактическую структуру файла).
2. Повторите задачу с `lxml.etree` и сравните удобство.
3. Напишите функцию `get_text_by_localname(root, name) -> str | None`, ищущую первый элемент с локальным именем `name` без учёта префикса (учебный рекурсивный обход).
4. **Сеть:** обсудите с ментором, когда хранить конфиг как XML в файлах, а когда — только на устройстве.

## Ссылки

- [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [lxml](https://lxml.de/)
