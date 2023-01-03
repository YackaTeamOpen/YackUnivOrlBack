from flask import request
from flask_login import login_required, current_user
from flask_restx import Resource
import logging

from main.model.proof_of_travel import Proof_of_travel
from main.util.dto import ProofOfTravelDto
from main.service.proof_of_travel_service import (
    createProof,
    validateProof,
    getProofById
)

log = logging.getLogger(__name__)
api = ProofOfTravelDto.api


# @api.route("/")
# class AllProofs(Resource):
#     @login_required
#     @api.response(200, "List of proofs.")
#     @api.response(401, "Unauthorized.")
#     def get(self):
#         """Récupération de toutes les preuves de covoiturage"""
#         pass


@api.route("/create")
class ProofOfTravel(Resource):
    @login_required
    # @api.response(201, "Proof successfully created.")
    # @api.response(409, "Already created")
    @api.response(401, "Unauthorized.")
    def post(self):
        """Création d'une preuve de covoiturage"""
        return {}, 201


@api.route("/<int:proof_of_travel_id>")
class ProofOfTravel2(Resource):
    @login_required
    @api.response(200, "Here is the proof.")
    @api.response(401, "Unauthorized.")
    def get(self, proof_of_travel_id):
        """Récupération d'une preuve de covoiturage avec l'id associé"""

        return {}, 200

    @login_required
    @api.response(200, "Proof successfully updated.")
    @api.response(401, "Unauthorized.")
    def put(self, proof_of_travel_id):
        """Modification d'une preuve de covoiturage avec l'id associé"""
        pass


@api.route("/<int:community_id>/counts/<int:user_id>")
class ProofsCountByUserComp(Resource):
    @login_required
    @api.response(200, "Total proofs validated by the user.")
    @api.response(401, "Unauthorized.")
    def get(self, community_id, user_id):
        """Récupération du total de voyages prouvés par les utilisateurs faisant partie d'une entreprise"""
        return {}, 200


@api.route("/<int:community_id>/counts/<int:user_id>/driver")
class ProofsCountByDriverComp(Resource):
    @login_required
    @api.response(200, "Total proofs validated by the user as a driver.")
    @api.response(401, "Unauthorized.")
    def get(self, community_id, user_id):
        """Récupération du total de voyages prouvés en tant que conducteur pour les utilisateurs faisant partie d'une entreprise"""
        return {}, 200


@api.route("/<int:community_id>/counts/<int:user_id>/passenger")
class ProofsCountByPassengerComp(Resource):
    @login_required
    @api.response(200, "Total proofs validated by the user as a passenger.")
    @api.response(401, "Unauthorized.")
    def get(self, community_id, user_id):
        """Récupération du total de voyages prouvés en tant que passager pour les utilisateurs faisant partie d'une entreprise"""
        return {}, 200

