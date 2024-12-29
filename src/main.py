from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import Field
from pydantic_settings import BaseSettings

from .gigachat_service import gigachat_service
from .models import ListModelsResponse


class AppSettings(BaseSettings):
    debug: bool = False
    environment: str = "production"
    bearer_token: str = Field(
        ...,
        description="Bearer token is required to authorize requests.",
    )
    cors_allowed_hosts: list[str] | None = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        extra = "allow"


def get_app_settings() -> AppSettings:
    return AppSettings()  # type: ignore


bearer_scheme = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    settings: AppSettings = Depends(get_app_settings),
):
    if (
        credentials.scheme.lower() != "bearer"
        or credentials.credentials != settings.bearer_token
    ):
        raise HTTPException(status_code=401, detail="Invalid or missing Bearer token")


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

    @app.get(
        "/v1/models",
        response_model=ListModelsResponse,
        dependencies=[Depends(verify_token)],
    )
    async def get_models():
        return gigachat_service.get_models()

    return app


app = get_application()
