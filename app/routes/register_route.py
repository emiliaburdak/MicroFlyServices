from fastapi import APIRouter
from app.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/hello")
async def read_hello():
    return {"message": "Hello, dupa ruta!"}