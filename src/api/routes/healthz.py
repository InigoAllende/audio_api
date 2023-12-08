
from http import HTTPStatus
from fastapi import APIRouter, Response


router = APIRouter(prefix="/healthz")

@router.get("/", response_class=Response)
async def health_check():
    return Response(status_code=HTTPStatus.OK, content="Healthy")

