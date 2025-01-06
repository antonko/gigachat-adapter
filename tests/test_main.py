from fastapi import status
from pytest_httpx import HTTPXMock

from .conftest import TEST_BEARER_TOKEN


def test_get_models(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={
            "data": [
                {
                    "id": "GigaChat",
                    "object": "model",
                    "owned_by": "salutedevices",
                    "created": 1735689600,
                },
                {
                    "id": "GigaChat-Max",
                    "object": "model",
                    "owned_by": "salutedevices",
                    "created": 1735689600,
                },
                {
                    "id": "GigaChat-Plus",
                    "object": "model",
                    "owned_by": "salutedevices",
                    "created": 1735689600,
                },
                {
                    "id": "GigaChat-Pro",
                    "object": "model",
                    "owned_by": "salutedevices",
                    "created": 1735689600,
                },
            ],
            "object": "list",
        },
        url="https://gigachat.devices.sberbank.ru/api/v1/models",
    )
    headers = {"Authorization": f"Bearer {TEST_BEARER_TOKEN}"}
    response = client.get("/v1/models", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["object"] == "list"
    assert len(data["data"]) == 4


def test_chat_completions(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={
            "choices": [
                {
                    "message": {
                        "content": "Вот какие варианты у меня получились",
                        "role": "assistant",
                    },
                    "index": 0,
                    "finish_reason": "stop",
                }
            ],
            "created": 1736023521,
            "model": "GigaChat:1.0.26.20",
            "object": "chat.completion",
            "usage": {"prompt_tokens": 32, "completion_tokens": 63, "total_tokens": 95},
        },
        url="https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        method="POST",
    )

    payload = {
        "model": "GigaChat",
        "stream": False,
        "update_interval": 0,
        "messages": [
            {"role": "system", "content": "Отвечай как научный сотрудник"},
            {
                "role": "user",
                "content": "Напиши 5 вариантов названий для космической станции",
            },
        ],
    }

    headers = {"Authorization": f"Bearer {TEST_BEARER_TOKEN}"}
    response = client.post("/v1/chat/completions", json=payload, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["choices"][0]["message"]["content"].startswith("Вот какие варианты")
    assert data["usage"]["prompt_tokens_details"]["cached_tokens"] == 0


def test_invalid_token(client):
    headers = {"Authorization": "Bearer 111"}
    response = client.get("/v1/models", headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["message"] == "Invalid or missing Bearer token"
    assert data["error"]["type"] == "http"
    assert data["error"]["param"] is None
    assert data["error"]["code"] == "HTTP_EXCEPTION"


def test_invalid_json(client):
    headers = {
        "Authorization": f"Bearer {TEST_BEARER_TOKEN}"
    }  # or a valid token if needed
    # Pass intentionally malformed JSON:
    response = client.post(
        "/v1/chat/completions", data="{'invalid_json': }", headers=headers
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["type"] == "invalid_request_error"
    assert data["error"]["code"] == "BAD_REQUEST"
    assert "'JSON decode error'" in data["error"]["message"]
