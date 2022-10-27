# Modifié par Olivier en conséquence de la nouvelle utilité de l'historique
# (celui des shared_trips) - Février 2021

from main import db
from main.model.history import History


def get_overall_history():
    return History.query.all()


def get_history_by_shared_trip_id(shared_trip_id):
    return History.query.filter(History.shared_trip_id == shared_trip_id).all()


def insert_new_history(data):
    history = History(
        driver_id = data["driver_id"],
        passenger_id = data["passenger_id"],
        path_json = data["path"],
        occ_details_pickle = data["occ_details"],
        shared_trip_status= data["shared_trip_status"],
        driver_status = data["driver_status"],
        passenger_status = data["passenger_status"],
        pickled_when = data["when"],
        shared_distance = data["shared_distance"],
        yacka_points_amount = data["yacka_points_amount"],
        status_set_date = data["status_set_date"],
        shared_trip_id = data["shared_trip_id"],
        wtrip_list_id = data["wtrip_list_id"]
    )
    db.session.add(history)
    # On laisse le commit être fait par la routine appelante, pour lui laisser
    # la possibilité de synchroniser la création de l'archive avec une autre
    # màj de la BDD.
