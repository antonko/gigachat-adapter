import base64
import hashlib
import logging
import mimetypes
import uuid
from io import BytesIO
from typing import AsyncGenerator, AsyncIterator, BinaryIO, Dict, Union

from gigachat import GigaChat
from gigachat.models.chat import Chat, Messages
from gigachat.models.chat_completion import ChatCompletion
from gigachat.models.chat_function_call import ChatFunctionCall
from gigachat.models.function import Function as GigaChatFunction
from gigachat.models.messages_role import MessagesRole as GigaChatMessagesRole
from pydantic_settings import BaseSettings

from .core.kv_store import KVStore
from .core.logging import local_logger
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
    Tool,
    ToolCall,
)
from .models.files import FilePurpose, FileUploadResponse
from .models.models import ListModelsResponse, ModelData


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

    async def _upload_base64(self, base64_data: str) -> uuid.UUID:
        # Проверяем наличие файла в хранилище
        key = hashlib.sha256(base64_data.encode()).hexdigest()
        kv_store = KVStore()
        existing_id = await kv_store.get(key)
        if existing_id:
            return uuid.UUID(existing_id)

        # Загружаем изображение в GigaChat
        header, encoded = base64_data.split(",", 1)
        data = base64.b64decode(encoded)
        mime_type = header.split(":")[1].split(";")[0]
        extension = mimetypes.guess_extension(mime_type)
        filename = f"upload_{uuid.uuid4()}{extension}"
        file = BytesIO(data)

        local_logger.debug(f"Uploading file {filename} with mime type {mime_type}")

        file_upload_response = await self._client.aupload_file(
            (filename, file, mime_type), purpose="general"
        )

        # Сохраняем данные в хранилище
        await kv_store.set(key, str(file_upload_response.id_))

        return file_upload_response.id_

    def _convert_tool_to_gigachat_function(self, tool: Tool) -> GigaChatFunction:
        """Convert OpenAI Tool format to GigaChat Function format"""
        function_data = tool.function
        return GigaChatFunction(
            name=function_data.get("name", ""),
            description=function_data.get("description"),
            parameters=function_data.get("parameters"),
        )

    def _convert_tool_choice_to_gigachat_function_call(
        self, tool_choice: Union[str, Dict[str, str]]
    ) -> ChatFunctionCall | str | None:
        """Convert tool_choice parameter to GigaChat function_call format"""
        if isinstance(tool_choice, str):
            return tool_choice
        elif isinstance(tool_choice, dict):
            return ChatFunctionCall(
                name=tool_choice.get("name", ""),
                partial_arguments=tool_choice.get("partial_arguments"),
            )
        return None

    async def _create_gigachat_request(self, request: ChatCompletionRequest) -> Chat:
        messages: list[Messages] = []
        for message in request.messages:
            messages.extend(await self._process_message(message))

        # Convert tools to GigaChat functions format
        functions = None
        if request.tools:
            functions = [
                self._convert_tool_to_gigachat_function(t) for t in request.tools
            ]

        # Convert tool_choice to GigaChat function_call format
        function_call = None
        if request.tool_choice:
            function_call = self._convert_tool_choice_to_gigachat_function_call(
                request.tool_choice
            )

        result: Chat = Chat(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            stream=request.stream,
            functions=functions,
            function_call=function_call,
        )
        local_logger.debug(
            f"gigachat request: {result.json(by_alias=True, indent=2, ensure_ascii=False)}"
        )
        return result

    async def _process_message(self, message) -> list[Messages]:
        # Обрабатываем сообщение и возвращаем список сообщений
        if isinstance(message.content, str):
            return [self._create_text_message(message.role, message.content)]
        elif isinstance(message.content, list):
            return await self._process_message_content_list(
                message.role, message.content
            )
        return []

    def _create_text_message(self, role, content) -> Messages:
        # Создаем текстовое сообщение
        return Messages(role=GigaChatMessagesRole(role), content=content)

    async def _process_message_content_list(self, role, content_list) -> list[Messages]:
        # Обрабатываем список контента сообщения
        messages = []
        for content_item in content_list:
            message = await self._process_content_item(role, content_item)
            if message:
                messages.append(message)
        return messages

    async def _process_content_item(self, role, content_item) -> Messages | None:
        # Обрабатываем элемент контента сообщения
        match content_item:
            case ChatCompletionRequestMessageContentText():
                return self._create_text_message(role, content_item.text)
            case ChatCompletionRequestMessageContentImage():
                return await self._create_image_message(
                    role, content_item.image_url.url
                )
            case ChatCompletionRequestMessageContentAudio():
                local_logger.warning(
                    "Audio content is not supported by GigaChat Adapter"
                )
            case _:
                local_logger.warning("Unknown content type %s", type(content_item))
        return None

    async def _create_image_message(self, role, image_url) -> Messages:
        # Создаем сообщение с изображением
        attachment_id = await self._upload_base64(image_url)
        return Messages(
            role=GigaChatMessagesRole(role),
            attachments=[str(attachment_id)],
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

    def _convert_gigachat_function_call_to_tool_call(
        self, gigachat_function_call
    ) -> ToolCall | None:
        """Convert GigaChat FunctionCall to OpenAI ToolCall format"""
        if gigachat_function_call:
            return ToolCall(
                id=str(uuid.uuid4()),
                type="function",
                function={
                    "name": gigachat_function_call.name,
                    "arguments": gigachat_function_call.arguments or {},
                },
            )
        return None

    def _get_tool_calls_from_function_call(
        self, gigachat_function_call: ChatFunctionCall | None
    ) -> list[ToolCall] | None:
        """Convert GigaChat FunctionCall to OpenAI ToolCall format"""
        if gigachat_function_call:
            tool_call = self._convert_gigachat_function_call_to_tool_call(
                gigachat_function_call
            )
            if tool_call:
                return [tool_call]
        return None

    def _get_tool_calls_from_function_call_stream(
        self, gigachat_function_call: ChatFunctionCall | None
    ) -> list[ToolCall] | None:
        """Convert GigaChat FunctionCall to OpenAI ToolCall format for streaming"""
        if gigachat_function_call:
            tool_call = self._convert_gigachat_function_call_to_tool_call(
                gigachat_function_call
            )
            if tool_call:
                return [tool_call]
        return None

    async def chat(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        chat_completion: ChatCompletion = await self._client.achat(
            await self._create_gigachat_request(request)
        )
        local_logger.debug(
            f"gigachat response: {chat_completion.json(by_alias=True, indent=2, ensure_ascii=False)}"
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
                        tool_calls=self._get_tool_calls_from_function_call(
                            c.message.function_call
                        ),
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
        async for chunk in self._client.astream(
            await self._create_gigachat_request(request)
        ):
            local_logger.debug(
                f"gigachat response: {chunk.json(by_alias=True, indent=2, ensure_ascii=False)}"
            )
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
                            tool_calls=self._get_tool_calls_from_function_call_stream(
                                c.delta.function_call
                            )
                            if hasattr(c.delta, "function_call")
                            else None,
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
