from fastapi import FastAPI
from . import models
from .database import engine
from .api.flight_router import router as flight_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(flight_router)
