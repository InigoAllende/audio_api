from http import HTTPStatus
import os
from fastapi import APIRouter, Response, UploadFile

from api.models import UploadRequest
from config import settings

router = APIRouter()


@router.get("/", response_class=Response)
async def health_check():
    return Response(status_code=HTTPStatus.OK, content="Healthy")


@router.post("/upload")
async def audio_upload(file: UploadFile):
    file_path = os.path.join(settings.STORAGE_PATH, file.filename)
    print(file.file.read())
    # os.write(file_path, file.file.read())
    # os.close(file_path)
    with open(file_path, 'w') as f:
        f.write(file.file.read())
    return Response(status_code=HTTPStatus.OK, content=file.filename)


@router.get("/{file_id}/download")
async def audio_upload():
    return Response(status_code=HTTPStatus.NOT_IMPLEMENTED)


@router.post("/{file_id}/adjust_volume")
async def audio_upload():
    return Response(status_code=HTTPStatus.NOT_IMPLEMENTED)
