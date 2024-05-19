from fastapi import FastAPI
from flight_service.app import models
from flight_service.app.database import engine
from flight_service.app.api.flight_router import router as flight_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(flight_router)
