from fastapi import FastAPI
from . import models
from .api.booking_router_commands import router as command_router
from .api.booking_router_queris import router as query_router
from .database import engine
from .services.kafka_events_utils import kafka_router
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=kafka_router.lifespan_context)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(command_router)
app.include_router(query_router)
app.include_router(kafka_router)
