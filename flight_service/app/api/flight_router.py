from fastapi import APIRouter, Depends
from flight_service.app.database import SessionLocal
from datetime import date, timedelta
from typing import List
from sqlalchemy import extract
from sqlalchemy.orm import Session
from flight_service.app.schema import FlightSchema
from flight_service.app.servcies.flight_service import fetch_flights, extract_months, save_flights_to_database, update_records
from datetime import datetime
from flight_service.app.models import Flight

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/flights/", response_model=List[FlightSchema])
def search(departure: str, destination: str, date_start: date, date_end: date,
           db: Session = Depends(get_db)):
    year_months_to_check = extract_months(date_start, date_end)
    for year, month in year_months_to_check:
        existing_flight = db.query(Flight).filter(
            Flight.departure == departure,
            Flight.destination == destination,
            extract('month', Flight.date) == month,
            extract('year', Flight.date) == year
        ).first()
        if existing_flight and (datetime.utcnow() - existing_flight.update_data) > timedelta(hours=12):
            flights = fetch_flights(departure, destination, month, year)
            update_records(flights, db)
        elif not existing_flight:
            flights = fetch_flights(departure, destination, month, year)
            save_flights_to_database(flights, db)

    flights = db.query(Flight).filter(
        Flight.departure == departure,
        Flight.destination == destination,
        Flight.date >= date_start,
        Flight.date <= date_end,
    ).all()
    return flights
