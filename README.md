# GigaChat OpenAI-Compatible Adapter

[![Build](https://github.com/antonko/gigachat-adapter/actions/workflows/release.yml/badge.svg)](https://github.com/antonko/gigachat-adapter/actions/workflows/release.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/antonk0/gigachat-adapter)](https://hub.docker.com/r/antonk0/gigachat-adapter)

Адаптер предоставляет доступ к GigaChat API через интерфейс, совместимый с OpenAI API, позволяя интегрировать GigaChat в
приложения, изначально ориентированные на OpenAI, с минимальными изменениями кода.

Изначально проект был создан для подключения к сервису Open WebUI. На текущий момент реализована базовая работа с
GigaChat через метод `chat/completions` с поддержкой файлов в сообщениях и tool calling. Таких возможности как
embeddings и т.д будут реализованы по мере необходимости.

## Features

✨ Основные возможности:

- На основе официальной библиотеки [gigachat](https://github.com/ai-forever/gigachat)
- Поддержка `chat/completions` API с потоковой передачей сообщений
- Поддержка файлов в сообщениях исключая повторные загрузки в GigaChat
- Поддержка function call для интеграции с внешними API и сервисами (OpenAI-совместимый формат)
- Docker-образ
- Healthcheck API (ready, live)

### Запуск

#### Using Docker (рекомендуется):

```bash
docker run -p 8000:8000 \
  -e GIGACHAT_CREDENTIALS=your_credentials \
  -e BEARER_TOKEN=your_token \
  -e GIGACHAT_VERIFY_SSL_CERTS=False \
  antonk0/gigachat-adapter:latest
```

Через Docker Compose:

```yaml
services:
  gigachat-adapter:
    image: antonk0/gigachat-adapter:latest
    ports:
      - "8000:8000"
    environment:
      - GIGACHAT_CREDENTIALS=your_credentials
      - BEARER_TOKEN=your_token
      - GIGACHAT_VERIFY_SSL_CERTS=False
```

## Интеграция с OpenAI-совместимыми приложениями

При интеграции адаптера с приложениями, которые поддерживают OpenAI API, используйте следующий базовый URL:

```
http://your-host:8000/v1
```

**Важно**: Для корректной работы с большинством OpenAI-совместимых приложений рекомендуется добавлять `/v1` к базовому URL адаптера (но это не точно).

Примеры настройки:

- **Base URL**: `http://localhost:8000/v1` (для локального запуска)
- **Base URL**: `http://gigachat-adapter:8000/v1` (для Docker Compose)
- **Authorization**: Bearer Token (значение переменной `BEARER_TOKEN`)

## Environment Variables

Below are the environment variables you can set in your .env file:

### GigaChat Settings

Параметры библиотеки [gigachat](https://github.com/ai-forever/gigachat). Параметры должны начинаться с `GIGACHAT_` и
соответствовать параметрам GigaChat API.

| Параметр          | Обязательный | Описание                                                           |
|-------------------|--------------|--------------------------------------------------------------------|
| CREDENTIALS       | Да           | Ключ авторизации для доступа к GigaChat API.API.                   |
| VERIFY_SSL_CERTS  | Нет          | Отключение проверки ssl-сертификатов.                              |
| SCOPE             | Нет          | Версия API: GIGACHAT_API_PERS, GIGACHAT_API_B2B, GIGACHAT_API_CORP |
| MODEL             | Нет          | Модель GigaChat                                                    |
| BASE_URL          | Нет          | URL API                                                            |
| AUTH_URL          | Нет          | URL для авторизации                                                |
| ACCESS_TOKEN      | Нет          | Токен доступа                                                      |
| PROFANITY_CHECK   | Нет          | Модерация                                                          |
| USER              | Нет          | Имя пользователя                                                   |
| PASSWORD          | Нет          | Пароль                                                             |
| TIMEOUT           | Нет          | Таймаут запросов                                                   |
| VERBOSE           | Нет          | Подробный вывод логов                                              |
| CA_BUNDLE_FILE    | Нет          | Путь к корневому сертификату                                       |
| CERT_FILE         | Нет          | Путь к клиентскому сертификату                                     |
| KEY_FILE          | Нет          | Путь к ключу сертификата                                           |
| KEY_FILE_PASSWORD | Нет          | Пароль от ключа сертификата                                        |

### Application Settings

Обязательно надо указать `BEARER_TOKEN` для авторизации запросов к адаптеру.

| Параметр           | Обязательный | Описание                                  |
|--------------------|--------------|-------------------------------------------|
| BEARER_TOKEN       | Да           | Токен для авторизации запросов к адаптеру |
| DEBUG              | Нет          | Режим отладки, подробные логи             |
| ENVIRONMENT        | Нет          | Окружение (development/production)        |
| CORS_ALLOWED_HOSTS | Нет          | Список разрешенных хостов для CORS        |

## Поддержка Functino Call

Адаптер поддерживает functino calling в формате, совместимом с OpenAI API, позволяя моделям GigaChat вызывать
определенные инструменты с параметрами. Это полезно для интеграции с внешними API, базами данных или пользовательской
логикой.

### Пример использования:

```json
{
  "model": "GigaChat",
  "messages": [
    {
      "role": "user",
      "content": "What's the weather like in Moscow?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city name"
            }
          },
          "required": [
            "location"
          ]
        }
      }
    }
  ],
  "tool_choice": "auto"
}
```

### Формат ответа:

```json
{
  "choices": [
    {
      "message": {
        "content": "",
        "role": "assistant",
        "tool_calls": [
          {
            "id": "call_123",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": {
                "location": "Moscow"
              }
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

Подробное описание tool calling доступно
в [документации](https://developers.sber.ru/docs/ru/gigachat/guides/functions/overview).

# Development

## Quick Start development

```bash
# Clone repository
git clone https://github.com/your-username/gigachat-adapter
cd gigachat-adapter

# Install dependencies
uv sync
```

### Configuration

1. Создайте файл `.env` в корне проекта
2. Добавьте обязательные переменные окружения:

```
BEARER_TOKEN=your_token
GIGACHAT_CREDENTIALS=your_gigachat_credentials
```

3. Local development:

```bash
uv run fastapi dev src/main.py
```

Swagger документация доступна по адресу: http://localhost:8000/docs

### Ручная сборка docker-образа

Build and run with Docker:

```bash
docker build -t gigachat-adapter .

docker run -p 8000:8000 \
  -e BEARER_TOKEN=your_token \
  -e GIGACHAT_CREDENTIALS=your_credentials \
  -e GIGACHAT_VERIFY_SSL_CERTS=false \
  gigachat-adapter
```

### Testing

```bash
pytest .
```

### Code Quality

```bash
ruff check
mypy .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
