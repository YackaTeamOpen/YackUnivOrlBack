# Modifié par Olivier pour la prise en compte des Yacka_when
# et la recherche de trajets partageables pour le conducteur
# ou le passager concerné - Janvier 2021
import datetime
from sqlalchemy.orm import aliased

from main import db
from main.model.waiting_trip import Waiting_trip
from main.model.address import Address


def getWaitingTripById(waiting_trip_id):
    wtrip = Waiting_trip.query.filter_by(id=waiting_trip_id).first()
    return wtrip


def getUserWaitingTrips(user_id):
    wtrips = Waiting_trip.query.filter_by(passenger_id=user_id).filter(Waiting_trip.state != 0).all()
    return wtrips


def getUserWaitingTripCount(user_id):
    wtrip_count = Waiting_trip.query.filter_by(passenger_id=user_id).filter(Waiting_trip.state != 0).count()
    return wtrip_count


def getAllAnonymizedWaitingTrips():
    start_address = aliased(Address)
    arrival_address = aliased(Address)
    now_dt = datetime.datetime.now()
    # recherche des waiting_trips non supprimés
    waiting_trips_addresses = db.session.query(
        Waiting_trip.id,
        start_address,
        arrival_address,
        Waiting_trip.recurrence_rule,
        Waiting_trip.pickled_when,
        Waiting_trip.single_trip,
        Waiting_trip.validity_start_date,
        Waiting_trip.validity_end_date,
        Waiting_trip.creation_date,
        Waiting_trip.start_time,
        Waiting_trip.passenger_id
        ).\
        join(start_address, Waiting_trip.start_address_id == start_address.id).\
        join(arrival_address, Waiting_trip.arrival_address_id == arrival_address.id).\
        filter(Waiting_trip.state != 0).all()
    path_list = []
    for wta in waiting_trips_addresses :
        # On ne garde que ceux dont il reste des occurrences à venir
        if wta[4].count_after(now_dt) > 0 :
            path = {
                "id" : wta[0],
                "start_address" : wta[1],
                "arrival_address" : wta[2],
                "recurrence_rule" : wta[3],
                "single_trip" : wta[5],
                "validity_start_date" : wta[6],
                "validity_end_date" : wta[7],
                "creation_date" : wta[8],
                "start_time" : wta[9],
                "user_id" : wta[10],
            }
            path_list.append(path)
    return path_list
