from flask import request
from flask_login import login_required, current_user
from flask_restx import Resource
import logging

from ..util.dto import TripDto

# from main.service.photo.photo_uploader import get_photo

# from main.service.maptools.utils import decode_trip_polyline
from main.service.trip_tool_service import get_trip_waiting_trip_list
from main.service.trip_service import getTripById
from main.service.waiting_trip_service import getWaitingTripById

log = logging.getLogger(__name__)
api = TripDto.api
_trip = TripDto.trip
_reduced_trips_and_wtrips = TripDto.reduced_trips_and_wtrips


@api.route("/<int:trip_id>")
class Trip(Resource):
    @login_required
    @api.doc('get trip or waiting trip')
    @api.marshal_with(_trip)
    @api.response(401, 'Unauthorized.')
    @api.response(200, 'Trip successfully returned.')
    @api.param('role', 'Query string arg, role of the trip owner : "driver" or "passenger"')
    def get(self, trip_id):
        role = request.args.get("role", "driver")
        trip = (getTripById(trip_id) if role == "driver"
                else getWaitingTripById(trip_id))
        if (trip is None or trip.state != 2) :
            return {}, 204
        trip_user_id = (trip.driver_id if role == "driver"
                        else trip.passenger_id)
        if ((trip_user_id != current_user.id) and (current_user.type != 4)) :
            return {"status": "fail", "message": "Unauthorized"}, 401
        else:
            return trip, 200


@api.route("/getalltrips")
class AllTrips(Resource):
    @login_required
    @api.response(200, "Trip and waiting_trip list as requested.")
    @api.response(204, "Empty trip/waiting_trip list.")
    @api.response(401, 'Unauthorized.')
    @api.doc("list_of_all_trips_and_waiting_trips")
    @api.marshal_with(_reduced_trips_and_wtrips, envelope="trips")
    def get(self):
        # Pour l'utilisateur de type 4 seulement
        if (current_user.type != 4) :
            return {"status": "fail", "message": "Unauthorized"}, 401
        """List trips"""
        trip_waiting_trip_list = get_trip_waiting_trip_list()
        # print("trip_waiting_trip_list : {}".format(trip_waiting_trip_list))
        return trip_waiting_trip_list, 200
