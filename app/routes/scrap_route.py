from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app import models, schema
from app.service.scrap_service import fetch_flights_from_external_api

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/flights/", response_model=List[schema.FlightSchema])
def search_flights(departure: str, destination: str, date_start: date, date_end: date,
                   db: Session = Depends(get_db)):
    existing_flights = db.query(models.Flight).filter(
        models.Flight.departure == departure,
        models.Flight.destination == destination,
        models.Flight.date >= date_start,
        models.Flight.date <= date_end,
    ).all()

    if existing_flights:
        return existing_flights

    try:
        flights = fetch_flights_from_external_api(departure, destination, date_start, date_end)
        if flights:
            db.add_all(flights)
            db.commit()
            return flights
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
