from flask_login import current_user

from main import db
from main.model.address import Address
from main.model.trip import Trip
from main.model.waiting_trip import Waiting_trip


def getAllAddress():
    return Address.query.all()


def getAddressById(address_id):
    return Address.query.filter_by(id=address_id).first()


def getAllAddressByUser(user_id):
    addresses = Address.query.filter_by(user_id=user_id).all()
    return addresses


def get_all_user_s_non_deleted_addresses(user_id):
    addresses = Address.query.filter(Address.user_id == user_id).filter(Address.state == 2).all()
    return addresses


def delete_address(address_id):
    address = Address.query.filter_by(id=address_id).first()
    if address.user_id == current_user.id :
        # Check if an active trip or waiting_trip is linked to this address
        user_addresses = user_trip_addresses(current_user.id)
        if ((address_id in user_addresses["alive_trip_addresses"]) or (address_id in user_addresses["alive_wtrip_addresses"])) :
            # can't delete this address
            return {"status": "fail", "message": "Address in use"}, 403
        else :
            address.state = 0
            commit()
            return {"status": "success", "message": "Address state updated"}, 200
    return {"status": "fail", "message": "Unauthorized"}, 401


def user_trip_addresses(user_id) :
    """ Returns a dict with the address ids of all the trips linked to a user """
    user_trips = Trip.query.filter_by(driver_id = user_id).all()
    user_waiting_trips = Waiting_trip.query.filter_by(passenger_id = user_id).all()
    alive_trip_addresses, alive_wtrip_addresses = [], []
    deleted_trip_addresses, deleted_wtrip_addresses = [], []
    for trip in user_trips :
        if trip.state == 0 :
            deleted_trip_addresses.append(trip.start_address_id)
            deleted_trip_addresses.append(trip.arrival_address_id)
        else :
            alive_trip_addresses.append(trip.start_address_id)
            alive_trip_addresses.append(trip.arrival_address_id)
    for wtrip in user_waiting_trips :
        if wtrip.state == 0 :
            deleted_wtrip_addresses.append(wtrip.start_address_id)
            deleted_wtrip_addresses.append(wtrip.arrival_address_id)
        else :
            alive_wtrip_addresses.append(wtrip.start_address_id)
            alive_wtrip_addresses.append(wtrip.arrival_address_id)
    return {
        "alive_trip_addresses": alive_trip_addresses,
        "deleted_trip_addresses": deleted_trip_addresses,
        "alive_wtrip_addresses": alive_wtrip_addresses,
        "deleted_wtrip_addresses": deleted_wtrip_addresses
    }


def save_changes(data):
    db.session.add(data)
    commit()


def commit():
    db.session.commit()
