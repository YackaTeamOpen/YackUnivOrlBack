from sqlalchemy.orm import aliased
from datetime import datetime
import pprint
import itertools

from main import db

from main.model.trip import Trip
from main.model.user import User
from main.model.waiting_trip import Waiting_trip
from main.model.wtrip_list import Wtrip_list
from main.model.shared_trip import Shared_trip
import qrcode

from main.service.shared_trip_service import (
    get_shared_trips_per_user,
    get_a_shared_trip
)
from main.service.status_manager_service import (
    Sht_wtl_whole,
    terminate_a_shared_trip
)
from main.service.history_service import (
    get_overall_history,
    get_history_by_shared_trip_id,
)


def test(test_type, arg=None, arg2=None, arg3=None, arg4=None, arg5=None):
    """ Runs a sequence of tests mentionned by test_type.

    Test list : [ list_all_users | list_users_with_multiple_shared_trips [--arg=<status>] | \
    list_users_with_one_shared_trip [--arg=<status>] | show_shared_trip_consistency |\
    list_concurrent_shared_trips | delete_pending_shared_trips | overall_shared_trip_history | \
    shared_trip_history --arg=<sht_id> | trips_with_shared_trips | show_shared_trip_statuses | \
    terminate_a_shared_trip --arg=<shared_trip_id> ]
    """

    def list_all_users() :
        user_list = User.query.all()
        for user in user_list :
            print("\nId: {}, email: {}, active: {}".format(
                user.id,
                user.email,
                ("no" if user.type == 3 else "yes")
            ))

    if test_type in ["list_all_users"]:
        list_all_users()
        return True

    def list_users_with_shared_trips(min_number = 1, status = None):
        """Recherche des utilisateurs avec un ou plus shared_trip "visible" associé

        Si un argument est donné grâce à "--arg=...", on considère que cet argument
        représente un statut. ET dans ce cas, seuls les utilisateurs dont au moins
        un shared_trip associé est au statut correspondant (mais dont au moins deux des
        shared_trips ont des statuts différents) seront retournés.
        """
        test_beginning = datetime.now()
        print("début de la recherche des utilisateurs 'multi-shared_trips' : {:%H:%M:%S}\n".format(
            test_beginning))
        user_list = User.query.all()
        users_with_multiple_shared_trips = []
        for u in user_list:
            shared_trip_and_wtrip_list_lists = get_shared_trips_per_user(u.id, show_all = False)
            if (shared_trip_and_wtrip_list_lists is not None) and (len(shared_trip_and_wtrip_list_lists["shared_trip_list"]) >= min_number) :
                # On crée une liste des id et des statuts des shared_trips
                user_sht_status_list = [
                    (sht.id, sht.shared_trip_status) for sht in shared_trip_and_wtrip_list_lists["shared_trip_list"]
                ]
                if status is None :
                    users_with_multiple_shared_trips.append("{} ({} {} {}) : {}".format(
                        u.id, u.surname, u.name, u.email, user_sht_status_list))
                else :
                    sht_status_list = [sht_status[1] for sht_status in user_sht_status_list]
                    # on vérifie si le statut spécifié fait partie de la liste
                    # et si, si min_number > 1, il y a plus de 2 statuts différents
                    if (status in sht_status_list) and ((min_number < 2) or len(set(user_sht_status_list)) > 1) :
                        users_with_multiple_shared_trips.append("{} ({} {} {}) : {}".format(
                            u.id, u.surname, u.name, u.email, user_sht_status_list))
        test_end = datetime.now()
        print("fin  de la recherche des utilisateurs 'multi-shared_trips' : {:%H:%M:%S}\n ({} sec.)".format(
            test_end, (test_end - test_beginning).total_seconds()))
        print("Nb of users with multiple shared_trips{} : {}\n".format("" if status is None
                                                                       else " and at least one with status '{}'".format(status),
                                                                       len(users_with_multiple_shared_trips)))
        for line in users_with_multiple_shared_trips :
            print(line)

    if test_type in ["list_users_with_one_shared_trip"] :
        list_users_with_shared_trips(min_number = 1, status = arg)
        return True

    if test_type in ["list_users_with_multiple_shared_trips"] :
        list_users_with_shared_trips(min_number = 2, status = arg)
        return True

    def list_concurrent_shared_trips() :
        """Recherche des shared_trips pour lesquels il existe des shared_trip concurrents"""
        sht_id_list = [sht.id for sht in Shared_trip.query.all()]
        driver = aliased(User)
        passenger = aliased(User)
        result_list = []
        for sht_id in sht_id_list:
            sht_wtl = get_a_shared_trip(sht_id)
            sht = sht_wtl["shared_trip_list"][0]
            wtl = sht_wtl["wtrip_list_list"][0][0]
            shared_trips_wtrip_lists = (db.session.query(Shared_trip, Wtrip_list, driver, passenger)
                                        .join(Trip, Shared_trip.trip_id == Trip.id)
                                        .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
                                        .join(Waiting_trip, Wtrip_list.waiting_trip_id == Waiting_trip.id)
                                        .join(driver, Trip.driver_id == driver.id)
                                        .join(passenger, Waiting_trip.passenger_id == passenger.id)
                                        .filter(((Trip.id == sht.trip_id) | (Waiting_trip.id == wtl.waiting_trip_id))
                                                & (Shared_trip.id != sht_id))
                                        .all())
            if len(shared_trips_wtrip_lists) != 0 :
                result_list.append([sht_id, [(sht.id, wtl.id, drv.id, psg.id)
                                             for sht, wtl, drv, psg in shared_trips_wtrip_lists]])
        # pp = pprint.PrettyPrinter(indent = 4)
        print("{} Shared_trips avec concurrents :".format(len(result_list)))
        pprint_output = pprint.pformat(result_list, indent=4)
        print(pprint_output)

    if test_type in ["list_concurrent_shared_trips", "all"] :
        list_concurrent_shared_trips()
        return True

    def show_shared_trip_statuses():
        """Liste le nombre de shared_trips pour chaque statut dans la BDD"""
        shared_trips_wtrip_lists = (
            db.session.query(Shared_trip, Wtrip_list)
            .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
            .all()
        )
        status_count_dict = {}
        print("{} shared_trips :".format(len(shared_trips_wtrip_lists)))
        for sht, wtl in shared_trips_wtrip_lists:
            global_status = (
                sht.shared_trip_status
                + " / "
                + sht.driver_status
                + " /"
                + wtl.passenger_status
            )
            if global_status in status_count_dict:
                status_count_dict[global_status] += 1
            else:
                status_count_dict[global_status] = 1
            # print("shared_trip id : {}, {}".format(sht.id, global_status))
        # pp = pprint.PrettyPrinter(indent = 4)
        pprint_output = pprint.pformat(status_count_dict, indent=4)
        print(pprint_output)

    if test_type in ["show_shared_trip_statuses"] :
        show_shared_trip_statuses()
        return True

    def show_shared_trip_consistency():
        """Liste le nombre de shared_trips pour chaque statut dans la BDD"""
        shared_trips_wtrip_lists = (
            db.session.query(Shared_trip, Wtrip_list)
            .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
            .all()
        )
        print("{} shared_trips :".format(len(shared_trips_wtrip_lists)))
        for sht, wtl in shared_trips_wtrip_lists:
            sht_wtl_whole = Sht_wtl_whole(sht, wtl)
            if sht_wtl_whole.is_ok :
                continue
            else:
                print("Erreur sht {} : {} - {} - {}".format(
                    sht.id,
                    sht.shared_trip_status,
                    sht.driver_status,
                    wtl.passenger_status))

    if test_type in ["show_shared_trip_consistency"] :
        show_shared_trip_consistency()
        return True

    if test_type in ["trips_with_shared_trips"] :
        """Liste les trips et les waiting_trips associés à au moins un shared_trip"""
        shared_trips_wtrip_lists = (
            db.session.query(Shared_trip, Wtrip_list)
            .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
            .all()
        )
        trip_list, wtrip_list = [], []
        for sht, wtl in shared_trips_wtrip_lists:
            trip_list.append(sht.trip_id)
            wtrip_list.append(wtl.waiting_trip_id)
        sorted_filtered_trip_list = sorted(set(trip_list))
        sorted_filtered_wtrip_list = sorted(set(wtrip_list))
        print("Trips    |    Waiting_trips")
        for trip, wtrip in itertools.zip_longest(sorted_filtered_trip_list,
                                                 sorted_filtered_wtrip_list, fillvalue = "----") :
            print("{}    |    {}".format(trip, wtrip))
        return True

    if test_type in ["overall_shared_trip_history"] :
        """Liste l'historique des états des shared_trips"""
        history = get_overall_history()
        for item in history:
            print(item)
        return True

    if test_type in ["shared_trip_history"] :
        if arg == None:
            print("shared_trip id argument missing.")
            return None
        sht_id = int(arg)
        history = get_history_by_shared_trip_id(sht_id)
        print("History of shared_trip {}".format(sht_id))
        for item in history:
            print(
                "On {}, status changed to {}/{}/{}\n  -> with recurrence : {}/{}/{}/{} ".format(
                    item.status_set_date,
                    item.shared_trip_status,
                    item.driver_status,
                    item.passenger_status,
                    item.pickled_when.dtstart,
                    item.pickled_when.dtend,
                    item.pickled_when.is_recurring,
                    item.pickled_when.rruleset,
                )
            )
        return True

    if test_type in ["terminate_a_shared_trip"]:
        if (arg == None) :
            print("<shared_trip_id> argument missing.")
            return None
        terminate_a_shared_trip(arg)
        return True
    if test_type in ["trips"]:
        trip = get_a_shared_trip(1)
        print(trip)
        return True

    def list_terminated_sht_proof_of_travel():
        shared_trips_wtrip_lists_terminated = (
            db.session.query(Shared_trip, Wtrip_list)
                .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
                .filter(Shared_trip.shared_trip_status=="terminated")
                .all()
        )
        proofs_of_travel=[]
        for s,w in shared_trips_wtrip_lists_terminated:
            sht_whole = Sht_wtl_whole(s,w)
            if sht_whole.is_ok:
                proof = get_proof_of_travel_sht(sht_whole.sht.id)
                proofs_of_travel.append("Proof of travel of the shared trip {}: {}".format(
                    sht_whole.sht.id,proof)
                )
        if (len(proofs_of_travel)>0):
            print(proofs_of_travel)
        else:
            print("Number of terminated shared trip : {}".format(
                len(shared_trips_wtrip_lists_terminated)
            ))

    if test_type in ["list_proof_of_travel"]:
        list_terminated_sht_proof_of_travel()
        return True



    return None
