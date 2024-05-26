from fastapi import FastAPI
from . import models
from .api.booking_router import router as flight_router
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(flight_router)
