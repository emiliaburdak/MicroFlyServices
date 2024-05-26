from fastapi import FastAPI
from . import models
from .database import engine
from .api.authentication_router import router as authentication_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication_router)
