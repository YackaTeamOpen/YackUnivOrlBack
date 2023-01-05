# Modifié par Olivier pour ajouter le Shared_tripDto - Janvier 2021
from flask_restx import Namespace, fields

# from numpy.core.numeric import require ???

### READ ONLY CLASSES

## PREFERENCES
class MusicPrefDto:
    api = Namespace("/music_pref", description="Music_pref endpoints")
    music_pref = api.model(
        "music_pref",
        {
            "id": fields.String(required=True, description="music_pref id"),
            "label": fields.String(required=True, description="music_pref label"),
        },
    )


class SmokingPrefDto:
    api = Namespace("/smoking_pref", description="Smoking_pref endpoints")
    smoking_pref = api.model(
        "smoking_pref",
        {
            "id": fields.String(required=True, description="smoking_pref id"),
            "label": fields.String(required=True, description="smoking_pref label"),
        },
    )


class SpeakingPrefDto:
    api = Namespace("/speaking_pref", description="Speaking_pref endpoints")
    speaking_pref = api.model(
        "speaking_pref",
        {
            "id": fields.String(required=True, description="speaking_pref id"),
            "label": fields.String(required=True, description="speaking_pref label"),
        },
    )


## PROBLEM
class ProblemDto:
    api = Namespace("/problem", description="Problem endpoint")
    problem = api.model(
        "problem",
        {
            "id": fields.String(required=True, description="problem id"),
            "comment": fields.String(required=True, description="problem comment"),
        },
    )


## TRUNK
class TrunkDto:
    api = Namespace("/trunk", description="Trunk endpoints")
    trunk = api.model(
        "trunk",
        {
            "id": fields.String(required=True, description="trunk id"),
            "label": fields.String(required=True, description="trunk label"),
        },
    )


## READ/WRITE CLASSES


class BillDto:
    api = Namespace("/bill", description="Bill endpoints")
    bill = api.model(
        "bill",
        {
            "id": fields.String(required=True, description="bill id"),
            "price": fields.String(required=True, description="smoking_pref label"),
            "nb_max_employees": fields.String(
                required=True, description="nb_max_employees label"
            ),
        },
    )
    bill_for_company = api.model(
        "bill",
        {
            # "id": fields.String(required=True, description="bill id"),
            # "price": fields.String(required=True, description="smoking_pref label"),
            "nb_max_employees": fields.String(
                required=True, description="nb_max_employees label"
            ),
        },
    )


class OrganizationDto:
    api = Namespace("/organization", description="Organization endpoints")
    organization = api.model(
        "organization",
        {
            # "id": fields.String(required=True, description="organization id"),
            "name": fields.String(required=True, description="organization name"),
            # "siret": fields.String(required=True, description="organization siret"),
            # "address": fields.String(required=True, description="organization address"),
            # "creation_date": fields.String(
            #     required=True, description="organization creation_date"
            # ),
            # "bill": fields.Nested(BillDto.bill),
        },
    )
    organization_for_company = api.model(
        "organization",
        {
            # "id": fields.String(required=True, description="organization id"),
            "name": fields.String(required=True, description="organization name"),
            # "siret": fields.String(required=True, description="organization siret"),
            # "address": fields.String(required=True, description="organization address"),
            # "creation_date": fields.String(
            #     required=True, description="organization creation_date"
            # ),
            "bill": fields.Nested(BillDto.bill_for_company),
        },
    )


class CommunityDto:
    api = Namespace("/community", description="Community endpoints")
    community = api.model(
        "community",
        {
            "id": fields.String(required=True, description="community id"),
            "name": fields.String(required=True, description="community name"),
        },
    )

    communities = api.model(
        "communities", {"communities": fields.List(fields.Nested(community))}
    )

class UserDto:
    api = Namespace("/user", description="User endpoints")
    user = api.model(
        "user",
        {
            "id": fields.String(required=True, description="user id"),
            "type": fields.String(required=True, description="user type"),
            "gender": fields.String(required=True, description="user gender"),
            "name": fields.String(required=True, description="user name"),
            "surname": fields.String(required=True, description="user surname"),
            "email": fields.String(required=True, description="user email"),
            "phone": fields.String(required=True, description="user phone"),
            "aboutme": fields.String(required=True, description="user aboutme"),
            "organization": fields.Nested(OrganizationDto.organization),
            "speaking_pref": fields.Nested(SpeakingPrefDto.speaking_pref),
            "smoking_pref": fields.Nested(SmokingPrefDto.smoking_pref),
            "music_pref": fields.Nested(MusicPrefDto.music_pref),
            "points": fields.String(required=True, description="user points"),
            "last_login": fields.String(required=True, description="user last_login"),
            "unsubscribe": fields.String(required=True, description="user unsubscribe"),
            "birthdate": fields.String(required=True, description="user birthdate"),
            "creation_date": fields.String(
                required=True, description="user creation date"
            ),
            "photo": fields.String(
                required=True, description="photo of user base64 encoded"
            ),
            "current_points": fields.Float(
                required=True, description="yacka points fo the user", default=0
            ),
            "communities": fields.List(
                fields.Nested(CommunityDto.community), default=list(), description="Communities of the user"
            )
        },
    )
    get_user = api.model("get_user", {"user": fields.Nested(user)})
    user_private = api.model(
        "user_private",
        {
            "id": fields.String(required=True, description="user id"),
            "gender": fields.String(required=True, description="user gender"),
            "name": fields.String(required=True, description="user name"),
            "surname": fields.String(required=True, description="user surname"),
            "aboutme": fields.String(required=True, description="user aboutme"),
            "speaking_pref": fields.Nested(SpeakingPrefDto.speaking_pref),
            "smoking_pref": fields.Nested(SmokingPrefDto.smoking_pref),
            "music_pref": fields.Nested(MusicPrefDto.music_pref),
            "photo": fields.String(
                required=True, description="photo of user base64 encoded"
            ),
        },
    )
    user_private_with_phone = api.model(
        "user_private_with_phone",
        {
            "id": fields.String(required=True, description="user id"),
            "gender": fields.String(required=True, description="user gender"),
            "name": fields.String(required=True, description="user name"),
            "surname": fields.String(required=True, description="user surname"),
            "phone": fields.String(required=True, description="user phone"),
            "aboutme": fields.String(required=True, description="user aboutme"),
            "speaking_pref": fields.Nested(SpeakingPrefDto.speaking_pref),
            "smoking_pref": fields.Nested(SmokingPrefDto.smoking_pref),
            "music_pref": fields.Nested(MusicPrefDto.music_pref),
            "photo": fields.String(
                required=True, description="photo of user base64 encoded"
            ),
            "communities": fields.List(
                fields.Nested(CommunityDto.community), default=list(), description="Communities of the user"
            )
        },
    )
    user_for_company = api.model(
        "user_for_company",
        {
            # "id": fields.String(required=True, description="user id"),
            # "gender": fields.String(required=True, description="user gender"),
            "name": fields.String(required=True, description="user name"),
            "surname": fields.String(required=True, description="user surname"),
            "phone": fields.String(required=True, description="user phone"),
            "organization": fields.Nested(OrganizationDto.organization_for_company),
            "aboutme": fields.String(required=True, description="user aboutme"),
            "photo": fields.String(
                required=True, description="photo of user base64 encoded"
            ),
        },
    )


class AddressDto:
    api = Namespace("/address", description="Address endpoints")
    address = api.model(
        "address",
        {
            "id": fields.String(required=True, description="address id"),
            "street": fields.String(required=True, description="street"),
            "city": fields.String(required=True, description="city"),
            "zipcode": fields.String(required=True, description="zipcode"),
            "latitude": fields.String(required=True, description="latitude"),
            "longitude": fields.String(required=True, description="longitude"),
        },
    )

    cvlatlng_structure = api.model(
        "cvlatlng_structure",
        {
            "label": fields.String(required=True, description="address label"),
            "housenumber": fields.String(
                required=True, description="address housenumber"
            ),
            "name": fields.String(required=True, description="address name"),
            "postcode": fields.String(required=True, description="address postcode"),
            "city": fields.String(required=True, description="address city"),
            "street": fields.String(required=True, description="address street"),
        },
    )


class CarDto:
    api = Namespace("/car", description="Car endpoints")
    car = api.model(
        "car",
        {
            "id": fields.String(required=True, description="car id"),
            "user_id": fields.String(required=True, description="user id"),
            "label": fields.String(required=True, description="description of car"),
        },
    )



class TripDto:
    api = Namespace("/trip", description="Trip endpoints")
    trip = api.model(
        "trip",
        {
            "id": fields.Integer(required=True, description="trip id"),
            "start_address_id": fields.Integer(
                required=True, description="start address id"
            ),
            "arrival_address_id": fields.Integer(
                required=True, description="arrival address id"
            ),
            "driver_id": fields.Integer(required=False, description="driver id"),
            "passenger_id": fields.Integer(required=False, description="driver id"),
            "start_time": fields.DateTime(required=True, description="trip start time"),
            "arrival_time": fields.DateTime(
                required=False, description="trip arrival time"
            ),
            # "day": fields.Nested(DayDto.day),
            "comment": fields.String(required=True, description="trip comment"),
            "car_id": fields.Integer(required=False, description="car id"),
            "state": fields.String(required=True, description="trip state"),
            "waypoint_address_id": fields.Integer(
                required=False, description="trip waypoint"
            ),
            "creation_date": fields.DateTime(
                required=True, description="trip creation date"
            ),
            "heading": fields.Float(required=True, description="trip heading"),
            "single_trip": fields.String(
                required=True, description="single or recurrent trip"
            ),
            "validity_start_date": fields.DateTime(
                required=True, description="trip validity start date"
            ),
            "validity_end_date": fields.DateTime(
                required=True, description="trip validity end date"
            ),
            "recurrence_rule": fields.String(
                required=True, description="recurrence rule"
            ),
            # "polyline": fields.String(required=True, description="trip polyline"),
            "start_address": fields.Nested(
                AddressDto.address, required=True, description="start address object"
            ),
            "arrival_address": fields.Nested(
                AddressDto.address, required=True, description="arrival address object"
            ),
            "driver": fields.Nested(
                UserDto.user_private, required=False, description="driver object"
            ),
            "passenger": fields.Nested(
                UserDto.user_private, required=False, description="passenger object"
            ),
            "car": fields.Nested(
                CarDto.car, required=False, description="car object"
            ),
            "free_ratio": fields.Integer(required=False, description="free ratio"),
            "event_occurrence_id": fields.Integer(required=False, description="occurrence id"),
            "nb_seats": fields.Integer(required=False, description="nb of seats"),
            "nb_stops": fields.Integer(required=False, description="nb of acceptable stops"),
            "nb_passengers": fields.Integer(required=False, description="nb of passengers"),
        },
    )


    reduced_trip = api.model(
        "reduced_trip",
        {
            "id": fields.Integer(required=True, description="trip id"),
            "start_address": fields.Nested(AddressDto.address,
                required=True,
                description="trip start address",
            ),
            "arrival_address": fields.Nested(AddressDto.address,
                required=True,
                description="trip arrival address",
            ),
            "recurrence_rule": fields.String(
                required=True, description="recurrence rule"
            ),
            "single_trip": fields.String(
                required=True, description="single or recurrent trip"
            ),
            "validity_start_date": fields.DateTime(
                required=True, description="trip validity start date"
            ),
            "validity_end_date": fields.DateTime(
                required=True, description="trip validity end date"
            ),
            "creation_date": fields.DateTime(
                required=True, description="trip creation date"
            ),
            "start_time": fields.DateTime(required=True, description="trip start time"),
            "user_id": fields.Integer(required=True, description="trip driver or passenger id"),
        },
    )


    reduced_trips_and_wtrips = api.model(
        "reduced_trips_and_wtrips",
        {
            "reduced_trips": fields.List(
                fields.Nested(reduced_trip),
                required=True,
                description="lighter trip list",
            ),
            "reduced_waiting_trips": fields.List(
                fields.Nested(reduced_trip),
                required=True,
                description="lighter waiting_trip list",
            ),
        },
    )

    atcf_trip = api.model(
        "atcf_trip",
        {
            "start_address": fields.Nested(AddressDto.address,
                required=True,
                description="trip start address",
            ),
            "arrival_address": fields.Nested(AddressDto.address,
                required=True,
                description="trip arrival address",
            ),
        },
    )




class Shared_tripDto:
    api = Namespace("/shared_trip", description="Shared_trip endpoints")
    # liste d'occurrences d'un shared_trip
    shared_trip_when = api.model(
        "shared_trip_when",
        {
            "occurrence_list": fields.List(
                fields.DateTime, required=True, description="occurrence_list"
            )
        },
    )
    # coordonnées d'un point d'un itinéraire
    path_point = api.model(
        "shared_trip_coord",
        {
            "long": fields.String(
                required=True, description="shared_trip path point longitude"
            ),
            "lat": fields.String(
                required=True, description="shared_trip path point latitude"
            ),
            "address": fields.Nested(
                AddressDto.cvlatlng_structure,
                required=True,
                description="human readable address of path point",
            ),
        },
    )
    # coordonnées d'un point de routage
    directions_point = api.model(
        "shared_trip_coord",
        {
            "long": fields.String(
                required=True, description="shared_trip path point longitude"
            ),
            "lat": fields.String(
                required=True, description="shared_trip path point latitude"
            ),
        },
    )
    occupant_details = api.model(
        "occupant_details",
        {
            "start_time": fields.DateTime(
                required=True, description="occupant start_time"
            ),
            "start_path_index": fields.Integer(
                required=True, description="occupant start_path_index"
            ),
            "arrival_time": fields.DateTime(
                required=True, description="occupant arrival_time"
            ),
            "arrival_path_index": fields.Integer(
                required=True, description="occupant arrival_path_index"
            ),
        },
    )
    shared_trip = api.model(
        "shared_trip",
        {
            "id": fields.Integer(required=True, description="shared_trip id"),
            "trip_id": fields.Integer(
                required=True, description="shared_trip driver trip_id"
            ),
            "trip_driver_id": fields.Integer(
                required=True, description="shared_trip driver name"
            ),
            "event_occurrence_id": fields.Integer(
                required=True, description="trip event_occurrence_id"
            ),
            "nb_seats": fields.Integer(
                required=True, description="trip nb_seats"
            ),
            "car_label": fields.String(
                required=True, description="car used for shared_trip"
            ),
            "trip_driver": fields.Nested(
                UserDto.user_private_with_phone, required=True, description="shared_trip driver"
            ),
            "driver_score": fields.Integer(
                required=True, description="trip driver score"
            ),
            "passengers_score": fields.Integer(
                required=True, description="trip driver score"
            ),
            "shared_trip_comment": fields.String(
                required=True, description="shared_trip comment"
            ),
            "shared_trip_status": fields.String(
                required=True, description="shared_trip status"
            ),
            "driver_status": fields.String(
                required=True, description="shared_trip driver status"
            ),
            "path": fields.List(
                fields.Nested(path_point),
                required=True,
                description="shared_trip path (list of {long, lat, address})",
            ),
            "directions": fields.List(
                fields.Nested(directions_point),
                required=True,
                description="shared_trip directions (list of {long, lat})",
            ),
            # "shared_distance_list": fields.List(
            #     fields.Float,
            #     required=True,
            #     description="list of shared distances btw passengers and driver",
            # ),
            "occ_details_list": fields.List(
                fields.Nested(occupant_details),
                required=True,
                description="occupants details (list of occupant_details)",
            ),
            "occ_when_list": fields.List(
                fields.Nested(shared_trip_when),
                required=True,
                description="occupants whens (list of occupant occurrence list)",
            ),
            "passenger_id_list": fields.List(
                fields.Integer,
                required=True,
                description="shared_trip passenger ids (list of integers)",
            ),
            "passenger_nb_pass_list": fields.List(
                fields.Integer,
                required=True,
                description="list of nb_passengers (list of integers)",
            ),
            "passenger_list": fields.List(
                fields.Nested(UserDto.user_private_with_phone),
                required=True,
                description="shared_trip passengers (list of User)",
            ),
            "passenger_status_list": fields.List(
                fields.String,
                required=True,
                description="shared_trip passenger statuses (list of strings)",
            ),
            "passenger_comment_list": fields.List(
                fields.String,
                required=True,
                description="shared_trip passenger comments (list of strings)",
            ),
            "waiting_trip_id_list": fields.List(
                fields.Integer,
                required=True,
                description="shared_trip linked waiting_trip id list (list of integer)",
            ),
            "yacka_points_list": fields.List(
                fields.Float,
                required=True,
                description="List of yacka points btw passengers and driver",
            ),
            "fr_info_list": fields.List(
                fields.Integer,
                required=True,
                description="List of free_ratio info",
            ),
        },
    )

    # Dictionnaire comprenant les informations relatives à la mise à jour
    # d'un shared_trip et du (des) wtrip_list associés. Voir la description
    # dans le shared_trip_controller.
    sht_update_info = api.model(
        "sht_update_info",
        {
            "action": fields.String(
                required=True, description="action made by the user"
            ),
            "occ_when_list": fields.List(
                fields.Nested(shared_trip_when),
                required=False,
                description="changed passengers whens list (list of passengers occurrence list)",
            ),
        },
    )

    # Dictionnaire comprenant le nombre d'occurrences de shared_trip risquant d'être
    # affectées par une modification de trip / waiting_trip
    sht_check_info = api.model(
        "sht_check_info",
        {
            "sht_status_info": fields.String(
                required=True, description="driver or passenger status of a shared_trip"
            ),
            "nb_occurrences": fields.Integer(
                required=True, description="nb of shared_trip occurrences with the corresponding status"
            ),
            "wtl_id_list": fields.String(
                required=True, description="string of the list of wtl_ids impacted, for each status"
            )

        }
    )

    # Dictionnaire comprenant la liste des shared_trips modifiés ou supprimés par la
    # modification d'un trip / waiting_trip.
    sht_trip_update_info = api.model(
        "sht_trip_update_info",
        {
            "updated_list": fields.List(
                fields.Integer,
                required=True, description="list of updated shared_trips ids"
            ),
            "deleted_list": fields.List(
                fields.Integer,
                required=True, description="list of deleted shared_trips ids"
            ),
            "new_rule_exceeds": fields.Boolean(
                required=True, description="whether new rule exceeds the old one"
            )
        }
    )

    agenda_indexes = api.model(
        "agenda_indexes",
        {
            "index": fields.Integer(
                required=True, description="index of associated shared_trip in agenda"
            ),
            "date": fields.DateTime(
                required=True, description="occurence of shared_trip linked to index"
            ),
        },
    )

    agenda_home = api.model(
        "agenda_home",
        {
            "agenda_indexes": fields.List(
                fields.Nested(agenda_indexes),
                required=True,
                description="list of trips sorted by date with indexes",
            ),
            "shared_trips": fields.List(
                fields.Nested(shared_trip),
                required=True,
                description="List of every shared_trips linked to user",
            ),
        },
    )

    polyline_details = api.model(
        "polyline_details",
        {
            "shared_trip_status": fields.String(
                required=True, description="shared_trip status"
            ),
            "directions": fields.List(
                fields.Nested(directions_point),
                required=True,
                description="shared_trip directions (list of {long, lat})",
            ),
            "occ_details_list": fields.List(
                fields.Nested(occupant_details),
                required=True,
                description="occupants details (list of occupant_details)",
            ),
            "path": fields.List(
                fields.Nested(path_point),
                required=True,
                description="shared_trip path (list of {long, lat, address})",
            ),
        },
    )

    shtrip_for_company = api.model(
        "shtrip_for_company",
        {
            "directions": fields.List(
                fields.Nested(directions_point),
                required=True,
                description="shared_trip directions (list of {long, lat})",
            ),
            "path": fields.List(
                fields.Nested(path_point),
                required=True,
                description="shared_trip path (list of {long, lat, address})",
            ),
            "driver_start": fields.Nested(path_point,
                required=True,
                description="driver start path point",
            ),
            "driver_arrival": fields.Nested(path_point,
                required=True,
                description="driver arrival path point",
            ),
            "passenger_start": fields.Nested(path_point,
                required=True,
                description="passenger start path point",
            ),
            "passenger_arrival": fields.Nested(path_point,
                required=True,
                description="passenger arrival path point",
            ),
            "shared_distance": fields.Float(
                required=True,
                description="shared distance btw passenger and driver",
            ),
        },
    )
    shtrip_list_for_stats = api.model(
        "shtrip_list_for_stats",
        {
            "sht_status_info": fields.String(
                required=True, description="status of a shared_trip"
            ),
            "nb_sht": fields.Integer(
                required=True,
                description="nb of shared_trip with this status",
            ),
            "sht_list": fields.List(
                fields.Nested(shtrip_for_company),
                required=True,
                description="list of shtrips",
            ),
        },
    )


class MessageDto:
    api = Namespace("/message", description="Message endpoints")
    message = api.model(
        "message",
        {
            "id": fields.String(required=True, description="message id"),
            "user1": fields.String(required=True, description="sender id"),
            "user2": fields.String(required=True, description="receiver id"),
            "user1db": fields.Nested(UserDto.user_private),
            "user2db": fields.Nested(UserDto.user_private),
            "message": fields.String(required=True, description="message sent"),
            "alert_level": fields.Integer(required=False, description="message alert level"),
            "send_date": fields.String(required=True, description="message sent date"),
            "read_date": fields.String(required=True, description="message read date"),
            "current_user_id": fields.String(
                required=True,
                description="id of the current user, allows to determine who is the sender",
            ),
        },
    )

    conversation = api.model(
        "conversation",
        {
            "user": fields.Nested(UserDto.user_private, description="current user"),
            "other_user": fields.Nested(
                UserDto.user_private,
                description="user with the one the current_user is speaking with",
            ),
            "conversation": fields.List(fields.Nested(message)),
        },
    )

    conversations = api.model(
        "conversations", {"conversations": fields.List(fields.Nested(message))}
    )


# Commented by Olivier as history table was redefined - to be rewritten if
# such an endpoint is still needed

# class HistoryDto:
#   api = Namespace('/history',description="History endpoints")
#   history = api.model('history',{
#     'id':fields.String(required=True, description='history id'),
#     'user':fields.Nested(UserDto.user),
#     'trip':fields.Nested(TripDto.trip),
#     'date':fields.String(required=True, description='history date')
#   })


class ReportDto:
    api = Namespace("/report", description="Report endpoints")
    report = api.model(
        "report",
        {
            "id": fields.String(required=True, description="report id"),
            "problem": fields.Nested(ProblemDto.problem),
            "user": fields.Nested(UserDto.user),
            "target": fields.Nested(UserDto.user),
            "comment": fields.String(required=True, description="report comment"),
        },
    )


class ExceptionDto:
    api = Namespace("/exception", description="Exception endpoints")
    exception = api.model(
        "exception",
        {
            "id": fields.String(required=True, description="exception id"),
            "start_date": fields.String(
                required=True, description="exception start date"
            ),
            "end_date": fields.String(required=True, description="exception end date"),
        },
    )


class GiftDto:
    api = Namespace("/gift", description="Gift endpoints")
    gift = api.model(
        "gift",
        {
            "id": fields.String(required=True, description="gift id"),
            "organization": fields.Nested(OrganizationDto.organization),
            "label": fields.String(required=True, description="gift label"),
            "point_value": fields.String(required=True, description="gift point value"),
            "real_value": fields.String(required=True, description="gift real value"),
        },
    )


class ReviewDto:
    api = Namespace("/review", description="Review endpoints")
    review = api.model(
        "review",
        {
            "id": fields.String(required=True, description="review id"),
            "comment": fields.String(required=True, description="review comment"),
            "organization": fields.Nested(OrganizationDto.organization),
            "date": fields.String(required=True, description="review date"),
        },
    )



class GeneralDto:
    api = Namespace("/", description="General endpoints")


class TestDto:
    api = Namespace("/test", description="Test endpoints")

    tested_path = api.model(
        "tested_path",
        {
            "driver_heading": fields.Float(required=True, description="driver trip heading"),
            "passenger_heading": fields.Float(required=True, description="passenger trip heading"),
            "driver_gap": fields.Float(required=True, description="driver time gap"),
            "driver_gap_ratio": fields.Float(required=True, description="driver time gap ratio"),
            "directions": fields.List(
                fields.Nested(Shared_tripDto.directions_point),
                required=True,
                description="resulting directions (list of {long, lat})",
            )
        },
    )


class AdminDto:
    api = Namespace("/admin", description="Admin endpoints")
    stats_admin = api.model(
        "stats",
        {
            "nb_companies": fields.String(),
            "nb_employees": fields.String(),
            "nb_trips": fields.String(),
            "revenue_month": fields.String(),
            "revenue_per_employees": fields.String(),
        },
    )
    home_admin = api.model("home_admin", {"stats": fields.Nested(stats_admin)})
    companies_admin = api.model(
        "companies_admin", {"users": fields.List(fields.Nested(UserDto.user))}
    )
    settings_admin = api.model("settings_admin", {"admin": fields.Nested(UserDto.user)})
    reports_admin = api.model(
        "reports_admin", {"reports": fields.List(fields.Nested(ReportDto.report))}
    )


class UsersDto:
    api = Namespace("/users", description="Users endpoints")
    home_users = api.model(
        "home_users",
        {
            "user": fields.Nested(UserDto.user),
            "problems": fields.List(fields.String),
            "welcome_msg": fields.String(),
            "has_unread_message": fields.Boolean(
                required=True, description="doas the user has unread message ?"
            ),
        },
    )
    user_trips = api.model(
        "user_trips",
        {
            "user": fields.Nested(UserDto.user),
            "trips": fields.List(fields.Nested(TripDto.trip)),
            "waiting_trips": fields.List(fields.Nested(TripDto.trip)),
        },
    )
    user_trip_counts = api.model(
        "user_trip_counts",
        {
            "trip_count": fields.Integer(),
            "waiting_trip_count": fields.Integer()
        },
    )
    profile_users = api.model(
        "profile_users",
        {
            "user": fields.Nested(UserDto.user),
        },
    )
    settings_users = api.model(
        "settings_users",
        {
            "user": fields.Nested(UserDto.user),
            "cars": fields.List(fields.Nested(CarDto.car)),
            "addresses": fields.List(fields.Nested(AddressDto.address)),
        },
    )
    search_users = api.model(
        "search_users", {"trips": fields.List(fields.Nested(TripDto.trip))}
    )
    # history_users = api.model('history_users',{
    #   "history":fields.List(fields.Nested(HistoryDto.history)),
    #   "problems":fields.List(fields.Nested(ProblemDto.problem))
    # })


class WelcomeMessageDto:
    api = Namespace("/welcome-msg", description="Welcome Message endpoints")
    wmsg = api.model(
        "wmsg",
        {
            "id": fields.String(required=True, description="welcome message id"),
            "message": fields.String(
                required=True, description="message of welcome message"
            ),
        },
    )
    all_wmsg_m = api.model(
        "all_welcome_msg", {"welcome_msgs": fields.List(fields.Nested(wmsg))}
    )


class EventDto:
    api = Namespace("/event", description="Event endpoints")
    event_occurrence = api.model(
        "event_occurrence",
        {
            "id": fields.Integer(required=True, description="user id"),
            "name": fields.String(required=True, description="event occurrence name"),
            "open_occurrence" : fields.Boolean(required=True, description="whether the event occurrence is open or not"),
            "community_id": fields.String(required=True, description="community id"),
            "start_time": fields.DateTime(required=True, description="event occurrence start time"),
            "comment": fields.String(required=True, description="occurrence comment"),
        },
    )
    event_occurrence_public = api.model(
        "event_occurrence",
        {
            "id": fields.Integer(required=True, description="user id"),
            "name": fields.String(required=True, description="event occurrence name"),
            "open_occurrence" : fields.Boolean(required=True, description="whether the event occurrence is open or not"),
            "start_time": fields.DateTime(required=True, description="event occurrence start time"),
            "comment": fields.String(required=True, description="occurrence comment"),
        },
    )
    event = api.model(
        "event",
        {
            "id": fields.Integer(required=True, description="event id"),
            "event_org_name": fields.String(required=True, description="event organizer name"),
            "single_date" : fields.Boolean(required=True, description="whether the event is single or multiple date"),
            "beginning_date": fields.DateTime(required=False, description="event start time"),
            "end_date": fields.DateTime(required=False, description="event end time"),
            "name": fields.String(required=True, description="event name"),
            "email": fields.String(required=True, description="event email"),
            "event_url": fields.String(required=True, description="event url"),
            "phone": fields.String(required=True, description="event phone"),
            "sht_url_ext": fields.String(required=True, description="event sht url ext"),
            "sht_preferred_url_ext": fields.String(required=True, description="event sht preferred url ext"),
            "full_sht_url": fields.String(required=True, description="event full sht url"),
            "address": fields.Nested(
                AddressDto.address, required=True, description="address object"
            ),
            "comment": fields.String(required=True, description="event comment"),
            "logo": fields.String(required=True, description="event base64 encoded banner"),
            "occurrences": fields.List(fields.Nested(event_occurrence)),
        },
    )
    event_public = api.model(
        "event",
        {
            # "id": fields.Integer(required=True, description="user id"),
            # "organization": fields.Nested(OrganizationDto.organization),
            "event_org_name": fields.String(required=True, description="event organizer name"),
            "single_date" : fields.Boolean(required=True, description="whether the event is single or multiple date"),
            "beginning_date": fields.DateTime(required=False, description="event start time"),
            "end_date": fields.DateTime(required=False, description="event end time"),
            "name": fields.String(required=True, description="event name"),
            "email": fields.String(required=True, description="event email"),
            "event_url": fields.String(required=True, description="event url"),
            "phone": fields.String(required=True, description="event phone"),
            "full_sht_url": fields.String(required=True, description="event full sht url"),
            "address": fields.Nested(
                AddressDto.address, required=True, description="address object"
            ),
            "comment": fields.String(required=True, description="event comment"),
            "logo": fields.String(required=True, description="event base64 encoded banner"),
            "occurrences": fields.List(fields.Nested(event_occurrence_public)),
        },
    )

    event_update_info = api.model(
        "event_update_info",
        {
            "updated_event": fields.Nested(event),
        }
    )

    event_occ_update_info = api.model(
        "event_occ_update_info",
        {
            "updated_event": fields.Nested(event),
            "updated_event_occ": fields.Nested(event_occurrence),
        }
    )
    event_occurrence_stats = api.model(
        "event_occurrence_stats",
        {
            "name": fields.String(required=True, description="event name"),
            "start_time": fields.DateTime(required=True, description="event occurrence start time"),
            "trip_cumulative_distance": fields.Integer(),
            "waiting_trip_cumulative_distance": fields.Integer(),
            "trip_mean_distance": fields.Float(),
            "waiting_trip_mean_distance": fields.Float(),
            "trip_nb_occurrence_mean": fields.Integer(),
            "atcf_trip_list": fields.List(fields.Nested(TripDto.atcf_trip)),
            "atcf_waiting_trip_list": fields.List(fields.Nested(TripDto.atcf_trip)),
            "shtrip_list": fields.Nested(Shared_tripDto.shtrip_list_for_stats),
            "nb_pend_shtrip": fields.Integer(),
            "nb_halfacc_shtrip": fields.Integer(),
            "nb_valid_shtrip": fields.Integer(),
            "valid_shtrip_mean_distance": fields.Float(),
        },
    )


class CompanyDto:
    api = Namespace("/companies", description="Companies endpoints")
    best_user_company = api.model(
        "best_user_company",
        {
            "score": fields.String(),
            "id": fields.String(),
            "name": fields.String(),
            "surname": fields.String(),
        },
    )
    # shtrip_list_for_stats = api.model(
    #     "shtrip_list_for_stats",
    #     {
    #         "sht_status_info": fields.String(
    #             required=True, description="status of a shared_trip"
    #         ),
    #         "nb_sht": fields.Integer(
    #             required=True,
    #             description="nb of shared_trip with this status",
    #         ),
    #         "sht_list": fields.List(
    #             fields.Nested(Shared_tripDto.shtrip_for_company),
    #             required=True,
    #             description="list of shtrips",
    #         ),
    #     },
    # )
    stats_company = api.model(
        "stats_company",
        {
            "nb_subscribers": fields.Integer(),
            "trip_cumulative_distance": fields.Integer(),
            "waiting_trip_cumulative_distance": fields.Integer(),
            "trip_mean_distance": fields.Float(),
            "waiting_trip_mean_distance": fields.Float(),
            "trip_nb_occurrence_mean": fields.Integer(),
            "waiting_trip_nb_occurrence_mean": fields.Float(),
            "subscriber_list": fields.List(fields.String()),
            "atcf_trip_list": fields.List(fields.Nested(TripDto.atcf_trip)),
            "atcf_waiting_trip_list": fields.List(fields.Nested(TripDto.atcf_trip)),
            "community_list": fields.List(fields.String()),
            "shtrip_list": fields.Nested(Shared_tripDto.shtrip_list_for_stats),
            "nb_pend_shtrip": fields.Integer(),
            "nb_halfacc_shtrip": fields.Integer(),
            "nb_valid_shtrip": fields.Integer(),
            "valid_shtrip_mean_distance": fields.Float(),
            "halfacc_shtrip_nb_occurrence_mean": fields.Integer(),
            "valid_shtrip_nb_occurrence_mean": fields.Integer(),
        },
    )
    home_company = api.model(
        "home_company",
        {
            "user": fields.Nested(UserDto.user_for_company),
            "stats": fields.Nested(stats_company),
            "welcome_msg": fields.String(),
            "has_unread_message": fields.Boolean(
                required=True, description="doas the user has unread message ?"
            ),
        },
    )
    users_company = api.model(
        "users_company",
        {
            "user": fields.Nested(UserDto.user),
            "users": fields.List(fields.Nested(UserDto.user)),
        },
    )
    settings_company = api.model(
        "settings_company",
        {
            "user": fields.Nested(UserDto.user),
            "addresses": fields.List(fields.Nested(AddressDto.address))
        }
    )
    events_company = api.model(
        "events_company",
        {
            "events": fields.Nested(EventDto.event),
            "remaining_events": fields.Nested(EventDto.event),
            "past_events": fields.Nested(EventDto.event),
        },
    )

class ProofOfTravelDto:
    api = Namespace("/proof", description="Proof of travel endpoints")
    proof = api.model(
        "proof",
        {
            "id": fields.String(required=True, description="proof id"),
            "proof_class": fields.String(required=True, description="proof class"),
            "driver_id": fields.String(required=True, description="driver id"),
            "passenger_id": fields.String(required=True, description="passenger id"),
            "passenger_seats": fields.String(required=True, description="number of seats"),
            "passenger_contribution": fields.String(required=True, description="passenger contribution"),
            "driver_revenue": fields.String(required=True, description="driver revenue"),
            "incentive_id": fields.String(required=True, description="incentive id"),
            "wtrip_list_id": fields.String(required=True, description="wtrip list id"),
        },
    )

    get_proof = api.model("get_proof", {"proof": fields.Nested(proof)})
    user_private = api.model(
        "proof2",
        {
            "id": fields.String(required=True, description="proof id"),
            "proof_class": fields.String(required=True, description="proof class"),
            "driver_id": fields.String(required=True, description="driver id"),
            "passenger_id": fields.String(required=True, description="passenger id"),
            "passenger_seats": fields.String(required=True, description="number of seats"),
        },
    )

