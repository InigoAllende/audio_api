import os
from http import HTTPStatus

from fastapi import Header, HTTPException

from config import settings


async def verify_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key is None or str(x_api_key) != settings.API_KEY:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Invalid or missing API Key",
        )

    return x_api_key
