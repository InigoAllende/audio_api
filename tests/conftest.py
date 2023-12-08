import os
import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app

settings.API_KEYS = ["TEST_KEY", "TEST_KEY2"]
settings.STORAGE_PATH = os.path.join(os.getcwd(), "tests/audio_file_storage")


@pytest.fixture
def client():
    client = TestClient(app)
    return client
