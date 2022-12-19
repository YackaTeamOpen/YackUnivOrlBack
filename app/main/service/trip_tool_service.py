import datetime


from main import db

from main.model.trip import Trip
from main.model.waiting_trip import Waiting_trip
from main.service.trip_service import getAllAnonymizedTrips
from main.service.waiting_trip_service import getAllAnonymizedWaitingTrips
from main.service.path_when_service import (
    make_path_point_tuple_from_trip,
    estimate_real_distance_between
)
from main.service.community_service import users_related_to_organization


def get_trip_waiting_trip_list() :
    reduced_trip_list = getAllAnonymizedTrips()
    reduced_waiting_trip_list = getAllAnonymizedWaitingTrips()
    return {
        "reduced_trips" : reduced_trip_list,
        "reduced_waiting_trips" : reduced_waiting_trip_list
    }


def list_all_trips_by_organization(trip_type, organization_id, start_time = None) :
    user_list = users_related_to_organization(organization_id)
    user_id_list = [user.user_id for user in user_list]
    if trip_type == 'driver' :
        trip_list = (db.session.query(Trip)
                     .filter(Trip.state != 0)
                     .filter(Trip.driver_id.in_(user_id_list))
                     .all())
    else :
        trip_list = (db.session.query(Waiting_trip)
                     .filter(Waiting_trip.state != 0)
                     .filter(Waiting_trip.passenger_id.in_(user_id_list))
                     .all())
    if start_time is None :
        # Aucun filtre sur les dates des trips concernés
        return trip_list
    else :
        # On construit une liste ne reprenant de trip_list que les trips dont au moins
        # une occurrence est postérieure à start_time
        filtered_trip_list = []
        for trip in trip_list :
            if trip.pickled_when.is_all_before(start_time) :
                continue
            filtered_trip_list.append(trip)
    return filtered_trip_list


def list_on_going_trips_by_organization(trip_type, organization_id) :
    now_dt = datetime.datetime.now()
    return list_all_trips_by_organization(trip_type, organization_id, start_time = now_dt)


def trip_list_est_cumulative_distance(trip_list) :
    est_cumulative_distance = 0
    for trip in trip_list :
        trip_coord = make_path_point_tuple_from_trip(trip)
        est_cumulative_distance += estimate_real_distance_between(trip_coord[0], trip_coord[1])
    return int(est_cumulative_distance / 1000)


def trip_list_est_mean_distance(trip_list) :
    est_cumulative_distance = 0
    for trip in trip_list :
        trip_coord = make_path_point_tuple_from_trip(trip)
        est_cumulative_distance += estimate_real_distance_between(trip_coord[0], trip_coord[1])
    return 0 if len(trip_list) == 0 else (est_cumulative_distance / len(trip_list)) / 1000


def trip_list_recurrence_mean(trip_list) :
    recurrence_sum = 0
    for trip in trip_list :
        recurrence_sum += trip.pickled_when.nb_occurrences()
    return 0 if len(trip_list) == 0 else int(recurrence_sum / len(trip_list))


