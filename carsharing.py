from fastapi import FastAPI, HTTPException
from schemas import CarInput, CarOutput, load_db, save_db, TripInput, TripOutput

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

@app.post("/app/cars", response_model= CarOutput)
def add_car(car: CarInput):
    new_car = CarOutput(id = len(db)+1, size=car.size,doors=car.doors, fuel=car.fuel, transmission=car.transmission)
    db.append(new_car)
    save_db(db)
    return new_car

@app.post("/app/cars/{car_id}/trips", response_model=TripOutput)
def add_trip(car_id:int, trip: TripInput) -> TripOutput:    
    matches = [car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips)+1,
                             start=trip.start,end=trip.end,
                             description=trip.description)
        car.trips.add(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}")




