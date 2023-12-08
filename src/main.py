from fastapi import FastAPI

from api.routes import audio, healthz

description = """
This service contains several endpoints to manage audio files that are described in this documentation.
To use all the endpoins within the '/audio' path an api key is required. Please be sure that your requests contain a valid api key.
"""

app = FastAPI(
    title="Audio procesing app",
    summary="This service allows for the upload, download and management of audio files",
    description=description,
)
app.include_router(audio.router)
app.include_router(healthz.router)
