from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import Field
from pydantic_settings import BaseSettings

import src.gigachat_monkey_patch  # noqa: F401

from .gigachat_service import gigachat_service
from .models.completion import ChatCompletionRequest, ChatCompletionResponse
from .models.files import FilePurpose, FileUploadResponse
from .models.models import ListModelsResponse


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


async def stream_chat_completion(
    request: ChatCompletionRequest,
) -> AsyncGenerator[str, None]:
    async for chunk in gigachat_service.chat_stream(request):
        yield f"data: {chunk.model_dump_json()}\n\n"
    yield "data: [DONE]\n\n"


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
        return await gigachat_service.get_models()

    @app.post(
        "/v1/chat/completions",
        response_model=ChatCompletionResponse,
        dependencies=[Depends(verify_token)],
    )
    async def create_chat_completion(request: ChatCompletionRequest):
        if request.stream:
            return StreamingResponse(
                stream_chat_completion(request),
                media_type="text/event-stream",
            )
        return await gigachat_service.chat(request)

    @app.post("/files")
    async def upload_file(
        file: UploadFile,
        purpose: Annotated[FilePurpose, Form()],
    ) -> FileUploadResponse:
        if file.filename is None or file.content_type is None:
            raise HTTPException(status_code=400, detail="No file uploaded")
        uploaded = await gigachat_service.upload_file(
            filename=file.filename,
            file=file.file,
            content_type=file.content_type,
            purpose=purpose.value if purpose != FilePurpose.FINE_TUNE else "general",
        )

        return uploaded

    return app


app = get_application()
