# GigaChat OpenAI-Compatible Adapter

Этот проект предоставляет минимальный сервис, который эмулирует поведение **OpenAI API** и под капотом перенаправляет запросы в **GigaChat API** от Сбера.

# Возможности

- **/v1/models** – возвращает список доступных моделей.

# Документация

- Документация доступна по адресу http://localhost:8000/docs

# Development

```
fastapi dev src/main.py
```

## Environment Variables

Below are the environment variables you can set in your .env file:

### GigaChat Settings (env*prefix = "GIGACHAT*")

- GIGACHAT_BASE_URL
- GIGACHAT_AUTH_URL
- GIGACHAT_CREDENTIALS
- GIGACHAT_SCOPE
- GIGACHAT_ACCESS_TOKEN
- GIGACHAT_MODEL
- GIGACHAT_PROFANITY_CHECK
- GIGACHAT_USER
- GIGACHAT_PASSWORD
- GIGACHAT_TIMEOUT
- GIGACHAT_VERIFY_SSL_CERTS
- GIGACHAT_VERBOSE
- GIGACHAT_CA_BUNDLE_FILE
- GIGACHAT_CERT_FILE
- GIGACHAT_KEY_FILE
- GIGACHAT_KEY_FILE_PASSWORD

### Application Settings

- BEARER_TOKEN (Required)
- DEBUG
- ENVIRONMENT
- CORS_ALLOWED_HOSTS

## Testing

```bash
pytest .
```

## Lint and format

```bash
ruff check
mypy .
```
