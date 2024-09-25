import json
from pydantic import BaseModel

class Car(BaseModel):
    id:int
    size: str
    fuel: str | None = 'electric'
    doors: int
    transmission: str | None = 'auto'

def load_db() -> list[Car]:
    """Load a list of Car objects from a JSON file"""
    with open('cars.json') as f:
         data = json.load(f)
         return [Car(**obj) for obj in data]

