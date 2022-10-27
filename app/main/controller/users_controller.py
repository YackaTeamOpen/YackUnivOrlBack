import json
from flask import Response, request
from flask_login import login_required,current_user
from flask_restx import Resource
from functools import wraps
import logging

from .. import login_manager
from ..util.dto import UsersDto

from main.service.address_service import get_all_user_s_non_deleted_addresses
from main.service.car_service import getAllCarByUser
#from main.service.history_service import getHistoryByUser
# from main.service.pref_service import getAllMusicPref, getAllSmokingPref, getAllSpeakingPref
from main.service.problem_service import getAllProblem
from main.service.trip_service import getUserTrips, getUserTripCount
from main.service.user_service import getUserById, hasUnreadMessage, new_problem
from main.service.welcome_message_service import getWelcomeMessage
from main.service.waiting_trip_service import getUserWaitingTrips, getUserWaitingTripCount

log = logging.getLogger(__name__)
api = UsersDto.api
home_m = UsersDto.home_users
user_trips_m = UsersDto.user_trips
user_trip_counts_m = UsersDto.user_trip_counts
profile_m = UsersDto.profile_users
settings_m = UsersDto.settings_users
# search_m = UsersDto.search_users
#history_m = UsersDto.history_users

def onboard_required(f) :
  """ A decorator to check if the user went through the onboarding process """
  @wraps(f)
  def decorated_function(*args, **kwargs) :
    if current_user.last_login :
      return f(*args, **kwargs)
    else:
      return {"status":"fail","message":"Need to process onboarding"}, 403
  return decorated_function


@api.route("/home")
class UsersHome(Resource):
  @login_required
  @onboard_required
  @api.doc('get user elements')
  @api.response(200, 'Getting users information')
  @api.response(401, 'Unauthorized.')
  @api.marshal_with(home_m)
  def get(self):
    if current_user.type in [2, 4]:
      user = getUserById(current_user.id)
      welcome_msg =  getWelcomeMessage(current_user.id)
      has_unread_message = hasUnreadMessage(current_user.id)
      resp = {"user":user, "welcome_msg":welcome_msg, "has_unread_message":has_unread_message}
      resp["status"] = "success"
      resp["message"] = "Getting users information"
      return resp,200
    else:
      return {"status":"fail","message":"Need to connect first"},401

@api.route("/trips")
class UsersTrips(Resource):
  @login_required
  @onboard_required
  @api.doc('get user configurated trips')
  @api.response(200, 'Getting users trips')
  @api.response(401, 'Unauthorized.')
  @api.marshal_with(user_trips_m)
  def get(self):
    if current_user.type in [2, 4]:
      user = getUserById(current_user.id)
      waiting_trips = getUserWaitingTrips(current_user.id)
      trips = getUserTrips(current_user.id)
      resp = {"user":user, "trips": trips, "waiting_trips": waiting_trips}
      resp["status"] = "success"
      resp["message"] = "Getting users trips"
      return resp,200
    else:
      return {"status":"fail","message":"Need to connect first"},401

@api.route("/tripcounts")
class UsersTripcounts(Resource):
  @login_required
  @onboard_required
  @api.doc('get user configurated trip count')
  @api.response(200, 'Getting users trips')
  @api.response(401, 'Unauthorized.')
  @api.marshal_with(user_trip_counts_m)
  def get(self):
    if current_user.type in [2, 4]:
      waiting_trip_count = getUserWaitingTripCount(current_user.id)
      trip_count = getUserTripCount(current_user.id)
      resp = {"trip_count": trip_count, "waiting_trip_count": waiting_trip_count}
      resp["status"] = "success"
      resp["message"] = "Getting users trip counts"
      return resp,200
    else:
      return {"status":"fail","message":"Need to connect first"},401

@api.route('/profile')
class UsersProfile(Resource):
  @login_required
  @onboard_required
  @api.doc('get user settings')
  @api.response(200, 'Getting users settings')
  @api.response(401, 'Unauthorized.')
  @api.marshal_with(profile_m)
  def get(self):
    if current_user.type in [2, 4]:
      user = getUserById(current_user.id)
      # The following is not used any more by the frontend
      # photo = get_photo(current_user.id)
      # music = getAllMusicPref()
      # smoke = getAllSmokingPref()
      # speaking = getAllSpeakingPref()
      # resp = {"user":user, "photo": photo, "music":music, "smoke":smoke,"speaking":speaking}
      resp = {"user":user}
      resp["status"] = "success"
      resp["message"] = "Getting users settings"
      return resp,200
    else:
      return {"status":"fail","message":"Need to connect first"},401

@api.route('/settings')
class UsersSettings(Resource):
  @login_required
  @onboard_required
  @api.doc('get user settings')
  @api.response(200, 'Getting users settings')
  @api.response(401, 'Unauthorized.')
  @api.marshal_with(settings_m)
  def get(self):
    if current_user.type in [2, 4]:
      user = getUserById(current_user.id)
      cars = getAllCarByUser(current_user.id)
      addresses = get_all_user_s_non_deleted_addresses(current_user.id)
      resp = {"user":user, "cars":cars, "addresses":addresses}
      resp["status"] = "success"
      resp["message"] = "Getting users settings"
      return resp,200
    else:
      return {"status":"fail","message":"Need to connect first"},401


@api.route('/menu')
class UsersMenu(Resource):
  @login_required
  @onboard_required
  @api.doc('get user menu')
  @api.response(200, 'Getting users menu')
  @api.response(401, 'Unauthorized.')
  # Return nothing inparticular - just check login and onboard are ok
  def get(self):
    return {}, 200


@api.route('/problem')
class UsersProblem(Resource):
  @login_required
  @onboard_required
  @api.doc('Post a problem on the app')
  @api.response(200, 'Problem sent')
  @api.response(400, 'Error with points.')
  @api.response(401, 'Unauthorized.')
  @api.param('start[]', 'Start address')
  @api.param('arrival[]', 'Arrival address')
  @api.param('nb_waypoints', 'Number of waypoints')
  @api.param('waypoints[]', 'Waypoint')
  def post(self):
    if current_user.type in [1, 2, 4]:
      data = request.form
      waypoints = []
      comment = data["comment"]
      resp = new_problem(current_user.id, comment)
      return resp,200
    else:
      return {"status":"fail","message":"Need to connect first"},401

