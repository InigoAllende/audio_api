import io
import os
from http import HTTPStatus

from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile
from fastapi.responses import StreamingResponse
from pydub import AudioSegment

from api.middleware import verify_api_key
from api.models import VolumeAdjustRequest
from config import settings

FERNET = Fernet(settings.ENCRYPTION_KEY)

router = APIRouter(
    prefix="/audio",
    dependencies=[Depends(verify_api_key)],
    responses={403: {"Forbidden": HTTPStatus.UNAUTHORIZED}},
)


@router.post(
    "/upload",
    status_code=HTTPStatus.CREATED,
    response_class=Response,
    responses={415: {}},
)
async def audio_upload(file: UploadFile) -> Response:
    if file.content_type.split("/")[0] != "audio":
        raise HTTPException(status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    file_path = os.path.join(settings.STORAGE_PATH, file.filename)
    encrypted_file = FERNET.encrypt(file.file.read())
    with open(file_path, "wb") as f:
        f.write(encrypted_file)
    return Response(status_code=HTTPStatus.CREATED)


@router.get(
    "/{file_id}/download",
    responses={
        200: {
            "content": {"audio/*": {}},
            "description": "Success.",
        },
        404: {},
    },
    response_class=StreamingResponse,
)
async def audio_download(file_id: str):
    file_path = os.path.join(settings.STORAGE_PATH, file_id)
    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Audio file not found",
        )
    with open(file_path, "rb") as f:
        encrypted_file = f.read()
    decrypted_file = io.BytesIO(FERNET.decrypt(encrypted_file))
    return StreamingResponse(
        decrypted_file,
        media_type="audio/*",
        headers={"Content-Disposition": f"inline; filename={file_id}"},
    )


@router.put(
    "/{file_id}/adjust_volume",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        404: {},
    },
    response_class=Response,
    description="Please provide a value for the volume increase in decibels. \
    A positive value will increase the volumen whereas a negative one will decrease it. \
    This endpoint only updates the volume and does not download the file, to access the updated file, please use the download endpoint",
)
async def adjust_volume(file_id: str, request: VolumeAdjustRequest):
    file_path = os.path.join(settings.STORAGE_PATH, file_id)
    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Audio file not found",
        )
    with open(file_path, "rb") as f:
        encrypted_file = f.read()

    decrypted_file = FERNET.decrypt(encrypted_file)
    audio = AudioSegment.from_file_using_temporary_files(io.BytesIO(decrypted_file))
    audio += request.volume_increase
    encrypted_file = FERNET.encrypt(audio.export().read())
    with open(file_path, "wb") as f:
        f.write(encrypted_file)
    # audio = AudioSegment.from_file(file_path)
    # audio = audio + request.volume_increase
    # audio.export(file_path)
    return Response(status_code=HTTPStatus.NO_CONTENT)
