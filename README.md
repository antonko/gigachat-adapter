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

## Testing

```bash
pytest .
```

## Lint and format

```bash
ruff check
mypy .
```
