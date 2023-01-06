from flask_login import current_user

from main import db
from main.model.proof_of_travel import Proof_of_travel
from main.model.shared_trip import Shared_trip
from main.model.wtrip_list import Wtrip_list
from main.model.incentive import Incentive
from main.model.user import User
from main.service.shared_trip_service import pay_ratio
from main.service.incentive_service import (
    create_incentive,
    create_incentives,
    get_incentivesPassenger,
    get_incentivesDriver,
    get_incentives,
    get_incentives_by_user
)
from main.model.history import History
from main.service.history_service import get_history_by_shared_trip_id
from main.service.status_manager_service import (
    user_visible_shared_trip_status_exception_list,
    user_visible_driver_status_exception_list,
    user_visible_passenger_status_exception_list,
    terminated_candidate_status_list
)
from main.service.path_when_service import (
    estimate_real_distance_between
)
from datetime import datetime,date


def time_end(end_dt, gap):
    """ Retourne True si la différence entre l'heure de fin self et celle de end_dt est inférieure à max_time_gap"""
    today_dt = date.today()
    dtend=datetime.now()
    dt1 = end_dt.replace(day=today_dt.day, month=today_dt.month, year=today_dt.year)
    dt2 = dtend.replace(day=today_dt.day, month=today_dt.month, year=today_dt.year)
    time_diff = dt1 - dt2
    return True if (abs(time_diff.total_seconds() / 60) < gap) else False

def create_proof_of_travel(sht_id,contribution=0,amont_driver=0,amont_passenger=0,revenue=0):
    """Cette fonction crée pour chaque shared_trip une preuve de covoiturage quand le shared_trip est terminated et la date de fin de trajet est équivelent à la date actuelle et prévue"""
    sht_wtl=(db.session.query(Shared_trip, Wtrip_list)
             .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
             .filter((Shared_trip.id==sht_id) &
                (Shared_trip.shared_trip_status.notin_(user_visible_shared_trip_status_exception_list()))
                & (Wtrip_list.passenger_status.notin_(user_visible_passenger_status_exception_list()))
                & (Shared_trip.driver_status.notin_(user_visible_driver_status_exception_list()))
        )
        .first())

    if (sht_wtl == []):
        return None
    else:
        dtend = datetime.now()
        sht=sht_wtl[0]
        wtl=sht_wtl[1]
        dict={}
        if time_end(sht.occ_details_pickle[len(sht.occ_details_pickle)-1]["arrival_time"],240):
            dict["proof_class"]="C"
            trip = sht.trip
            dict["driver_id"]=trip.driver_id
            dict["driver_iso_start_time"]=sht.occ_details_pickle[0]["start_time"].isoformat()

            dict["driver_iso_end_time"] = sht.occ_details_pickle[0]["arrival_time"].isoformat()

            dict["passenger_iso_start_time"] = sht.occ_details_pickle[len(sht.occ_details_pickle) - 1]["start_time"].isoformat()

            dict["passenger_iso_end_time"] = sht.occ_details_pickle[len(sht.occ_details_pickle) - 1]["arrival_time"].isoformat()
            dict["passenger_seats"]=1;
            dict["passenger_contribution"]=contribution*pay_ratio(trip.free_ratio)
            revenue = 0
            if get_incentivesDriver(dict["driver_id"]) is None or get_incentivesDriver(dict["driver_id"]) == []:
                incentivesDriver = create_incentive(amont_driver,dict["driver_id"])
            dict["driver_revenue"]=revenue
            dict["passenger_id"] = wtl.waiting_trip.passenger_id
            dict["wtrip_list_id"] = wtl.id
            if get_incentivesPassenger(dict["passenger_id"]) is None or get_incentivesPassenger(dict["passenger_id"]) == []:
                incentivesPassenger = create_incentive(amont_passenger,dict["passenger_id"])

            create_incentives(dict["passenger_id"],dict["driver_id"],dict["wtrip_list_id"])
            incentives = get_incentives(trip.driver_id, dict["passenger_id"], dict["wtrip_list_id"])
            dict["incentive_id"]=incentives.id

            for i in range(len(sht.path_json)):
                if i == sht.occ_details_pickle[0]["start_path_index"]:
                    dict["driver_start_latitude"]=sht.path_json[i][1]
                    dict["driver_start_longitude"] = sht.path_json[i][0]
                elif i == sht.occ_details_pickle[0]["arrival_path_index"]:
                    dict["driver_end_latitude"] = sht.path_json[i][1]
                    dict["driver_end_longitude"] = sht.path_json[i][0]

                if i == sht.occ_details_pickle[len(sht.occ_details_pickle)-1]["start_path_index"]:
                    dict["passenger_start_latitude"]=sht.path_json[i][1]
                    dict["passenger_start_longitude"]=sht.path_json[i][0]
                if i == sht.occ_details_pickle[len(sht.occ_details_pickle)-1]["arrival_path_index"]:
                    dict["passenger_end_latitude"]=sht.path_json[i][1]
                    dict["passenger_end_longitude"]=sht.path_json[i][0]
            proof = Proof_of_travel(
                proof_class=dict["proof_class"],
                driver_id=dict["driver_id"],
                driver_iso_start_time=dict["driver_iso_start_time"],
                driver_start_latitude=dict["driver_start_latitude"],
                driver_start_longitude=dict["driver_start_longitude"],
                driver_iso_end_time=dict["driver_iso_end_time"],
                driver_end_latitude=dict["driver_end_latitude"],
                driver_end_longitude=dict["driver_end_longitude"],
                passenger_id=dict["passenger_id"],
                passenger_iso_start_time=dict["passenger_iso_start_time"],
                passenger_start_latitude=dict["passenger_start_latitude"],
                passenger_start_longitude=dict["passenger_start_longitude"],
                passenger_iso_end_time=dict["passenger_iso_end_time"],
                passenger_end_latitude=dict["passenger_end_latitude"],
                passenger_end_longitude=dict["passenger_end_longitude"],
                passenger_seats=dict["passenger_seats"],
                passenger_contribution=dict["passenger_contribution"],
                driver_revenue=dict["driver_revenue"],
                incentive_id=dict["incentive_id"],
                wtrip_list_id=dict["wtrip_list_id"]
            )
            save_changes(proof)
            return {"status": "success", "message": "Proof of travel created"}, 201
        else:
            return {"status": "fail", "message": "Bad datetime"}, 400


def get_all_proofs_of_travel():
    return Proof_of_travel.query.all()


def get_proof_of_travel_by_wtl_id(wtl_id):
    return Proof_of_travel.query.join(Wtrip_list, Proof_of_travel.wtrip_list_id==wtl_id)\
        .filter(Proof_of_travel.wtrip_list_id==wtl_id).all()

def get_proof_of_travel_by_sht_id(sht_id):
    history = get_history_by_shared_trip_id(sht_id)[0];
    proof = Proof_of_travel.query.join(Wtrip_list, Proof_of_travel.wtrip_list_id==history.wtrip_list_id)\
        .filter_by(id=history.wtrip_list_id)
    return proof

def getAllProof():
    return Proof_of_travel.query.all()

def createProof(driver_id, passenger_id, trip_id):
    pass

def validateProof(proof_id):
    proof = Proof_of_travel.query.filter_by(id=int(proof_id)).first()
    proof.validate()
    save_changes(proof)
    return {}, 204

def getProofById(proof_id):
    proof = Proof_of_travel.query.filter_by(id=proof_id).first()
    return proof

def getProofByUser(user_id):
    proof = Proof_of_travel.query.filter((Proof_of_travel.driver_id==user_id) | (Proof_of_travel.passenger_id==user_id)).first()
    return proof

def getNbProofByUserAsDriver(user_id):
    proofs = Proof_of_travel.query.filter_by(driver_id=user_id)
    return proofs.count()

def getNbProofByUserAsPassenger(user_id):
    proofs = Proof_of_travel.query.filter_by(passenger_id=user_id)
    return proofs.count()

def getNbKmByUserAsDriver(user_id):
    proofs = Proof_of_travel.query.filter_by(driver_id=user_id)


def getNbKmByUserAsPassenger(user_id):
    proofs = Proof_of_travel.query.filter_by(passenger_id=user_id)


def list_shared_trip_terminate_candidates():
    sht_wtl = (db.session.query(Shared_trip, Wtrip_list)
               .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
               .filter(
                       (Shared_trip.shared_trip_status.notin_(user_visible_shared_trip_status_exception_list()))
                        & (Shared_trip.shared_trip_status.in_(terminated_candidate_status_list()))
                       & (Wtrip_list.passenger_status.notin_(user_visible_passenger_status_exception_list()))
                       & (Shared_trip.driver_status.notin_(user_visible_driver_status_exception_list()))
                       )
               .all())
    return sht_wtl


def get_one_shared_trip_terminate_candidates():
    """Cette fonction est utilisée pour les tests"""
    sht_wtl = (db.session.query(Shared_trip, Wtrip_list)
               .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
               .filter(
                       (Shared_trip.shared_trip_status.notin_(user_visible_shared_trip_status_exception_list()))
                        & (Shared_trip.shared_trip_status.in_(terminated_candidate_status_list()))
                       & (Wtrip_list.passenger_status.notin_(user_visible_passenger_status_exception_list()))
                       & (Shared_trip.driver_status.notin_(user_visible_driver_status_exception_list()))
                       )
               .first())
    return sht_wtl





def save_changes(data):
    db.session.add(data)
    db.session.commit()

def commit():
    db.session.commit()