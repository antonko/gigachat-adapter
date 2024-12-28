from fastapi import FastAPI

from .gigachat_service import gigachat_service
from .models import (
    ModelsResponse,
)


def get_application() -> FastAPI:
    app = FastAPI(
        title="GigaChat Adapter API",
        description="Коннектор к GigaChat API c использованием OpenAI",
    )

    @app.get("/v1/models", response_model=ModelsResponse)
    async def get_models():
        return gigachat_service.get_models()

    return app


app = get_application()
