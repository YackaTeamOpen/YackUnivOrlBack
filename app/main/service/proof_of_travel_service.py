from flask_login import current_user

from main import db
from main.model.proof_of_travel import Proof_of_travel
from main.model.shared_trip import Shared_trip
from main.model.wtrip_list import Wtrip_list
from main.service.status_manager_service import Sht_wtl_whole
from main.service.trip_service import getAllAnonymizedTrips
from main.service.shared_trip_service import pay_ratio
from main.service.incentive_service import get_incentives
from datetime import datetime


def create_proof_of_travel(sht_id,contribution=0):
    """Cette fonction crée pour chaque shared_trip une preuve de covoiturage quand le shared_trip est terminated et la date de fin de trajet est équivelent à la date actuelle et prévue"""
    sht_wtl=(db.session.query(Shared_trip, Wtrip_list)
        .join(Wtrip_list, Shared_trip.id == Wtrip_list.sh_trip_id)
        .filter((Shared_trip.id==sht_id)
                (Shared_trip.shared_trip_status=="terminated")
                & (Shared_trip.driver_status=="drove")
                & (Shared_trip.pass_status=="was driven")
        )
        .first())

    if (sht_wtl == []):
        return None
    else:
        dtend = datetime.now().isoformat()
        for sht,wtl in sht_wtl:
            dict={}
            if dtend == sht.occ_details_pickle[len(sht.occ_details_pickle)-1]["arrival_date"]:
                dict["proof_of_class"]="C"
                trip = sht.trip
                dict["driver_id"]=trip.driver_id
                dict["driver_iso_start_time"]=sht.occ_details_pickle[0]["start_time"]

                dict["driver_iso_end_time"] = sht.occ_details_pickle[0]["arrival_time"]

                dict["passenger_iso_start_time"] = sht.occ_details_pickle[len(sht.occ_details_pickle) - 1]["start_time"]

                dict["passenger_iso_end_time"] = sht.occ_details_pickle[len(sht.occ_details_pickle) - 1]["arrival_time"]
                dict["passenger_seats"]=1;
                dict["passenger_contribution"]=contribution*pay_ratio(trip.free_ratio)
                incentivesDriver = (db.session.query(Incentive)
                    .join(User, Incentive.user_id == trip.driver_id)
                    .filter((Incentive.user_id==trip.driver_id)).all()
                )
                if incentives == []:
                    dict["incentives"]=[]
                revenue = 0
                for incentiveDriver in incentivesDriver:
                    revenue=revenue+incentiveDriver.amont

                dict["driver_revenue"]=revenue
                dict["passenger_id"] = wtl[0].waiting_trip.passenger_id
                dict["wtrip_list_id"] = wtl[0].id

                dict["incentives"]=get_incentives(trip.driver_id,dict["passenger_id"])




                for i in range(sht.path_json):
                    if i == sht.occ_details_pickle[0]["start_path_index"]:
                        dict["driver_start_latitude"]=sht.path_json[i]["lat"]
                        dict["driver_start_longitude"] = sht.path_json[i]["long"]
                    elif i == sht.occ_details_pickle[0]["arrival_path_index"]:
                        dict["driver_end_latitude"] = sht.path_json[i]["lat"]
                        dict["driver_end_longitude"] = sht.path_json[i]["long"]

                    if i == sht.occ_details_pickle[len(sht.path_json)-1]["start_path_index"]:
                        dict["passenger_start_latitude"]=sht.path_json[i]["lat"]
                        dict["passenger_start_longitude"]=sht.path_json[i]["long"]
                    if i == sht.occ_details_pickle[len(sht.path_json)-1]["end_path_index"]:
                        dict["passenger_end_latitude"]=sht.path_json[i]["lat"]
                        dict["passenger_end_longitude"]=sht.path_json[i]["long"]
                save_changes(dict)
                return {"status": "success", "message": "Proof of travel created"}, 200
            else:
                return {"status": "fail", "message": "Bad datetime"}, 400


def get_all_proofs_of_travel():
    return Proof_of_travel.query.all()


def get_proof_of_travel_by_wtl_id(wtl_id):
    return Proof_of_travel.query.join(Wtrip_list, Proof_of_travel.wtrip_list_id==wtl_id)\
        .filter(Proof_of_travel.wtrip_list_id==wtl_id).all()



def save_changes(data):
    db.session.add(data)
    db.session.commit()