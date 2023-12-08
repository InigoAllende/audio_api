from http import HTTPStatus

import pytest
from fastapi import Header, HTTPException

from api.middleware import verify_api_key
from config import settings


@pytest.mark.parametrize(
    "key",
    [
        None,
        "",
        "asdasdasd",
        1232,
        "123TEST_KEY",
        "TEST_KEY123",
        "123TEST_KEY321",
    ],
)
@pytest.mark.asyncio
async def test_verify_api_key_wrong_key(key):
    with pytest.raises(HTTPException) as excinfo:
        await verify_api_key(x_api_key=key)

    assert excinfo.value.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_verify_api_key_correct_key():
    assert len(settings.API_KEYS) > 0, "Make sure there are test api keys set"

    for key in settings.API_KEYS:
        result = await verify_api_key(key)
        assert result == key
