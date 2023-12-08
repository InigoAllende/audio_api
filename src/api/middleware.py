import os
from http import HTTPStatus

from fastapi import HTTPException, Header, Request

API_KEYS = os.environ.get("API_KEYS")


async def verify_api_key(x_api_key: str = Header(...)):
    header_api_key = x_api_key
    if header_api_key in API_KEYS:
        return header_api_key

    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail="Invalid or missing API Key",
    )
