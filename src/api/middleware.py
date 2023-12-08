from http import HTTPStatus
import os
from fastapi import HTTPException, Request

API_KEYS = os.environ.get("API_KEYS")


async def verify_api_key(request: Request):
    header_api_key = request.headers.get("x-api-key")
    if header_api_key in API_KEYS:
        return header_api_key

    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
