from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer

from .core.logging import local_logger
from .core.settings import AppSettings, get_app_settings
from .core.verify_token import verify_token
from .gigachat_service import gigachat_service
from .models.completion import ChatCompletionRequest, ChatCompletionResponse
from .models.files import FilePurpose, FileUploadResponse
from .models.health import HealthResponse
from .models.models import ListModelsResponse

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.get(
    "/v1/models",
    response_model=ListModelsResponse,
    dependencies=[Depends(verify_token)],
)
async def get_models():
    return await gigachat_service.get_models()


@router.post(
    "/v1/chat/completions",
    response_model=ChatCompletionResponse,
    dependencies=[Depends(verify_token)],
)
async def create_chat_completion(request: ChatCompletionRequest):
    local_logger.debug(
        f"api request chat/completions: {request.model_dump_json(indent=2)}"
    )
    if request.stream:
        # Необходимо для корректных ответов если GigaChat
        # возвращает ошибку, иначе мы уже начали стримить ответ

        stream = gigachat_service.stream_chat_sse(request)
        first_chunk = await anext(stream)

        async def streaming_generator():
            yield first_chunk
            async for chunk in stream:
                yield chunk

        return StreamingResponse(
            streaming_generator(),
            media_type="text/event-stream",
        )
    return await gigachat_service.chat(request)


@router.post("/files")
async def upload_file(
    file: UploadFile, purpose: FilePurpose = Form(...)
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


@router.get("/health/liveness", response_model=HealthResponse)
async def liveness(settings: AppSettings = Depends(get_app_settings)) -> HealthResponse:
    """
    Liveness probe для kubernetes.
    Проверяет что сервис жив и отвечает на запросы.
    """
    return HealthResponse(status="ok", version=settings.version)


@router.get("/health/readiness", response_model=HealthResponse)
async def readiness(
    settings: AppSettings = Depends(get_app_settings),
) -> HealthResponse:
    """
    Readiness probe для kubernetes.
    Проверяет что сервис готов обрабатывать запросы,
    включая проверку подключения к GigaChat API.
    """
    await gigachat_service.get_models()
    return HealthResponse(status="ok", version=settings.version)
