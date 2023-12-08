from fastapi import FastAPI
from api.routes.audio import router

app = FastAPI()

app.include_router(router)
