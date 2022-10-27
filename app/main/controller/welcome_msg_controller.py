import json
from flask import Response, request
from flask_login import login_required,current_user
from flask_restx import Resource

from .. import login_manager
from ..util.dto import WelcomeMessageDto
from ..service.welcome_message_service import delete_welcome_msg,create_new_welcome_msg,get_all_welcome_msg

api = WelcomeMessageDto.api
all_wmsg_m = WelcomeMessageDto.all_wmsg_m

@api.route("/<int:welcome_msg_id>")
class WelcomeMessage(Resource):
    @login_required
    @api.doc('delete welcome_msg')
    def delete(self,welcome_msg_id):
        data = request.form
        return delete_welcome_msg(welcome_msg_id,data)

@api.route("/create")
class CreateWelcomeMessage(Resource):
    @login_required
    @api.doc('create new welcome_msg')
    def post(self):
        data = request.form
        return create_new_welcome_msg(data)

@api.route("/all")
class AllWelcomeMessage(Resource):
    @login_required
    @api.doc('get all welcome_msg')
    @api.marshal_with(all_wmsg_m)
    def get(self):
        data = request.form
        return get_all_welcome_msg(data)

# Remplacer welcome_msg ==> "nom_de_la_table"
# Remplacer WelcomeMessage ==> "Nom_de_la_table"
