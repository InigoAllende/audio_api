import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app

settings.API_KEYS = ["TEST_KEY", "TEST_KEY2"]


@pytest.fixture
def client():
    client = TestClient(app)
    return client
