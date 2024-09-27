from fastapi import Depends, FastAPI, HTTPException
from schemas import Car, CarInput, Trip, TripInput
from sqlmodel import Session, create_engine, SQLModel, select
from contextlib import asynccontextmanager

app = FastAPI(title="Car Sharing")

engine = create_engine(
    "sqlite:///carsharing.db", 
    connect_args={"check_thread": False}, 
    echo=True
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup event
    SQLModel.metadata.create_all(engine)
    yield
    # shatdown event
    pass


def get_session():
    with Session(engine) as session:
        yield session

@app.get("/api/cars")
def get_cars(size: str | None = None, doors: int | None = None, session: Session = Depends(get_session)) -> list:
    # with Session(engine) as session:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors == doors)
    return session.exec(query).all()

@app.get("/api/cars/{id}")
def car_by_id(id: int, session: Session = Depends(get_session)) -> dict:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

@app.post("/app/cars", response_model= Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    # with Session(engine) as session:
    new_car = Car.model_validate(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@app.delete("/api/cars/{id}", satatus_code=284)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

@app.put("/api/cars/{id}", response_model=Car)
def change_car(id: int, new_data: CarInput, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size= new_data.size
        car.doors = new_data.doors
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.post("/api/cars/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, trip_input: TripInput,
             session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.model_validate(trip_input, update={'car_id': car_id})
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")




