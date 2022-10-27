# Modifié par Olivier pour ajouter le namespace shared_trip_ns - Janvier 2021
from flask_restx import Api
from flask import Blueprint

from main.controller.general_controller import api as general_ns
from main.controller.users_controller import api as users_ns
from main.controller.companies_controller import api as companies_ns

# from main.controller.address_controller import api as address_ns
# from main.controller.car_controller import api as car_ns
# from main.controller.report_controller import api as report_ns
# from main.controller.review_controller import api as review_ns
from main.controller.trip_controller import api as trip_ns
# from main.controller.trip_request_controller import api as trip_request_ns
from main.controller.message_controller import api as message_ns
from main.controller.welcome_msg_controller import api as welcome_msg_ns
from main.controller.shared_trip_controller import api as shared_trip_ns
# from main.controller.test_controller import api as test_ns
# from main.controller.community_controller import api as community_ns
# from main.controller.event_controller import api as event_ns

from main.util.dto import OrganizationDto as organization_ns
from main.util.dto import BillDto as bill_ns
from main.util.dto import MusicPrefDto as music_pref_ns
from main.util.dto import SpeakingPrefDto as speaking_pref_ns
from main.util.dto import SmokingPrefDto as smoking_pref_ns
from main.util.dto import ProblemDto as problem_ns


from main.controller.user_controller import api as user_ns

blueprint = Blueprint('api',__name__)
api = Api(blueprint,title='Yacka - API',version='0.2',description="API privée pour l'application Yacka")

api.add_namespace(general_ns,path='/')
api.add_namespace(users_ns,path='/users')
api.add_namespace(companies_ns,path='/companies')

# api.add_namespace(address_ns,path="/address")
api.add_namespace(bill_ns.api,path="/bill")
# api.add_namespace(car_ns,path="/car")
api.add_namespace(music_pref_ns.api,path="/music_pref")
api.add_namespace(organization_ns.api,path="/organization")
api.add_namespace(problem_ns.api,path="/organization")
# api.add_namespace(report_ns,path="/report")
# api.add_namespace(review_ns,path="/review")
api.add_namespace(speaking_pref_ns.api,path="/speaking_pref")
api.add_namespace(smoking_pref_ns.api,path="/smoking_pref")
api.add_namespace(trip_ns,path="/trip")
api.add_namespace(user_ns,path="/user")
api.add_namespace(message_ns,path="/message")
api.add_namespace(welcome_msg_ns,path="/welcome-msg")
api.add_namespace(shared_trip_ns,path="/shared_trip")
# api.add_namespace(test_ns,path="/test")
# api.add_namespace(event_ns,path="/event")
# api.add_namespace(community_ns,path="/community")
