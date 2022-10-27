import json
from flask import Response, request
from flask_login import login_required,current_user
from flask_restx import Resource

from main.controller.users_controller import onboard_required
from ..util.dto import MessageDto
from ..service.message_service import create_new_message,get_message,get_conversations

api = MessageDto.api

conversation_m = MessageDto.conversation
conversation_list_m = MessageDto.conversations

@api.route("/conv/<int:user_id>")
class ConvMessage(Resource):
  @login_required
  @onboard_required
  @api.doc('get messages between specified user and current user')
  @api.marshal_with(conversation_m)
  def get(self, user_id):
    data = request.form
    return get_message(user_id)

@api.route("/conv/list")
class ConvMessageList(Resource):
  @login_required
  @onboard_required
  @api.doc('get list of conversations of the current user')
  @api.marshal_with(conversation_list_m)
  def get(self):
    return get_conversations(current_user.id)

@api.route("/create")
class CreateMessage(Resource):
  @login_required
  @api.doc('create new message')
  def post(self):
    data = request.form
    return create_new_message(data)
