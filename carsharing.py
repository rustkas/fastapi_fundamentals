import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db

app = FastAPI(title="Car Sharing")

db = load_db()

@app.get("/api/cars")
def get_cars(size: str | None = None, doors: int | None = None) -> list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int) -> dict:
    print(f"db = {db}")
    result = [car for car in db if car.id == id]
    if result:
        return result[0].model_dump()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")







