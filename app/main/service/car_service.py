from flask_login import current_user

from main import db
from main.model.car import Car
from main.model.trip import Trip


def getAllCar():
    cars = Car.query.all()
    return cars


def getCarById(car_id):
    car = Car.query.filter_by(id=car_id).first()
    return car


def getAllCarByUser(user_id):
    cars = Car.query.filter(Car.user_id == user_id).filter(Car.state != 0).all()
    return cars


def create_new_car(data):
    if current_user.is_active and current_user.type in [2, 4]:
        car = Car(
            user_id=current_user.id,
            label=data["label"],
            state=2
        )
        save_changes(car)
        db.session.refresh(car)
        return {"id": car.id, "status": "success", "message": "Car inserted"}, 201
    return {"status": "fail", "message": "Unauthorized"}, 401


def update_car(car_id, data):
    car = Car.query.filter_by(id=car_id).first()
    if car.user_id == current_user.id:
        Car.query.filter_by(id=car_id).update(data)
        save_changes(Car.query.filter_by(id=car_id).first())
        return {"status": "success", "message": "Car updated"}, 200
    return {"status": "fail", "message": "Unauthorized"}, 401


def delete_car(car_id):
    car = Car.query.filter_by(id=car_id).first()
    if car.user_id == current_user.id :
        # Check if an active trip or waiting_trip is linked to this car
        user_cars = user_trip_cars(current_user.id)
        if (car_id in user_cars["alive_trip_cars"]) :
            # can't delete this car
            return {"status": "fail", "message": "Car in use"}, 403
        elif (car_id in user_cars["deleted_trip_cars"]) :
            car.state = 0
            commit()
            return {"status": "success", "message": "Car state updated"}, 200
        else :
            Car.query.filter_by(id=car_id).delete()
            commit()
            return {"status": "success", "message": "Car deleted"}, 200
    return {"status": "fail", "message": "Unauthorized"}, 401


def user_trip_cars(user_id) :
    """ Returns a dict with the car ids of all the trips linked to a user """
    user_trips = Trip.query.filter_by(driver_id = user_id).all()
    alive_trip_cars, deleted_trip_cars = [], []
    for trip in user_trips :
        if trip.state == 0 :
            deleted_trip_cars.append(trip.car_id)
        else :
            alive_trip_cars.append(trip.car_id)
    return {
        "alive_trip_cars": alive_trip_cars,
        "deleted_trip_cars": deleted_trip_cars
    }


def save_changes(data):
    db.session.add(data)
    commit()


def commit():
    db.session.commit()
