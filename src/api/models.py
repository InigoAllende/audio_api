from fastapi import UploadFile, File
from pydantic import BaseModel

class UploadRequest(BaseModel):
    audio_file: UploadFile
    file_id: str