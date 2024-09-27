import json
from collections import OrderedDict
from sqlmodel import Relationship, SQLModel, Field


class TripInput(SQLModel):
    start: int
    end: int
    description: str

class Trip(TripInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")

class CarInput(SQLModel):
    size: str | None = 'xl'
    fuel: str | None = 'electric'
    doors: int
    transmission: str | None = 'auto'

class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)


        
    def ordered_dump(self) -> OrderedDict:
        field_order = self.Config.fields
        return OrderedDict((field, getattr(self, field)) for field in sorted(field_order, key=lambda k: field_order[k]['order']))


