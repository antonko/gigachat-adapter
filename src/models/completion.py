from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class MessagesRole(str, Enum):
    """Роль автора сообщения"""

    ASSISTANT = "assistant"
    SYSTEM = "system"
    USER = "user"
    FUNCTION = "function"
    SEARCH_RESULT = "search_result"
    FUNCTION_IN_PROGRESS = "function_in_progress"


class ContentType(str, Enum):
    """Type of content in the message"""

    TEXT = "text"
    IMAGE_URL = "image_url"
    INPUT_AUDIO = "input_audio"


class ChatCompletionRequestMessageContentAudioInput(BaseModel):
    data: str = Field(..., description="Base64 encoded audio data.")
    format: str = Field(..., description="The format of the encoded audio data.")


class ChatCompletionRequestMessageContentAudio(BaseModel):
    type: ContentType = Field(
        ContentType.INPUT_AUDIO, description="The type of the content part."
    )
    input_audio: ChatCompletionRequestMessageContentAudioInput = Field(
        ..., description="The audio content."
    )


class ChatCompletionRequestMessageContentImageUrl(BaseModel):
    url: str = Field(
        ..., description="Either a URL of the image or the base64 encoded image data."
    )


class ChatCompletionRequestMessageContentImage(BaseModel):
    type: ContentType = Field(
        ContentType.IMAGE_URL, description="The type of the content part."
    )
    image_url: ChatCompletionRequestMessageContentImageUrl = Field(
        ..., description="The image content."
    )


class ChatCompletionRequestMessageContentText(BaseModel):
    type: ContentType = Field(
        ContentType.TEXT, description="The type of the content part."
    )
    text: str = Field(..., description="The text content.")


ChatCompletionRequestMessageContent = Union[
    ChatCompletionRequestMessageContentText,
    ChatCompletionRequestMessageContentImage | ChatCompletionRequestMessageContentAudio,
]


class ChatCompletionRequestMessage(BaseModel):
    content: str | List[ChatCompletionRequestMessageContent] = Field(
        ...,
        description="The content of the message, which is the user's input.",
    )
    role: MessagesRole = Field(
        ..., description="The role of the message, which is always 'user'."
    )


class ToolParameters(BaseModel):
    """Parameters for a tool"""

    type: str = Field("object", description="The type of the parameters object")
    properties: Optional[Dict[str, Any]] = Field(
        None, description="The properties of the parameters"
    )
    required: Optional[List[str]] = Field(None, description="Required parameter names")


class Tool(BaseModel):
    """A tool that can be called by the model (OpenAI format)"""

    type: str = Field("function", description="The type of the tool, always 'function'")
    function: Dict[str, Any] = Field(..., description="The function definition")


class Function(BaseModel):
    """A function that can be called by the model (GigaChat format)"""

    name: str = Field(..., description="The name of the function")
    description: Optional[str] = Field(
        None, description="A description of what the function does"
    )
    parameters: Optional[ToolParameters] = Field(
        None, description="The parameters the function accepts"
    )


class ChatCompletionRequest(BaseModel):
    model: str = Field(
        "GigaChat",
        title="Model name",
        description="The name of the model to use for completion",
    )
    messages: List[ChatCompletionRequestMessage] = Field(
        ..., description="The user messages to use for completion"
    )
    temperature: float = Field(
        1.0, description="Sampling temperature, from 0.0 to 2.0."
    )
    stream: bool = Field(
        False,
        description="Whether to stream the completion or return the full response.",
    )
    tools: Optional[List[Tool]] = Field(
        None,
        description="A list of tools the model may generate JSON inputs for (OpenAI format)",
    )
    tool_choice: Optional[Union[str, Dict[str, str]]] = Field(
        None,
        description="Controls how the model responds to tool calls (OpenAI format)",
    )
    # GigaChat specific parameters
    max_tokens: Optional[int] = Field(
        None, description="Maximum number of tokens to generate"
    )
    max_results: Optional[int] = Field(
        1, description="Maximum number of results to return"
    )
    repetition_penalty: Optional[float] = Field(
        1.0, description="Repetition penalty, from 0.0 to 2.0"
    )
    top_p: Optional[float] = Field(None, description="Nucleus sampling parameter")
    top_k: Optional[int] = Field(None, description="Top-k sampling parameter")


class ToolCall(BaseModel):
    """A tool call made by the model (OpenAI format)"""

    id: str = Field(..., description="The ID of the tool call")
    type: str = Field(
        "function", description="The type of the tool call, always 'function'"
    )
    function: Dict[str, Any] = Field(..., description="The function call details")


class FunctionCall(BaseModel):
    """A function call made by the model (GigaChat format)"""

    name: str = Field(..., description="The name of the function to call")
    arguments: Optional[Dict[str, Any]] = Field(
        None, description="The arguments to call the function with"
    )


class ChatCompletionResponseMessage(BaseModel):
    content: str = Field(
        ..., description="The content of the message, which is the user's input."
    )
    role: MessagesRole = Field(
        ..., description="The role of the message, which is always 'user'."
    )
    refusal: str | None = Field(
        description="The role of the message, which is always 'user'."
    )
    tool_calls: Optional[List[ToolCall]] = Field(
        None, description="The tool calls made by the model (OpenAI format)"
    )


class PromptTokensDetails(BaseModel):
    cached_tokens: int = 0


class CompletionTokensDetails(BaseModel):
    reasoning_tokens: int = 0
    accepted_prediction_tokens: int = 0
    rejected_prediction_tokens: int = 0


class ChatCompletionResponseUsage(BaseModel):
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt.")
    completion_tokens: int = Field(..., description="Number of tokens generated.")
    total_tokens: int = Field(..., description="Total number of tokens.")
    prompt_tokens_details: PromptTokensDetails = Field(
        ..., description="Details about the prompt tokens."
    )

    completion_tokens_details: CompletionTokensDetails = Field(
        ..., description="Details about the completion tokens."
    )


class ChatCompletionResponseChoice(BaseModel):
    index: int = Field(
        ..., description="Position of this completion among the choices."
    )
    message: ChatCompletionResponseMessage = Field(
        ..., description="The generated message."
    )
    finish_reason: str = Field(..., description="Reason the completion ended.")


class ChatCompletionResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the chat completion.")
    object: str = Field("chat.completion", description='Always "chat.completion".')
    created: int = Field(..., description="Unix timestamp (in seconds) when created.")
    model: str = Field(..., description="Model used.")
    choices: List[ChatCompletionResponseChoice]
    usage: ChatCompletionResponseUsage
    service_tier: None = None
    system_fingerprint: str = Field(
        "None", description="Unique identifier for the completion."
    )


class ChatCompletionStreamResponseDelta(BaseModel):
    content: str | None = Field(None, description="The content of the message chunk")
    role: MessagesRole | None = Field(None, description="The role of the message")
    refusal: str | None = Field(None, description="Refusal reason if any")
    tool_calls: Optional[List[ToolCall]] = Field(
        None, description="The tool calls delta"
    )


class ChatCompletionStreamResponseChoice(BaseModel):
    index: int = Field(..., description="Index of this completion choice")
    delta: ChatCompletionStreamResponseDelta = Field(
        ..., description="The message delta"
    )
    finish_reason: str | None = Field(None, description="Reason for completion")


class ChatCompletionStreamResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for this completion")
    object: str = Field("chat.completion.chunk", description="Object type")
    created: int = Field(..., description="Unix timestamp of creation")
    model: str = Field(..., description="Model used")
    choices: List[ChatCompletionStreamResponseChoice]
