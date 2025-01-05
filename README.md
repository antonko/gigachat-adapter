# GigaChat OpenAI-Compatible Adapter

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Release](https://github.com/antonko/gigachat-adapter/actions/workflows/release.yml/badge.svg)](https://github.com/your-username/gigachat-adapter/actions/workflows/release.yml)

Adapter для использования GigaChat API через интерфейс совместимый с OpenAI API. Позволяет интегрировать GigaChat в приложения, разработанные для работы с OpenAI, с минимальными изменениями кода.

## Features

✨ Основные возможности:

- OpenAI-совместимый API интерфейс
- Поддержка chat/completions API с потоковой передачей сообщений
- Загрузка файлов
- Swagger документация
- Официальный Docker-образ

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

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

### Running

```bash
uv run fastapi dev src/main.py
```

Swagger документация доступна по адресу: http://localhost:8000/docs

## Docker Support

Build and run with Docker:

```bash
# Build image
docker build -t gigachat-adapter .

# Run container
docker run -p 8000:8000 \
  -e BEARER_TOKEN=your_token \
  -e GIGACHAT_CREDENTIALS=your_credentials \
  -e GIGACHAT_VERIFY_SSL_CERTS=false \
  gigachat-adapter
```

## Environment Variables

Below are the environment variables you can set in your .env file:

### GigaChat Settings

Параметры должны начинаться с `GIGACHAT_` и соответствовать параметрам GigaChat API.

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
| DEBUG              | Нет          | Режим отладки                             |
| ENVIRONMENT        | Нет          | Окружение (development/production)        |
| CORS_ALLOWED_HOSTS | Нет          | Список разрешенных хостов для CORS        |

## Development

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
