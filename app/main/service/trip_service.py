import datetime
from sqlalchemy.orm import aliased

from main import db
from main.model.trip import Trip
from main.model.address import Address


def getTripById(trip_id):
    trip = Trip.query.filter_by(id=trip_id).first()
    return trip


def getUserTrips(user_id):
    trips = Trip.query.filter(Trip.driver_id == user_id).filter(Trip.state != 0).all()
    return trips


def getUserTripCount(user_id):
    trip_count = Trip.query.filter(Trip.driver_id == user_id).filter(Trip.state != 0).count()
    return trip_count


def getAllAnonymizedTrips():
    start_address = aliased(Address)
    arrival_address = aliased(Address)
    now_dt = datetime.datetime.now()
    # recherche des trips non supprimés
    trip_addresses = db.session.query(
        Trip.id,
        start_address,
        arrival_address,
        Trip.recurrence_rule,
        Trip.pickled_when,
        Trip.single_trip,
        Trip.validity_start_date,
        Trip.validity_end_date,
        Trip.creation_date,
        Trip.start_time,
        Trip.driver_id
    ).\
        join(start_address, Trip.start_address_id == start_address.id).\
        join(arrival_address, Trip.arrival_address_id == arrival_address.id).\
        filter(Trip.state != 0).all()
    path_list = []
    for ta in trip_addresses :
        # On ne garde que ceux dont il reste des occurrences à venir
        if ta[4].count_after(now_dt) > 0 :
            path = {
                "id" : ta[0],
                "start_address" : ta[1],
                "arrival_address" : ta[2],
                "recurrence_rule" : ta[3],
                "single_trip" : ta[5],
                "validity_start_date" : ta[6],
                "validity_end_date" : ta[7],
                "creation_date" : ta[8],
                "start_time" : ta[9],
                "user_id" : ta[10],
            }
            path_list.append(path)
    return path_list
