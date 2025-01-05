from typing import AsyncIterator, Optional

import gigachat.api.stream_chat
import httpx
from gigachat.models import Chat, ChatCompletionChunk


async def asyncio(
    client: httpx.AsyncClient,
    *,
    chat: Chat,
    access_token: Optional[str] = None,
) -> AsyncIterator[ChatCompletionChunk]:
    kwargs = gigachat.api.stream_chat._get_kwargs(chat=chat, access_token=access_token)
    async with client.stream(**kwargs) as response:
        await gigachat.api.stream_chat._acheck_response(response)
        async for line in response.aiter_lines():
            if chunk := gigachat.api.stream_chat.parse_chunk(line, ChatCompletionChunk):
                yield chunk


gigachat.api.stream_chat.asyncio = asyncio
