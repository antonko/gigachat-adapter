from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.core.gigachat_monkey_patch  # noqa: F401

from .core.settings import get_app_settings
from .endpoints import router


def get_application() -> FastAPI:
    settings = get_app_settings()
    app = FastAPI(
        title="GigaChat Adapter API",
        description="Connector to GigaChat API using OpenAI",
        debug=settings.debug,
        cors_allowed_origins=settings.cors_allowed_hosts,
    )

    if settings.cors_allowed_hosts:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allowed_hosts,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(router)

    return app


app = get_application()
