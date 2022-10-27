# Contrôleur définissant les endpoints de création et de manipulation des shared_trip
# Olivier - Janvier 2021
#
# Comporte les actions suivantes :
#
# - Création d'une liste de shared_trip à partir d'un trip conducteur, pour
#   proposition à ce dernier
# - Création d'une liste de shared_trip à partir d'un waiting_trip passager,
#   pour proposition à ce dernier
# - Suppression d'un shared_trip (pas retenu par un des protagonistes, ou plus
#   pertinent, par ex. suppression du trip ou d'un des waiting_trip relatifs)
# - Modification d'un shared_trip (ex.: un des passagers décline la proposition,
#   le shared_trip doit être recalculé sans lui, ou encore le conducteur modifie
#   ses disponibilités)
# - Liste les shared_trip relatifs à un conducteur ou un passager (vue agenda)
#
import time
from flask import request
from flask_restx import Resource
from flask_login import login_required, current_user


from main.config import environments, config_name
from main.util.dto import Shared_tripDto
from main.service.shared_trip_service import (
    get_shared_trips_per_user,
    get_a_shared_trip,
    build_shtl_response_for_dto,
    build_shtl_response_for_agenda_dto
)

# from main.service.maptools.utils import convertAddIntoLatLong


api = Shared_tripDto.api
_shared_trip = Shared_tripDto.shared_trip
_sht_update_info = Shared_tripDto.sht_update_info
_polyline_details = Shared_tripDto.polyline_details
agenda_home = Shared_tripDto.agenda_home


@api.route("/<int:shared_trip_id>")
class SharedTrip(Resource):
    @login_required
    @api.response(200, "Shared_trip returned as requested.")
    @api.response(204, "Shared_trip non existent.")
    @api.response(401, 'Unauthorized.')
    @api.doc("get a shared_trip")
    @api.marshal_with(_shared_trip, envelope="data")
    def get(self, shared_trip_id):
        """Return the requested shared_trip in a DTO-compliant shape"""
        shared_trip_and_wtrip_list = get_a_shared_trip(shared_trip_id)
        if shared_trip_and_wtrip_list is None:
            return {}, 204
        else:
            # On teste si le shared_trip est bien relatif au current user
            #
            if ((shared_trip_and_wtrip_list["shared_trip_list"][0].trip.driver_id != current_user.id)
                    and (shared_trip_and_wtrip_list["wtrip_list_list"][0][0].waiting_trip.passenger_id != current_user.id)) :
                return {"status": "fail", "message": "Unauthorized"}, 401
            #
            # Par défaut build_shtl_response_for_dto retourne une liste de
            # dictionnaires. Dans ce cas précis on ne retourne qu'un élément,
            # donc on prend le seul dictionnaire de la liste renvoyée.
            return build_shtl_response_for_dto(shared_trip_and_wtrip_list)[0], 200


@api.route("/getshtlpu/agenda")
class SharedTripListPerUserAgenda(Resource):
    @login_required
    @api.response(200, "Shared_trip list as requested.")
    @api.response(204, "Empty shared_trip list.")
    @api.doc("list_of_shared_trips_per_user")
    @api.param(
        "startdate",
        "(facultatif) date à laquelle les voyages doivent être pris en compte (par défaut : maintenant)",
    )
    @api.marshal_list_with(agenda_home, envelope="agenda")
    def get(self):
        """List shared_trips related to a specific user"""
        startdate = int(request.args.get("startdate", time.time()))
        shared_trip_and_wtrip_list = get_shared_trips_per_user(current_user.id)
        if shared_trip_and_wtrip_list is None:
            return {}, 204
        else:
            return (
                build_shtl_response_for_agenda_dto(
                    shared_trip_and_wtrip_list, current_user.id, startdate
                ),
                200,
            )
