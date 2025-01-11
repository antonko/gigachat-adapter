from fastapi import status
from pytest_httpx import HTTPXMock


def test_liveness(client):
    """Test liveness endpoint returns 200 and correct version"""
    response = client.get("/health/liveness")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert isinstance(data["version"], str)


def test_readiness(client, httpx_mock: HTTPXMock):
    """Test readiness endpoint returns 200 when GigaChat API is available"""
    # Mock GigaChat models API call
    httpx_mock.add_response(
        json={
            "data": [
                {
                    "id": "GigaChat",
                    "object": "model",
                    "owned_by": "salutedevices",
                    "created": 1735689600,
                }
            ],
            "object": "list",
        },
        url="https://gigachat.devices.sberbank.ru/api/v1/models",
    )

    response = client.get("/health/readiness")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert isinstance(data["version"], str)


def test_readiness_failure(client, httpx_mock: HTTPXMock):
    """Test readiness endpoint returns 500 when GigaChat API is unavailable"""
    # Mock GigaChat models API call failure
    httpx_mock.add_response(
        status_code=500,
        url="https://gigachat.devices.sberbank.ru/api/v1/models",
    )

    response = client.get("/health/readiness")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["error"]["type"] == "http"
    assert data["error"]["code"] == "HTTP_EXCEPTION"
