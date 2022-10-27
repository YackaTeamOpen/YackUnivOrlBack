# Définit les fonctions de création et de manipulation des shared_trip
# Olivier - Janvier 2021
#
from datetime import datetime
# from dateutil.parser import *
import logging

from main import db

from main.model.trip import Trip
from main.model.waiting_trip import Waiting_trip
from main.model.wtrip_list import Wtrip_list
from main.model.shared_trip import Shared_trip

from main.service.waiting_trip_service import getWaitingTripById
from main.service.status_manager_service import (
    user_visible_shared_trip_status_exception_list,
    user_visible_driver_status_exception_list,
    user_visible_passenger_status_exception_list,
    bydate_displayable_shared_trip_status_list,
    phone_displayable_driver_status_list,
    phone_displayable_passenger_status_list,
    not_alive_status_list,
    rank_status
)
from main.service.user_service import getUserWithNoLastname
from main.service.community_service import users_related_to_organization
# from main.service.helpers import total_size

log = logging.getLogger(__name__)

# Pour le debug
# from test.display_service import display_when_from_trip_list,\
#    display_matching_dict_list, display_a_single_when


def get_a_shared_trip(shared_trip_id) :
    """Retourne le shared_trip dont l'id est passé en paramètre,

    et son (ses) wtrip_list associés, ou {} sinon.
    """
    # Attention : On suppose ici qu'il n'y a qu'un enregistrement wtrip_list par shared_trip
    # car dans la version actuelle, on n'autorise qu'un passager par conducteur.
    shared_trips_wtrip_lists = (
        db.session.query(Shared_trip, Wtrip_list)
        .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
        .filter(Shared_trip.id == shared_trip_id)
        .first()
    )
    # Dans ces conditions, le résultat de la requête précédente est un 2uple comprenant
    # un shared_trip et un wtrip_list.
    # (Si on ouvrait la possibilité de plusieurs passagers par conducteur, la requête
    # précedente, au lieu de se terminer par .first(), finirait par .all(), et renverrait
    # une liste de tels 2uples, de même shared_trip mais avec des wtrip_list différents,
    # et il faudrait itérer sur ces wtrip_list pour renvoyer un élément compatible
    # avec Shared_tripDto.shared_trip).
    #
    # Du résultat de la requête ci-dessus il faut faire un dictionnaire de 2 listes,
    # dont l'une est une liste de listes comme s'il pouvait y avoir plusieurs
    # passagers par shared_trip, afin de la rendre compatible avec
    # Shared_tripDto.shared_trip.
    # Le tout renvoyé au contrôleur sera prêt à transmettre à build_shtl_response_for_dto.
    if shared_trips_wtrip_lists is None :
        return None
    return {
        "shared_trip_list" : [shared_trips_wtrip_lists[0]],
        "wtrip_list_list" : [[shared_trips_wtrip_lists[1]]],
    }


def get_shared_trips_per_user(user_id, show_all=False) :
    """Retourne tous les shared_trip associés à un user, en tant que conducteur ou passager"""

    # Si show_all == False, ne retourne pas les shared_trips concernés par
    # user_visible_shared_trip_status_exception_list(), user_visible_driver_status_exception_list()
    # et user_visible_passenger_status_exception_list().
    # Si show_all == True, ne tient pas compte de ces restrictions.
    if show_all == True :
        shared_trips_wtrip_lists = (db.session.query(Shared_trip, Wtrip_list)
                                    .join(Trip, Shared_trip.trip_id == Trip.id)
                                    .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
                                    .join(Waiting_trip, Wtrip_list.waiting_trip_id == Waiting_trip.id)
                                    .filter((Trip.driver_id == user_id) | (Waiting_trip.passenger_id == user_id))
                                    .all())
    else :
        shared_trips_wtrip_lists = (
            db.session.query(Shared_trip, Wtrip_list)
            .join(Trip, Shared_trip.trip_id == Trip.id)
            .join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id)
            .join(Waiting_trip, Wtrip_list.waiting_trip_id == Waiting_trip.id)
            .filter(Shared_trip.shared_trip_status.notin_(user_visible_shared_trip_status_exception_list())
                    & (((Trip.driver_id == user_id)
                        & Shared_trip.driver_status.notin_(user_visible_driver_status_exception_list()))
                       | ((Waiting_trip.passenger_id == user_id)
                          & Wtrip_list.passenger_status.notin_(user_visible_passenger_status_exception_list()))
                       )).all())

    # Attention : On suppose ici qu'il n'y a qu'un enregistrement wtrip_list par shared_trip
    # car dans la version actuelle, on n'autorise qu'un passager par conducteur.
    # Il faudrait modifier la boucle suivante si on ouvrait la possibilité d'avoir des
    # trajets multipassagers (boucle imbriquée plutôt qu'itération en parallèle).
    # Dans ces conditions, le résultat de la requête précédente est une liste de
    # n listes de 2 éléments :
    # le premier de ces éléments est un shared_trip, le second est un wtrip_list.
    # Il faut en faire 2 listes de n shared_trip et de n wtrip_list.
    # Mais il faut reconfigurer la seconde pour en faire une liste de listes
    # comme s'il pouvait y avoir plusieurs passagers par shared_trip, afin de la rendre
    # compatible avec Shared_tripDto.shared_trip.
    # Le tout renvoyé sous forme de dictionnaire au contrôleur sera prêt à
    # transmettre à build_shtl_response_for_dto.
    if len(shared_trips_wtrip_lists) == 0 :
        return None
    shared_trip_list, wtrip_list_list = [], []
    for sht, wtl in shared_trips_wtrip_lists :
        shared_trip_list.append(sht)
        wtrip_list_list.append([wtl])
    # breakpoint()
    return {"shared_trip_list" : shared_trip_list, "wtrip_list_list" : wtrip_list_list}


def build_shtl_response_for_dto(shared_trip_and_wtrip_list) :
    """Construit et retourne une réponse adaptée au modèle du DTO

    à partir de la liste des shared_trip et des wtrip_list (soit renvoyés
    par le processus de sélection "spatio-temporelle" :) puis de path-
    matching, soit par une sélection des shared_trip relatifs à un user...).
    """
    # Cette fonction prend en paramètre un dictionnaire :
    # {
    #   "shared_trip_list" : liste de shared_trip,
    #   "wtrip_list_list" : liste de listes de wtrip_list
    # }
    # Elle retourne une liste de dictionnaires conformes à Shared_tripDto.shared_trip.
    #
    # On va parcourir la liste des shared_trip et des wtrip_list associés
    # et construire une liste de shared_trip conformes au modèle du DTO.
    #
    # On part du principe que, dans la version actuelle, il n'y a qu'un enregistrement
    # wtrip_list par shared_trip (1 passager par conducteur). Conséquence : on parcourt
    # en parallèle les deux listes (de longueur égale) du dictionnaire passé en paramètre,
    # il faudrait faire deux boucles imbriquées si ce n'était pas le cas. Toutefois à chaque
    # shared_trip sont associées des listes relatives aux passagers (id, noms, prénoms...)
    # comme s'il y avait potentiellement plusieurs passagers par shared_trip.
    #
    # On initialise la liste de dictionnaires sur laquelle va se calquer le modèle du DTO
    return_dict_list = []
    for sht, wtl in zip(shared_trip_and_wtrip_list["shared_trip_list"],
                        shared_trip_and_wtrip_list["wtrip_list_list"]) :
        return_dict = {}
        return_dict["id"] = sht.id
        return_dict["trip_id"] = sht.trip_id
        trip = sht.trip
        # trip = getTripById(sht.trip_id)
        return_dict["trip_driver_id"] = trip.driver_id
        return_dict["event_occurrence_id"] = trip.event_occurrence_id
        return_dict["nb_seats"] = trip.nb_seats
        return_dict["car_label"] = trip.car.label
        return_dict["trip_driver"] = getUserWithNoLastname(trip.driver_id)
        return_dict["driver_score"] = sht.driver_score
        return_dict["passengers_score"] = sht.passengers_score
        return_dict["shared_trip_comment"] = trip.comment
        return_dict["shared_trip_status"] = sht.shared_trip_status
        return_dict["driver_status"] = sht.driver_status
        # Initialisation de la liste itinéraire
        path = []
        for point in sht.path_json :
            path_point = {
                "long" : point[0],
                "lat" : point[1],
                "address" : {
                    "street" : point[2],
                    "name" : point[2],
                    "city" : point[3],
                    "postcode" : point[4],
                    "label" : point[2] + " " + point[4] + " " + point[3],
                    "housenumber" : ""
                },
            }
            path.append(path_point)
        return_dict["path"] = path
        # Initialisation de la liste routage
        directions = []
        for point in sht.directions_json :
            directions_point = {"long" : point[0], "lat" : point[1]}
            directions.append(directions_point)
        return_dict["directions"] = directions
        # Initialisation de la liste des détails occupants (yc conducteur)
        # Cette partie fonctionnerait aussi avec de multiples passagers par conducteur
        occ_details_list = []
        for details in sht.occ_details_pickle :
            occ_details = {
                "start_time" : details["start_time"],
                "start_path_index" : details["start_path_index"],
                "arrival_time" : details["arrival_time"],
                "arrival_path_index" : details["arrival_path_index"],
            }
            occ_details_list.append(occ_details)
        return_dict["occ_details_list"] = occ_details_list
        # Initialisation des listes liées aux passagers : when, id, name, surname,
        # status, comment, waiting_trip_id, shared_distance
        occ_when_list, passenger_id_list = [], []
        passenger_list, yacka_points_list, fr_info_list = [], [], []
        passenger_status_list, passenger_comment_list, waiting_trip_id_list = [], [], []
        passenger_nb_pass_list = []
        for wtrip_list in wtl :
            waiting_trip = getWaitingTripById(wtrip_list.waiting_trip_id)
            waiting_trip_id_list.append(waiting_trip.id)
            passenger_id_list.append(waiting_trip.passenger_id)
            passenger_nb_pass_list.append(waiting_trip.nb_passengers)
            passenger_list.append(getUserWithNoLastname(waiting_trip.passenger_id))
            yacka_points_list.append(wtrip_list.yacka_points_amount)
            fr_info_list.append(wtrip_list.fr_info)
            passenger_status_list.append(wtrip_list.passenger_status)
            passenger_comment_list.append(waiting_trip.comment)
            # Construction de la liste des datetimes d'occurrence liée au passager
            when = wtrip_list.pickled_when
            if when.is_recurring :
                occ_when_list.append({"occurrence_list" : [dt for dt in when.rruleset]})
            else :
                occ_when_list.append({"occurrence_list" : [when.dtstart]})
        # On affecte ces listes ainsi constituées aux clés du dictionnaire résultat
        return_dict["occ_when_list"] = occ_when_list
        return_dict["passenger_id_list"] = passenger_id_list
        return_dict["passenger_nb_pass_list"] = passenger_nb_pass_list
        return_dict["passenger_list"] = passenger_list
        # return_dict["shared_distance_list"] = shared_distance_list
        return_dict["passenger_status_list"] = passenger_status_list
        return_dict["passenger_comment_list"] = passenger_comment_list
        return_dict["waiting_trip_id_list"] = waiting_trip_id_list
        return_dict["yacka_points_list"] = yacka_points_list
        return_dict["fr_info_list"] = fr_info_list
        return_dict_list.append(return_dict)
    return return_dict_list


def build_shtl_response_for_agenda_dto(shared_trip_and_wtrip_list, user_id, startdate, enddate = None) :
    """Construit et retourne une réponse adaptée au modèle du DTO pour afficher l'agenda

    à partir de la liste des shared_trip et des wtrip_list (soit renvoyés
    par le processus de sélection "spatio-temporelle" :) puis de path-
    matching, soit par une sélection des shared_trip relatifs à un user...).
    """
    # Cette fonction prend en paramètre un dictionnaire :
    # {
    #   "shared_trip_list" : liste de shared_trip,
    #   "wtrip_list_list" : liste de listes de wtrip_list
    # }
    # Elle retourne une liste de dictionnaires conformes à Shared_tripDto.shared_trip_agenda.
    # Les shared_trips retournés sont compris entre startdate et enddate
    # Si la enddate n'affiche aucun résultat, alors elle est artificiellement augmentée
    # D'une semaine jusqu'à avoir un résultat
    #
    # On va parcourir la liste des shared_trip et des wtrip_list associés
    # et construire une liste de shared_trip conformes au modèle du DTO.
    #
    # On part du principe que, dans la version actuelle, il n'y a qu'un enregistrement
    # wtrip_list par shared_trip (1 passager par conducteur). Conséquence : on parcourt
    # en parallèle les deux listes (de longueur égale) du dictionnaire passé en paramètre,
    # il faudrait faire deux boucles imbriquées si ce n'était pas le cas. Toutefois à chaque
    # shared_trip sont associées des listes relatives aux passagers (id, noms, prénoms...)
    # comme s'il y avait potentiellement plusieurs passagers par shared_trip.
    #
    # On initialise la liste de dictionnaires sur laquelle va se calquer le modèle du DTO

    startdate_dt = datetime.fromtimestamp(startdate)
    # enddate_dt = datetime.fromtimestamp(enddate)

    return_dict_list = []
    for sht, wtl in zip(shared_trip_and_wtrip_list["shared_trip_list"], shared_trip_and_wtrip_list["wtrip_list_list"]) :
        return_dict = {}
        return_dict["id"] = sht.id
        return_dict["trip_id"] = sht.trip_id
        trip = sht.trip
        # trip = getTripById(sht.trip_id)
        return_dict["trip_driver_id"] = trip.driver_id
        return_dict["event_occurrence_id"] = trip.event_occurrence_id
        return_dict["nb_seats"] = trip.nb_seats
        return_dict["car_label"] = trip.car.label
        return_dict["trip_driver"] = getUserWithNoLastname(trip.driver_id)
        return_dict["driver_score"] = sht.driver_score
        return_dict["passengers_score"] = sht.passengers_score
        return_dict["shared_trip_comment"] = trip.comment
        return_dict["shared_trip_status"] = sht.shared_trip_status
        return_dict["driver_status"] = sht.driver_status
        # Initialisation de la liste itinéraire
        path = []
        for point in sht.path_json :
            path_point = {
                "long" : point[0],
                "lat" : point[1],
                "address" : {
                    "street" : point[2],
                    "name" : point[2],
                    "city" : point[3],
                    "postcode" : point[4],
                    "label" : point[2] + " " + point[4] + " " + point[3],
                    "housenumber" : "",
                },
            }
            # log.info(path_point)
            path.append(path_point)
        return_dict["path"] = path
        # Initialisation de la liste routage
        directions = []
        for point in sht.directions_json :
            directions_point = {"long" : point[0], "lat" : point[1]}
            directions.append(directions_point)
        return_dict["directions"] = directions
        # Initialisation de la liste des détails occupants (yc conducteur)
        # Cette partie fonctionnerait aussi avec de multiples passagers par conducteur
        occ_details_list = []
        for details in sht.occ_details_pickle :
            occ_details = {
                "start_time" : details["start_time"],
                "start_path_index" : details["start_path_index"],
                "arrival_time" : details["arrival_time"],
                "arrival_path_index" : details["arrival_path_index"],
            }
            occ_details_list.append(occ_details)
        return_dict["occ_details_list"] = occ_details_list
        # Initialisation des listes liées aux passagers : when, id, name, surname,
        # status, comment, waiting_trip_id, shared_distance
        occ_when_list, passenger_id_list = [], []
        passenger_list, yacka_points_list, fr_info_list = [], [], []
        passenger_status_list, passenger_comment_list, waiting_trip_id_list = [], [], []
        passenger_nb_pass_list = []
        for wtrip_list in wtl :
            waiting_trip = getWaitingTripById(wtrip_list.waiting_trip_id)
            waiting_trip_id_list.append(waiting_trip.id)
            passenger_id_list.append(waiting_trip.passenger_id)
            passenger_nb_pass_list.append(waiting_trip.nb_passengers)
            passenger_list.append(getUserWithNoLastname(waiting_trip.passenger_id))
            yacka_points_list.append(wtrip_list.yacka_points_amount)
            fr_info_list.append(wtrip_list.fr_info)
            passenger_status_list.append(wtrip_list.passenger_status)
            passenger_comment_list.append(waiting_trip.comment)
            # Construction de la liste des datetimes d'occurrence liée au passager
            when = wtrip_list.pickled_when
            if when.is_recurring :
                # On vérifie que toutes les occurrences de when ne sont pas antérieures
                # à startdate_dt, pour éviter une recherche infructueuse.
                if not when.is_all_before(startdate_dt) :
                    # occ_list = [dt for dt in when.rruleset if startdate_dt <= dt <= enddate_dt]
                    occ_list = [dt for dt in when.rruleset if startdate_dt <= dt]
                    # Si on ne trouve aucune occurrence dans la période startdate, enddate,
                    # on prolonge enddate d'une semaine jusqu'à ce qu'on en trouve au moins une.
                    occ_when_list.append({"occurrence_list" : occ_list})
            else :
                if startdate_dt <= when.dtstart :
                    occ_when_list.append({"occurrence_list" : [when.dtstart]})
        # On affecte ces listes ainsi constituées aux clés du dictionnaire résultat
        return_dict["occ_when_list"] = occ_when_list
        return_dict["passenger_id_list"] = passenger_id_list
        return_dict["passenger_nb_pass_list"] = passenger_nb_pass_list
        return_dict["passenger_list"] = passenger_list
        # return_dict["shared_distance_list"] = shared_distance_list
        return_dict["passenger_status_list"] = passenger_status_list
        return_dict["passenger_comment_list"] = passenger_comment_list
        return_dict["waiting_trip_id_list"] = waiting_trip_id_list
        return_dict["yacka_points_list"] = yacka_points_list
        return_dict["fr_info_list"] = fr_info_list
        return_dict_list.append(return_dict)

    # Trie le dictionnaire obtenu selon le caractère récent exprimé par le statut
    # du shared_trip
    # Cela suppose de déterminer, pour chaque dictionnaire de return_dict_list,
    # le statut pertinent (c'est à dire corresondant à user_id), puis d'appeler rank_status()
    #
    return_dict_list.sort(key = lambda d : rank_status(d["driver_status"] if (d["trip_driver_id"] == user_id)
                                                       else d["passenger_status_list"][0]))
    # Complète le dictionnaire ainsi obtenu par une liste triée d'occurrences de trajets
    # et insère le tout dans la structure adaptée à la vue agenda du frontend
    # filtered_return_dict_list est la liste des shared_trips dont ceux qui sont validés
    # sont dépouillés des infos inutiles
    valid_sht_occ_list, agenda, filtered_return_dict_list = [], [], []
    for i, return_dict in enumerate(return_dict_list) :
        if (return_dict["shared_trip_status"] in bydate_displayable_shared_trip_status_list()) :
            # log.info(return_dict_list[i]["occ_when_list"])
            for occ_when_list in return_dict_list[i]["occ_when_list"] :
                for dt in occ_when_list["occurrence_list"] :
                    valid_sht_occ_list.append((i, dt.timestamp(), dt))
            # dépouillement des infos inutiles pour le frontend
            useful_keys = [
                # "id",
                # "trip_id",
                # "waiting_trip_id_list",
                "trip_driver_id",
                "event_occurrence_id",
                "nb_seats",
                "trip_driver",
                "driver_status",
                "path",
                "directions",
                "occ_details_list",
                "passenger_id_list",
                "passenger_nb_pass_list",
                "passenger_list",
                "passenger_status_list",
                "yacka_points_list",
                "fr_info_list",
                "passenger_comment_list",
                "shared_trip_comment",
                "car_label",
                "driver_score"
            ]
            filtered_dict = {useful_key: return_dict[useful_key] for useful_key in useful_keys}
            filtered_return_dict_list.append(filtered_dict)
        else :
            # s'il ne s'agit pas d'un trajet validé, alors on l'insère dans filtered_return_dict_list
            # après avoir retiré certaines infos confidentielles
            if (return_dict["driver_status"] not in phone_displayable_driver_status_list()) :
                return_dict["trip_driver"].phone = ""
            for p, psg in enumerate(return_dict["passenger_list"]) :
                if (return_dict["passenger_status_list"][p] not in phone_displayable_passenger_status_list()) :
                    psg.phone = ""
            filtered_return_dict_list.append(return_dict)
    if len(valid_sht_occ_list) != 0 :
        agenda_with_index = sorted(valid_sht_occ_list, key=lambda x : x[1])
        agenda = [{"index" : index, "date" : dt} for index, _, dt in agenda_with_index]
    result = {"agenda_indexes" : agenda, "shared_trips" : filtered_return_dict_list}
    # log.info(result)
    return result


def pay_ratio(free_ratio) :
    """ Calcule la proportion à payer en fonction du ratio de gratuité"""
    # On considère que le ration de gratuité indique :
    # - s'il vaut 0 --> que le trajet est entièrement payant
    # - s'il vaut 1 --> que le trajet est à demi payant
    # - s'il vaut 2 --> que le trajet est gratuit
    return (1 - free_ratio / 2)


def list_all_shtrips_by_organization(organization_id, start_time = None, with_directions = False) :
    user_list = users_related_to_organization(organization_id)
    user_id_list = [user.user_id for user in user_list]

    wtrip_lists = (
        db.session.query(Wtrip_list)
        .join(Shared_trip, Shared_trip.id == Wtrip_list.shared_trip_id)
        .join(Trip, Shared_trip.trip_id == Trip.id)
        .join(Waiting_trip, Wtrip_list.waiting_trip_id == Waiting_trip.id)
        .filter(
            (Trip.driver_id.in_(user_id_list)
             | Waiting_trip.passenger_id.in_(user_id_list))
            & Shared_trip.shared_trip_status.notin_(not_alive_status_list())
        )
        .all()
    )
    result_list, status_list, sht_list_list = [], [], []
    # On construit une liste ne reprenant de wtrip_list que les wtrips dont au moins
    # une occurrence est postérieure à start_time, et réarrangée par statut
    for wtl in wtrip_lists :
        if start_time is not None and wtl.pickled_when.is_all_before(start_time) :
            continue
        # on insère le statut du shared_trip dans la liste des statuts (s'il n'y est
        # pas déjà) et on incrémente le nombre d'occurrences associées à ce statut du
        # nbre d'occurrences dans sht_when
        status = wtl.shared_trip.shared_trip_status
        nb_occ = wtl.pickled_when.nb_occurrences()
        try :
            # la méthode index lève une erreur si elle ne trouve rien
            index = status_list.index(status)
            sht_list_list[index].append(
                {
                    "shared_distance" : wtl.shared_distance,
                    "nb_occ" : nb_occ
                }
            )
        except :
            status_list.append(status)
            sht_list_list.append([
                {
                    "shared_distance" : wtl.shared_distance,
                    "nb_occ" : nb_occ
                }
            ])
    # On réarrange les deux listes pour avoir une seule liste résultat indiquant,
    # pour chaque statut, le nombre d'occurrence concernées
    for status, sht_list in zip(status_list, sht_list_list) :
        result_list.append({"sht_status_info" : status, "nb_sht" : len(sht_list), "sht_list" : sht_list})
    # On retourne la liste résultat après l'avoir triée
    if result_list != [] :
        result_list.sort(key = lambda d : rank_status(d["sht_status_info"]))
    return result_list


def list_on_going_shtrips_by_organization(organization_id, with_directions = False) :
    now_dt = datetime.now()
    return list_all_shtrips_by_organization(organization_id, start_time = now_dt, with_directions = with_directions)


def nb_pend_shtrip(shtrip_list) :
    pending_sht_nb_list = [shtrip_list_by_status["nb_sht"] for shtrip_list_by_status in shtrip_list if shtrip_list_by_status["sht_status_info"] == "pending"]
    return 0 if pending_sht_nb_list == [] else pending_sht_nb_list[0]


def nb_halfacc_shtrip(shtrip_list) :
    half_accepted_sht_nb_list = [shtrip_list_by_status["nb_sht"] for shtrip_list_by_status in shtrip_list if shtrip_list_by_status["sht_status_info"] == "half-accepted"]
    return 0 if half_accepted_sht_nb_list == [] else half_accepted_sht_nb_list[0]


def nb_valid_shtrip(shtrip_list) :
    valid_sht_nb_list = [shtrip_list_by_status["nb_sht"] for shtrip_list_by_status in shtrip_list if (shtrip_list_by_status["sht_status_info"] in ["both-accepted", "when-modified"])]
    return 0 if valid_sht_nb_list == [] else sum(valid_sht_nb_list)


def valid_shtrip_mean_distance(shtrip_list) :
    valid_sht_list_list = [shtrip_list_by_status["sht_list"] for shtrip_list_by_status in shtrip_list if (shtrip_list_by_status["sht_status_info"] in ["both-accepted", "when-modified"])]
    if valid_sht_list_list == [] :
        return 0
    sht_distance_list = []
    for valid_sht_list in valid_sht_list_list :
        sht_distance_list += [sht["shared_distance"] for sht in valid_sht_list]
    return (sum(sht_distance_list) / len(sht_distance_list)) / 1000


def halfacc_shtrip_nb_occurrence_mean(shtrip_list) :
    half_accepted_sht_list_list = [shtrip_list_by_status["sht_list"] for shtrip_list_by_status in shtrip_list if shtrip_list_by_status["sht_status_info"] == "half-accepted"]
    if half_accepted_sht_list_list == [] :
        return 0
    nb_occ_list = [sht["nb_occ"] for sht in half_accepted_sht_list_list[0]]
    return int(sum(nb_occ_list) / len(half_accepted_sht_list_list[0]))


def valid_shtrip_nb_occurrence_mean(shtrip_list) :
    valid_sht_list_list = [shtrip_list_by_status["sht_list"] for shtrip_list_by_status in shtrip_list if (shtrip_list_by_status["sht_status_info"] in ["both-accepted", "when-modified"])]
    if valid_sht_list_list == [] :
        return 0
    nb_occ_list = []
    for valid_sht_list in valid_sht_list_list :
        nb_occ_list += [sht["nb_occ"] for sht in valid_sht_list]
    return sum(nb_occ_list) / len(nb_occ_list)
