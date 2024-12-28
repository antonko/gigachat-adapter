from fastapi import status


def test_get_models(client, httpx_mock):
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
        }
    )
    response = client.get("/v1/models")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["object"] == "list"
    assert len(data["data"]) == 4
