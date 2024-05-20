from fastapi import FastAPI
from booking_service.app import models
from booking_service.app.database import engine
from booking_service.app.api.booking_router import router as flight_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(flight_router)
