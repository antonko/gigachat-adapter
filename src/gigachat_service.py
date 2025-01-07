import logging
import uuid
from typing import AsyncGenerator, AsyncIterator, BinaryIO

from gigachat import GigaChat
from gigachat.models.chat import Chat, Messages
from gigachat.models.chat_completion import ChatCompletion
from gigachat.models.messages_role import MessagesRole as GigaChatMessagesRole
from pydantic_settings import BaseSettings

from .models.completion import (
    ChatCompletionRequest,
    ChatCompletionRequestMessageContentAudio,
    ChatCompletionRequestMessageContentImage,
    ChatCompletionRequestMessageContentText,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatCompletionResponseMessage,
    ChatCompletionResponseUsage,
    ChatCompletionStreamResponse,
    ChatCompletionStreamResponseChoice,
    ChatCompletionStreamResponseDelta,
    CompletionTokensDetails,
    MessagesRole,
    PromptTokensDetails,
)
from .models.files import FilePurpose, FileUploadResponse
from .models.models import ListModelsResponse, ModelData

_logger = logging.getLogger(__name__)


class GigaChatSettings(BaseSettings):
    base_url: str | None = None
    auth_url: str | None = None
    credentials: str | None = None
    scope: str | None = None
    access_token: str | None = None
    model: str | None = None
    profanity_check: bool | None = None
    user: str | None = None
    password: str | None = None
    timeout: int | None = None
    verify_ssl_certs: bool | None = None
    verbose: bool | None = None
    ca_bundle_file: str | None = None
    cert_file: str | None = None
    key_file: str | None = None
    key_file_password: str | None = None

    class Config:
        env_file = ".env"
        env_prefix = "GIGACHAT_"
        extra = "allow"


class GigaChatService:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._settings = GigaChatSettings(**kwargs)
        self._client = GigaChat(
            base_url=self._settings.base_url,
            auth_url=self._settings.auth_url,
            credentials=self._settings.credentials,
            scope=self._settings.scope,
            access_token=self._settings.access_token,
            model=self._settings.model,
            profanity_check=self._settings.profanity_check,
            user=self._settings.user,
            password=self._settings.password,
            timeout=self._settings.timeout,
            verify_ssl_certs=self._settings.verify_ssl_certs,
            verbose=self._settings.verbose,
            ca_bundle_file=self._settings.ca_bundle_file,
            cert_file=self._settings.cert_file,
            key_file=self._settings.key_file,
            key_file_password=self._settings.key_file_password,
        )

    async def initialize(self):
        await self._client.aget_token()

    async def get_models(self) -> ListModelsResponse:
        raw_models = await self._client.aget_models()
        data = [
            ModelData(
                id=m.id_, object=m.object_, owned_by=m.owned_by, created=1735689600
            )
            for m in raw_models.data
        ]
        return ListModelsResponse(data=data, object="list")

    def _create_gigachat_request(self, request: ChatCompletionRequest) -> Chat:
        # Конвертируем запрос от пользователя в формат, который понимает GigaChat
        messages: list[Messages] = []
        for message in request.messages:
            if isinstance(message.content, str):
                # Если контент - строка, то просто добавляем его в список сообщений
                messages.append(
                    Messages(
                        role=GigaChatMessagesRole(message.role), content=message.content
                    )
                )
            elif isinstance(message.content, list):
                # Если контент - список, то обрабатываем каждый элемент
                for content_item in message.content:
                    match content_item:
                        case ChatCompletionRequestMessageContentText():
                            # Если контент - текст
                            messages.append(
                                Messages(
                                    role=GigaChatMessagesRole(message.role),
                                    content=content_item.text,
                                )
                            )
                        case ChatCompletionRequestMessageContentImage():
                            # Если контент - изображение
                            _logger.warning(
                                "Image content is not supported by GigaChat Adapter"
                            )
                        case ChatCompletionRequestMessageContentAudio():
                            # Если контент - аудио
                            _logger.warning(
                                "Audio content is not supported by GigaChat Adapter"
                            )
                        case _:
                            _logger.warning(
                                "Unknown content type %s", type(content_item)
                            )

        return Chat(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            stream=request.stream,
        )

    def _map_finish_reason(self, finish_reason: str | None) -> str:
        # Конвертируем причину завершения чата из формата GigaChat в формат API
        if finish_reason == "blacklist":
            return "content_filter"
        elif finish_reason == "function_call":
            return "tool_calls"
        elif finish_reason == "error":
            return "stop"
        return finish_reason or "stop"

    async def chat(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        chat_completion: ChatCompletion = await self._client.achat(
            self._create_gigachat_request(request)
        )
        return ChatCompletionResponse(
            id=str(uuid.uuid4()),
            object="chat.completion",
            created=chat_completion.created,
            model=chat_completion.model,
            choices=[
                ChatCompletionResponseChoice(
                    index=c.index,
                    message=ChatCompletionResponseMessage(
                        role=MessagesRole(c.message.role),
                        content=c.message.content,
                        refusal=None,
                    ),
                    finish_reason=self._map_finish_reason(c.finish_reason),
                )
                for c in chat_completion.choices
            ],
            usage=ChatCompletionResponseUsage(
                prompt_tokens=chat_completion.usage.prompt_tokens,
                completion_tokens=chat_completion.usage.completion_tokens,
                total_tokens=chat_completion.usage.total_tokens,
                prompt_tokens_details=PromptTokensDetails(),
                completion_tokens_details=CompletionTokensDetails(),
            ),
            service_tier=None,
            system_fingerprint="None",
        )

    async def stream_chat(
        self, request: ChatCompletionRequest
    ) -> AsyncIterator[ChatCompletionStreamResponse]:
        async for chunk in self._client.astream(self._create_gigachat_request(request)):
            yield ChatCompletionStreamResponse(
                id=str(uuid.uuid4()),
                object="chat.completion.chunk",
                created=chunk.created,
                model=chunk.model,
                choices=[
                    ChatCompletionStreamResponseChoice(
                        index=c.index,
                        delta=ChatCompletionStreamResponseDelta(
                            role=MessagesRole(c.delta.role) if c.delta.role else None,
                            content=c.delta.content,
                            refusal=None,
                        ),
                        finish_reason=self._map_finish_reason(c.finish_reason),
                    )
                    for c in chunk.choices
                ],
            )

    async def upload_file(
        self, filename: str, file: BinaryIO, content_type: str, purpose: str
    ) -> FileUploadResponse:
        fule_upload = await self._client.aupload_file(
            (filename, file, content_type), purpose=purpose
        )
        result: FileUploadResponse = FileUploadResponse(
            id=fule_upload.id_,
            object="file",
            bytes=fule_upload.bytes_,
            created_at=fule_upload.created_at,
            filename=fule_upload.filename,
            purpose=FilePurpose(purpose),
        )
        return result

    async def stream_chat_sse(
        self,
        request: ChatCompletionRequest,
    ) -> AsyncGenerator[str, None]:
        # Стримим результаты чата в формате Server-Sent Events
        async for chunk in self.stream_chat(request):
            yield f"data: {chunk.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"


gigachat_service: GigaChatService = GigaChatService()
