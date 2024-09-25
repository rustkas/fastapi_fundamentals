import json
from pydantic import BaseModel

class Car(BaseModel):
    id:int
    size: str | None = 'xl'
    fuel: str | None = 'electric'
    doors: int
    transmission: str | None = 'auto'

def load_db() -> list[Car]:
    """Load a list of Car objects from a JSON file"""
    with open('cars.json') as f:
         data = json.load(f)
         return [Car(**obj) for obj in data]

def save_db(cars: list[Car]):
    with open("cars.json", 'w') as f:
        json.dump([car.model_dump() for car in cars], f, indent=4)