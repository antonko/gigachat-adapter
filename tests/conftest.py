import os
import time
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

TEST_BEARER_TOKEN = "test_token"
os.environ["BEARER_TOKEN"] = TEST_BEARER_TOKEN
os.environ["GIGACHAT_CREDENTIALS"] = "test_credentials"
os.environ["DEBUG"] = "false"


from src.main import get_application  # noqa: E402


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    app = get_application()
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
@pytest.mark.httpx_mock(assert_all_responses_were_requested=True)
def mock_oauth(httpx_mock: HTTPXMock):
    """Mock OAuth token request for all tests"""
    httpx_mock.add_response(
        method="POST",
        url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        json={
            "access_token": "mock_access_token",
            "expires_at": int(time.time()) + 3600,
        },
        is_optional=True,
    )
