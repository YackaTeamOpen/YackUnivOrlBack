import logging
from flask import request
from flask_login import login_required, current_user
from flask_restx import Resource


from ..util.dto import CompanyDto
from main.controller.users_controller import onboard_required

from main.service.user_service import getUserById, hasUnreadMessage
from main.service.welcome_message_service import getWelcomeMessage
from main.service.address_service import get_all_user_s_non_deleted_addresses
from main.service.community_service import users_related_to_organization
from main.service.trip_tool_service import (
    list_on_going_trips_by_organization,
    trip_list_est_cumulative_distance,
    trip_list_est_mean_distance,
    trip_list_recurrence_mean,
)
from main.service.shared_trip_service import (
    list_on_going_shtrips_by_organization,
    nb_pend_shtrip,
    nb_halfacc_shtrip,
    nb_valid_shtrip,
    valid_shtrip_mean_distance,
    halfacc_shtrip_nb_occurrence_mean,
    valid_shtrip_nb_occurrence_mean
)

# from main.service.helpers import total_size

log = logging.getLogger(__name__)

api = CompanyDto.api
home_m = CompanyDto.home_company
users_m = CompanyDto.users_company
settings_m = CompanyDto.settings_company
events_m = CompanyDto.events_company


@api.route("/home")
class CompanyHome(Resource):
    @login_required
    @onboard_required
    @api.doc('get company elements')
    @api.response(200, 'Getting company informations.')
    @api.response(401, 'Not authorized.')
    @api.marshal_with(home_m)
    def get(self):
        if current_user.type == 1:
            stats = request.args.get("stats", "")
            statistics = {}
            if stats == "users" :
                statistics["nb_subscribers"] = len(users_related_to_organization(current_user.organization_id))
                firstname_name_list = sorted(
                    [(user_belongs.user.surname, user_belongs.user.name)
                        for user_belongs in users_related_to_organization(current_user.organization_id)],
                    key = lambda x: x[1]
                )
                statistics["subscriber_list"] = [(x[0] + " " + x[1]) for x in firstname_name_list]
            elif stats == "trips" :
                trip_list = list_on_going_trips_by_organization("driver", current_user.organization_id)
                waiting_trip_list = list_on_going_trips_by_organization("passenger", current_user.organization_id)
                statistics["trip_cumulative_distance"] = trip_list_est_cumulative_distance(trip_list)
                statistics["waiting_trip_cumulative_distance"] = trip_list_est_cumulative_distance(waiting_trip_list)
                statistics["trip_mean_distance"] = trip_list_est_mean_distance(trip_list)
                statistics["waiting_trip_mean_distance"] = trip_list_est_mean_distance(waiting_trip_list)
                statistics["trip_nb_occurrence_mean"] = trip_list_recurrence_mean(trip_list)
                statistics["waiting_trip_nb_occurrence_mean"] = trip_list_recurrence_mean(waiting_trip_list)
                statistics["atcf_trip_list"] = trip_list
                statistics["atcf_waiting_trip_list"] = waiting_trip_list
            elif stats == "shtrips" :
                shtrip_list = list_on_going_shtrips_by_organization(current_user.organization_id)
                # log.info("size of shtrip_list : {}".format(total_size(shtrip_list)))
                statistics["shtrip_list"] = shtrip_list
                # for sht_list in shtrip_list :
                #     print("sht_status: {}, nb_sht: {}, len('sht_list'): {}".format(sht_list["sht_status_info"], sht_list["nb_sht"], len(sht_list["sht_list"])))
                statistics["nb_pend_shtrip"] = nb_pend_shtrip(shtrip_list)
                statistics["nb_halfacc_shtrip"] = nb_halfacc_shtrip(shtrip_list)
                statistics["nb_valid_shtrip"] = nb_valid_shtrip(shtrip_list)
                statistics["valid_shtrip_mean_distance"] = valid_shtrip_mean_distance(shtrip_list)
                statistics["halfacc_shtrip_nb_occurrence_mean"] = halfacc_shtrip_nb_occurrence_mean(shtrip_list)
                statistics["valid_shtrip_nb_occurrence_mean"] = valid_shtrip_nb_occurrence_mean(shtrip_list)

            user = getUserById(current_user.id, withOrganization=True)
            welcome_msg = getWelcomeMessage(current_user.id)
            has_unread_message = hasUnreadMessage(current_user.id)

            resp = {
                "user": user,
                "stats": statistics if (stats in ["users", "trips", "shtrips", "shtripswithdir"]) else None,
                "welcome_msg": welcome_msg,
                "has_unread_message": has_unread_message
            }
            resp["status"] = "success"
            resp["message"] = "Getting company information"
            return resp, 200
        else:
            return {"status": "fail", "message": "Need to connect first"}, 401


@api.route('/menu')
class CompanyMenu(Resource):
    @login_required
    @onboard_required
    @api.doc('get company menu')
    @api.response(200, 'Getting company menu')
    @api.response(401, 'Unauthorized.')
    # Return nothing inparticular - just check login and onboard are ok
    def get(self):
        return {}, 200


@api.route("/settings")
class CompanySettings(Resource):
    @login_required
    @onboard_required
    @api.doc('get company settings')
    @api.response(200, 'Getting settings of company .')
    @api.response(401, 'Not authorized.')
    @api.marshal_with(settings_m)
    def get(self):
        if current_user.type == 1:
            user = getUserById(current_user.id)
            addresses = get_all_user_s_non_deleted_addresses(current_user.id)
            resp = {"user": user, "addresses": addresses}
            resp["status"] = "success"
            resp["message"] = "Getting settings of company "
            return resp, 200
        else:
            return {"status": "fail", "message": "Need to connect first"}, 401


@api.route("/addresses")
class CompanyAddresses(Resource):
    @login_required
    @onboard_required
    @api.doc('get company addresses')
    @api.response(200, 'Getting addresses of company .')
    @api.response(401, 'Not authorized.')
    @api.marshal_with(settings_m)
    def get(self):
        if current_user.type == 1:
            addresses = get_all_user_s_non_deleted_addresses(current_user.id)
            resp = {"addresses": addresses}
            resp["status"] = "success"
            resp["message"] = "Getting addresses of company "
            return resp, 200
        else:
            return {"status": "fail", "message": "Need to connect first"}, 401
