# GigaChat OpenAI-Compatible Adapter

[![Build](https://github.com/antonko/gigachat-adapter/actions/workflows/release.yml/badge.svg)](https://github.com/antonko/gigachat-adapter/actions/workflows/release.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/antonk0/gigachat-adapter)](https://hub.docker.com/r/antonk0/gigachat-adapter)

Адаптер предоставляет доступ к GigaChat API через интерфейс, совместимый с OpenAI API, позволяя интегрировать GigaChat в приложения, изначально ориентированные на OpenAI, с минимальными изменениями кода.

Изначально проект был создан для подключения к сервису Open WebUI. На текущий момент реализована базовая работа с GigaChat через метод `chat/completions` с поддержкой файлов в сообщениях. Таких возможности как embeddings и т.д будут реализованы по мере необходимости.

## Features

✨ Основные возможности:

- На основе официальной библиотеки [gigachat](https://github.com/ai-forever/gigachat)
- Поддержка `chat/completions` API с потоковой передачей сообщений
- Поддержка файлов в сообщениях исключая повторные загрузки в GigaChat
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

## Environment Variables

Below are the environment variables you can set in your .env file:

### GigaChat Settings

Параметры библиотеки [gigachat](https://github.com/ai-forever/gigachat). Параметры должны начинаться с `GIGACHAT_` и соответствовать параметрам GigaChat API.

| Параметр          | Обязательный | Описание                                                           |
| ----------------- | ------------ | ------------------------------------------------------------------ |
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
| ------------------ | ------------ | ----------------------------------------- |
| BEARER_TOKEN       | Да           | Токен для авторизации запросов к адаптеру |
| DEBUG              | Нет          | Режим отладки, подробные логи             |
| ENVIRONMENT        | Нет          | Окружение (development/production)        |
| CORS_ALLOWED_HOSTS | Нет          | Список разрешенных хостов для CORS        |

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

2. Local development:

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
