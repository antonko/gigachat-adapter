from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class MessagesRole(str, Enum):
    """Роль автора сообщения"""

    ASSISTANT = "assistant"
    SYSTEM = "system"
    USER = "user"
    FUNCTION = "function"
    SEARCH_RESULT = "search_result"
    FUNCTION_IN_PROGRESS = "function_in_progress"


class ChatCompletionRequestMessage(BaseModel):
    content: str = Field(
        ..., description="The content of the message, which is the user's input."
    )
    role: MessagesRole = Field(
        ..., description="The role of the message, which is always 'user'."
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
