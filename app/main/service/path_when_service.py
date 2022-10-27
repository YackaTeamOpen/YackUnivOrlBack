# Définit les fonctions permettant à l'API de manipuler les objets Yacka_when,
# de filtrer les trajets désirés et proposés avant la recherche de correspondance,
# et de rechercher les meilleurs trajets correspondants.
# Olivier - Janvier 2021
#
from math import sqrt, exp

from main.config import environments, config_name
from main.service.path_matching_service import Path_point


def as_the_crow_flies_to_real_distance(as_the_crow_flies_distance) :
    # Convertit une distance à vol d'oiseau en une estimation d'une distance réelle
    # parcourue par un véhicule automobile.
    # Utilise les conclusions d'études menées sur le sujet (source :
    # https://www.cairn.info/revue-flux1-2009-2-page-110.htm)
    return (as_the_crow_flies_distance * (1.1 + 0.3 * exp(- as_the_crow_flies_distance / 20)))


def estimate_real_distance_between(start_pp, arrival_pp) :
    # Calcule une estimation de la distance réelle parcourue par un véhicule
    # à partir des points de départ et d'arrivée, en convertissant
    # donc la distance à vol d'oiseau entre ces deux points en une distance
    # réelle.
    # Permet d'éviter de calculer et de stocker les distances réelles des trips
    # et waiting_trip, dont on a a priori pas besoin puisque ces trajets ne sont
    # jamais effectués tels quels lors du covoiturage, étant déviés par ce dernier.
    # Cette fonction est destinée à donner aux "organizations" une estimation du
    # nb de km proposés ou demandés au partage par leurs membres.
    lat_to_meters = environments[config_name]["lat_to_meters"]
    long_to_meters = environments[config_name]["long_to_meters"]
    x_trip_distance = (arrival_pp.longitude - start_pp.longitude) * long_to_meters
    y_trip_distance = (arrival_pp.latitude - start_pp.latitude) * lat_to_meters
    as_the_crow_flies_distance = sqrt(x_trip_distance ** 2 + y_trip_distance ** 2)
    estimated_real_distance = as_the_crow_flies_to_real_distance(as_the_crow_flies_distance)
    return estimated_real_distance


def make_path_point_tuple_from_trip(trip) :
    start_point = Path_point(
        street = trip.start_address.street,
        city = trip.start_address.city,
        zipcode = trip.start_address.zipcode,
        latitude = trip.start_address.latitude,
        longitude = trip.start_address.longitude
    )
    arrival_point = Path_point(
        street = trip.arrival_address.street,
        city = trip.arrival_address.city,
        zipcode = trip.arrival_address.zipcode,
        latitude = trip.arrival_address.latitude,
        longitude = trip.arrival_address.longitude
    )
    return (start_point, arrival_point)
