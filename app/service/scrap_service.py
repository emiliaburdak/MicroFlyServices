from typing import List
import requests
from starlette import status

from app.models import Flight
from datetime import datetime


def fetch_flights_from_external_api(departure: str, destination: str, date_start: datetime, date_end: datetime) -> List[Flight]:
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
                        price=item["Cena"],
                    )
                    flights.append(flight)
        else:
            print(f"Error fetching data with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return flights
