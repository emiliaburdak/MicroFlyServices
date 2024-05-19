from typing import List
import requests
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database import SessionLocal
from app.models import Flight
from datetime import datetime, date
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def extract_months(date_start: date, date_end: date):
    years_months = []
    current_year = date_start.year
    current_month = date_start.month

    while (current_year, current_month) <= (date_end.year, date_end.month):
        years_months.append((current_year, current_month))
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1

    return years_months


# Output: [(2023, 12), (2024, 1), (2024, 2)]

def get_month_range(year, month):
    first_day = datetime(year, month, 1)
    last_day = first_day + relativedelta(months=1) - relativedelta(days=1)
    return first_day, last_day


def fetch_flights(departure: str, destination: str, month: int, year: int) -> List[Flight]:
    date_start, date_end = get_month_range(year, month)
    url = f"https://biletyczarterowe.r.pl/api/destynacja/wyszukaj-wylot?dataUrodzenia%5B%5D=1989-10-30&iataSkad%5B%5D={departure}&iataDokad%5B%5D={destination}&dataMin={date_start.strftime('%Y-%m-%d')}&dataMax={date_end.strftime('%Y-%m-%d')}&oneWay=true"
    flights = []

    try:
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            for item in data:
                for ticket in item["Bilety"]:
                    flight = Flight(
                        departure=ticket["Wylot"]["Iata"],
                        destination=ticket["Przylot"]["Iata"],
                        date=datetime.strptime(item["Data"], '%Y-%m-%d'),
                        time_departure=datetime.strptime(ticket["Wylot"]["Godzina"], '%H:%M').time() if ticket["Wylot"][
                            "Godzina"] else None,
                        time_arrival=datetime.strptime(ticket["Przylot"]["Godzina"], '%H:%M').time() if
                        ticket["Przylot"]["Godzina"] else None,
                        flight_time=ticket.get("CzasLotu", None),
                        id_arrival_next_day=ticket["Wylot"].get("Przesuniecie", None),
                        is_dreamliner=ticket["CzyDreamliner"],
                        checked_baggage=bool(ticket["BagazRejestrowany"]),
                        hand_luggage=bool(ticket["BagazPodreczny"]),
                        food=ticket["Wyzywienie"],
                        price=ticket["Cena"],
                        update_data=datetime.utcnow()
                    )
                    flights.append(flight)

        else:
            print(f"Error fetching data with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return flights


def save_flights_to_database(flights, db: Session):
    try:
        db.add_all(flights)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred while saving to the database: {e}")


def update_records(flights, db: Session):
    for flight in flights:
        existing_flight = db.query(Flight).filter(
            Flight.date == flight.date,
            Flight.destination == flight.destination,
            Flight.departure == flight.departure
        ).first()

        if existing_flight:
            existing_flight.time_departure = flight.time_departure
            existing_flight.time_arrival = flight.time_arrival
            existing_flight.flight_time = flight.flight_time
            existing_flight.id_arrival_next_day = flight.id_arrival_next_day
            existing_flight.is_dreamliner = flight.is_dreamliner
            existing_flight.checked_baggage = flight.checked_baggage
            existing_flight.hand_luggage = flight.hand_luggage
            existing_flight.food = flight.food
            existing_flight.price = flight.price
            existing_flight.update_data = datetime.utcnow()
        else:
            db.add(flight)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred during the database transaction: {e}")
