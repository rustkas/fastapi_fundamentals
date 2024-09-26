import json
from pydantic import BaseModel
from collections import OrderedDict

class TripInput(BaseModel):
    start: int
    end: int
    description: str

class TripOutput(TripInput):
    id: int

class CarInput(BaseModel):
    size: str | None = 'xl'
    fuel: str | None = 'electric'
    doors: int
    transmission: str | None = 'auto'

class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []

    class Config:
        fields = {
            'id': {'order': 1},
            'size': {'order': 2},
            'fuel': {'order': 3},
            'doors': {'order': 4},
            'transmission': {'order': 5},  
    }
        
    def ordered_dump(self) -> OrderedDict:
        field_order = self.Config.fields
        return OrderedDict((field, getattr(self, field)) for field in sorted(field_order, key=lambda k: field_order[k]['order']))


def load_db() -> list[CarOutput]:
    """Load a list of Car objects from a JSON file"""
    with open('cars.json') as f:
         data = json.load(f)
         if not data:
             return []
         return [CarOutput(**obj) for obj in data]

def save_db(cars: list[CarInput]):
    with open("cars.json", 'w') as f:
        json.dump([car.ordered_dump() for car in cars], f, indent=4)