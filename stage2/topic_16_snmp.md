# Топик 16. SNMP (pysnmp)

## Цели

- Выполнить **SNMP GET** (и при необходимости короткий WALK) для опроса счётчиков или sysDescr.
- Понимать роль **community** (v2c) и ограничения безопасности.

## Теория (тезисы)

- **SNMP** — запрос/ответ агента на устройстве; для учебной сети часто **SNMPv2c** с community string.
- **OID** — идентификатор объекта; стандартные ветки: `1.3.6.1.2.1.1` (system), `1.3.6.1.2.1.2` (interfaces).
- Полезные OID: `sysDescr` `.1.3.6.1.2.1.1.1.0`, `sysUpTime` `.1.3.6.1.2.1.1.3.0`.
- **pysnmp** — низкоуровневый API; для простоты можно использовать высокоуровневые хелперы из документации текущей версии.

## Пример (идея, синтаксис зависит от версии pysnmp)

```python
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd

iterator = getCmd(
    SnmpEngine(),
    CommunityData("public"),
    UdpTransportTarget(("192.0.2.1", 161)),
    ContextData(),
    ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),
)
errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
for oid, val in varBinds:
    print(val.prettyPrint())
```

## Практика

1. Опросите `sysDescr` на lab-устройстве с включённым SNMP (или на `snmpd` в Linux).
2. Выведите `sysUpTime` в человекочитаемом виде (секунды/часы — по желанию).
3. Обработайте таймаут и отсутствие ответа без падения скрипта.
4. **Офлайн:** зафиксируйте ожидаемые строки ответа в файле и сравните с результатом парсера OID → значение (учебная заглушка).

## Самопроверка

- Не используйте дефолтные community `public`/`private` в продакшене.

## Ссылки

- [pysnmp](https://pysnmp.com/)
