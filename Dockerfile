FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.5.13 /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  UV_HTTP_TIMEOUT=120 uv sync --frozen --no-install-project --no-editable

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
  UV_HTTP_TIMEOUT=120 uv sync --frozen --no-editable

FROM python:3.12-slim

RUN useradd -ms /bin/bash app
USER app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app /app

EXPOSE 8000

CMD ["/app/.venv/bin/fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "src/main.py"]