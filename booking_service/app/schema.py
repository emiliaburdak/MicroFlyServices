from pydantic import BaseModel


class FlightSchema(BaseModel):
    id: int
    user_id: int
    flight_id: int

    class Config:
        orm_mode = True
