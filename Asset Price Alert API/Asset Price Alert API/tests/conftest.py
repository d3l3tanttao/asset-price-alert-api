from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def unique_email() -> str:
    return f"user-{uuid4()}@example.com"


@pytest.fixture
def test_password() -> str:
    return "strongpassword"