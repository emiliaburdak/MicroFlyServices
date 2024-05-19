from fastapi import FastAPI
from user_service.app import models
from user_service.app.database import engine
from user_service.app.api.authentication_router import router as authentication_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication_router)
