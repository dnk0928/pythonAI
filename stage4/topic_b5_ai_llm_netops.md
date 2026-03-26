# Топик B5. ИИ-ассистент в NetOps (LLM API)

## Цели

- Использовать LLM API для конкретных сетевых задач: генерация конфига, анализ лога, объяснение traceback.
- Понимать ограничения и правила безопасности при использовании ИИ в NetOps.

## Теория (тезисы)

- **LLM в сетевой автоматизации (2026):** не замена Python, а инструмент ускорения; логика и безопасность — на вас.
- **Доступные API:** `openai` (GPT-4o), `anthropic` (Claude), `litellm` (унифицированный клиент), `ollama` (локальные модели без отправки данных в облако).
- **Основной паттерн:** системный промпт с контекстом → пользовательский запрос → ответ → парсинг/применение.
- **Где помогает:** черновик TextFSM/Jinja2, объяснение traceback, нормализация MAC/VLAN, первый шаг regex, резюме длинного `show`.
- **Где НЕ помогает:** замена live-coding на собеседовании; принятие решений о production-изменениях без review.

## Правила безопасности при работе с LLM

- **Никогда** не отправляйте реальные IP, credentials, конфигурации производственной сети в публичные API (GPT, Claude).
- Используйте **заглушки** (`r1`, `10.0.0.1`, `secret`) или **локальные модели** (`ollama`) для работы с реальными данными.
- Валидируйте весь сгенерированный конфиг **вручную** перед применением.

## Примеры использования

### Анализ traceback

```python
import openai

client = openai.OpenAI()  # ключ из OPENAI_API_KEY

def explain_error(traceback: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты помощник сетевого инженера. Объясни ошибку Python кратко на русском."},
            {"role": "user", "content": traceback},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content
```

### Генерация черновика Jinja2-шаблона

```python
prompt = """
Создай минимальный Jinja2-шаблон для Cisco IOS, 
который конфигурирует список VLAN из переменной vlans: list[dict] с полями id и name.
"""
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Ты эксперт по сетевой автоматизации."},
        {"role": "user", "content": prompt},
    ]
)
print(response.choices[0].message.content)
```

### Локальная модель через ollama (без отправки данных)

```bash
ollama run llama3.2  # установить ollama отдельно
```

```python
import httpx

def ask_local_llm(prompt: str) -> str:
    resp = httpx.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False},
        timeout=60,
    )
    return resp.json()["response"]
```

## Практика

1. **Безопасно:** возьмите traceback из задания топика 9 и попросите LLM (через API или веб-интерфейс) объяснить его; сравните с тем, что поняли сами.
2. Сгенерируйте черновик TextFSM-шаблона для строки `show mac address-table`; внесите правки вручную и протестируйте на файле из `labs/`.
3. Напишите функцию `summarize_show_output(text: str, model="gpt-4o-mini") -> str`, передающую вывод `show version` и возвращающую одну строку с ключевыми фактами (hostname, version, uptime).
4. **Stretch:** попробуйте `ollama` с локальной моделью (например `qwen2.5-coder`) для генерации фрагмента Netmiko-кода по описанию задачи.

## Инструменты 2026 (краткий обзор)

| Инструмент | Описание | Когда использовать |
|------------|----------|--------------------|
| `openai` | OpenAI API клиент | GPT-4o, cloud |
| `anthropic` | Claude API клиент | Сложный reasoning |
| `litellm` | Единый клиент для всех LLM | Смена провайдера без рефакторинга |
| `ollama` | Локальные LLM (Llama, Qwen, Mistral) | Конфиденциальные данные |
| Cursor / GitHub Copilot | IDE-ассистент | Написание кода, объяснение |
| `langchain` / `langgraph` | Агентные цепочки | Сложные workflow (продвинутый уровень) |

## Ссылки

- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [litellm](https://github.com/BerriAI/litellm)
- [ollama](https://ollama.com/)
