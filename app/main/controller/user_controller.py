from flask import request
from flask_login import login_required, current_user
from flask_restx import Resource
import logging

from ..util.dto import UserDto
from ..service.user_service import (
    update_user,
    getUserById,
)
from main.service.onboard_service import onboard_user

log = logging.getLogger(__name__)
api = UserDto.api
user_m = UserDto.user
get_user_m = UserDto.get_user


# Could be a more secure alternative to the initial route definition...
@api.route("/")
class User2(Resource):
    @login_required
    @api.doc("update user")
    @api.response(200, "User successfully updated.")
    @api.response(401, "Unauthorized.")
    @api.param("gender", "Gender")
    @api.param("name", "Name")
    @api.param("surname", "Surname")
    @api.param("email", "email")
    @api.param("phone", "Phone")
    @api.param("birthdate", "Birthdate millisecond")
    @api.marshal_with(user_m)
    def put(self):
        try:
            data = request.form.to_dict()
            return update_user(current_user.id, data)
        except Exception as e:
            log.exception(e, exc_info=True)
            return {"status": "fail", "message": "Error"}, 500


@api.route("/<int:user_id>")
class User(Resource):
    @login_required
    @api.doc("update user")
    @api.response(200, "User successfully updated.")
    @api.response(401, "Unauthorized.")
    @api.param("gender", "Gender")
    @api.param("name", "Name")
    @api.param("surname", "Surname")
    @api.param("email", "email")
    @api.param("phone", "Phone")
    @api.param("birthdate", "Birthdate millisecond")
    @api.marshal_with(user_m)
    def put(self, user_id):
        try:
            data = request.form.to_dict()
            return update_user(user_id, data)
        except Exception as e:
            log.exception(e, exc_info=True)
            return {"status": "fail", "message": "Error"}, 500

    @login_required
    @api.doc("get user")
    @api.marshal_with(get_user_m)
    def get(self, user_id):
        try:
            user = getUserById(user_id)
            resp = {"user": user}
            resp["status"] = "success"
            resp["message"] = "Getting user information"
            return resp, 200
        except Exception as e:
            log.exception(e, exc_info=True)
            return {"status": "fail", "message": "Error"}, 500


@api.route("/onboard")
class OnboardUser(Resource):
    @api.doc("update new user")
    @api.response(201, "User successfully created.")
    @api.response(400, "Something wrong with parameters.")
    @api.response(401, "Unauthorized.")
    @api.param("name", "Name")
    @api.param("surname", "Surname")
    @api.param("phone", "Phone")
    @api.param("photo", "Photo")
    @api.param("aboutme", "aboutme")
    @api.param("music_pref", "music_pref")
    @api.param("smoking_pref", "smoking_pref")
    @api.param("speaking_pref", "speaking_pref")
    @api.param("public_phone", "public_phone")
    @api.param("gender", "gender")
    @login_required
    def post(self):
        try:
            data = request.form.to_dict()
            user_id = current_user.id
            return onboard_user(user_id, data)
        except Exception as e:
            log.exception(e, exc_info=True)
            return {"status": "fail", "message": "Error"}, 500

