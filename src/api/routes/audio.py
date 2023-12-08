from http import HTTPStatus
import os
from fastapi import APIRouter, Depends, Response, UploadFile
from fastapi.responses import FileResponse
from pydub import AudioSegment
from api.middleware import verify_api_key
from api.models import VolumeAdjustRequest
from config import settings

router = APIRouter(prefix="/audio", dependencies=[Depends(verify_api_key)])


@router.post("/upload", dependencies=[Depends(verify_api_key)])
async def audio_upload(file: UploadFile):
    # TODO: Create subfolders per user
    file_path = os.path.join(settings.STORAGE_PATH, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return Response(status_code=HTTPStatus.OK, content=file.filename)


@router.get("/{file_id}/download", dependencies=[Depends(verify_api_key)])
async def audio_upload(file_id: str):
    file_path = os.path.join(settings.STORAGE_PATH, file_id)
    if not os.path.isfile(file_path):
        return Response(status_code=HTTPStatus.NOT_FOUND)
    return FileResponse(file_path)


@router.post("/{file_id}/adjust_volume", dependencies=[Depends(verify_api_key)])
async def audio_upload(file_id: str, request: VolumeAdjustRequest):
    file_path = os.path.join(settings.STORAGE_PATH, file_id)
    if not os.path.isfile(file_path):
        return Response(status_code=HTTPStatus.NOT_FOUND)
    audio = AudioSegment.from_file(file_path)
    audio = audio + request.volume_increase
    audio.export(file_path)
    return Response(status_code=HTTPStatus.OK)
