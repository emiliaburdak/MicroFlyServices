from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app import models, schema
from app.service.scrap_service import fetch_flights, extract_months, save_flights_to_database, update_records
from datetime import datetime

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
        flights = fetch_flights(departure, destination, month, year)
        if flights:
            db.add_all(flights)
            db.commit()
            return flights
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flight/")
def search(departure: str, destination: str, date_start: date, date_end: date,
           db: Session = Depends(get_db)):
    year_months_to_check = extract_months(date_start, date_end)
    for year_month in year_months_to_check:
        month = year_months_to_check[year_month][1]
        year = year_months_to_check[year_month][1]
        existing_flights = db.query(models.Flight).filter(
            models.Flight.departure == departure,
            models.Flight.destination == destination,
            models.Flight.date.month == year,
            models.Flight.date.year == month
        ).all()
        # może lepiej zronbić .first() po co sprawdzać czy są loty z całego miesiąca, wystarczy pierwszy skoro zawsze całe meisiące zapisuje
        if existing_flights and (existing_flights[0].update_data - datetime.utcnow().date()) > timedelta(hours=12):
            flights = fetch_flights(departure, destination, month, year)
            update_records(flights)
        else:
            flights = fetch_flights(departure, destination, month, year)
            save_flights_to_database(flights)

    flights = db.query(models.Flight).filter(
        models.Flight.departure == departure,
        models.Flight.destination == destination,
        models.Flight.date >= date_start,
        models.Flight.date <= date_end,
    ).all()
    return flights





