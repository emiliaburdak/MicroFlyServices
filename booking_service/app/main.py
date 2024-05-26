from fastapi import FastAPI
from . import models
from .api.booking_router_commands import router as command_router
from .api.booking_router_queris import router as query_router
from .database import engine
from .services.kafka_events_utils import kafka_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=kafka_router.lifespan_context)

app.include_router(command_router)
app.include_router(query_router)
app.include_router(kafka_router)
