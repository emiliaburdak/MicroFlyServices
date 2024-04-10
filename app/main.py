from fastapi import FastAPI
from app import models
from .database import engine

from app.routes.register_route import router as register_route
from app.routes.scrap_route import router as scrap_route


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(register_route)
app.include_router(scrap_route)
