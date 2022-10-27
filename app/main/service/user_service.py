import datetime
import json
from flask_login import current_user
from sqlalchemy import or_
import logging
import re

from main import db
from main.config import environments, config_name
from main.model.user import User
from main.model.message import Message
from main.model.address import Address
from main.model.car import Car

from main.service.mails.Mail import Mail

# from main.service.photo.photo_uploader import store_photo, get_photo

from main.service.organization_service import (
    getOrganizationById
)
from main.service.photo.image_utils import lighten_image

log = logging.getLogger(__name__)


def getAllUserType1():
    users = User.query.filter_by(type=1).all()
    for i, user in enumerate(users):
        users[i] = getUserById(user.id)
    return users


def getAllUserType2():
    users = User.query.filter_by(type=2).all()
    for i, user in enumerate(users):
        users[i] = getUserById(user.id)
    return users


def getUserByEmail(email):
    user = User.query.filter_by(email=email).first()
    return (getUserById(user.id) if user else None)


def getUserById(user_id, withLastname=True, withOrganization=False):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if not withLastname:
            user.name = ""

        if withOrganization and user.organization_id:
            user.organization = getOrganizationById(user.organization_id)
        
        return user
    return None


def getUserWithNoLastname(user_id):
    # Returns user record but without lastname (for confidentiality purpose)
    return getUserById(user_id, withLastname=False)


def hasUnreadMessage(user_id):
    unread_messages = (
        Message.query.filter(Message.user2 == user_id)
        .filter(Message.read_date == None)
        .all()
    )
    return len(unread_messages) > 0


def update_user(user_id, data, from_API = False):
    if user_id == current_user.id:
        # To avoid inappropriate modification of critical info, remove
        # the possible critical keys from the data dict, except if the
        # function is called from within the API
        if not from_API :
            data.pop("type", None)
            data.pop("password_hash", None)
            data.pop("email", None)
            data.pop("organization_id", None)
            data.pop("points", None)
            data.pop("last_login", None)
            data.pop("cgu", None)
            data.pop("creation_date", None)
            data.pop("email_ok", None)
            data.pop("check", None)
            data.pop("category", None)

        # If photo is to be loaded and its size is too big, reduce it
        regexp = re.compile('^data:image/.+;base64,')
        if (("photo" in data) and (regexp.search(data['photo'][:40]))) :
            avatar_size = environments[config_name]["avatar_size"]
            data['photo'] = lighten_image(data['photo'], avatar_size)
        else :
            data['photo'] = ''
        if current_user.type in [2, 4]:
            if "birthdate" in data and data["birthdate"] != None:
                data["birthdate"] = datetime.datetime.fromtimestamp(
                    int(data["birthdate"]) / 1000
                )
            if "email" in data:
                del data["email"]

            # Vérification de la bonne valeur pour le genre
            if 'gender' in data and data['gender'] != 'X' :
                data['gender'] = ('F' if (data["gender"] == 'F') else 'M')
            User.query.filter_by(id=user_id).update(data)
            save_changes(User.query.filter_by(id=user_id).first())
            return {"status": "success", "message": "User updated"}, 200
        elif current_user.type == 1:
            User.query.filter_by(id=user_id).update(data)
            commit()
            # save_changes(User.query.filter_by(id=user_id).first())
            # data_organization = {
            #     "name": data["name"],
            #     "siret": data["siret"],
            #     "address": data["address"],
            # }
            # Organization.query.filter_by(id=current_user.organization_id).update(
            #     data_organization
            # )
            # save_changes(
            #     Organization.query.filter_by(
            #         id=current_user.organization_id).first()
            # )
            return {"status": "success", "message": "User updated"}, 200
        return {"status": "fail", "message": "Unauthorized"}, 401
    return {"status": "fail", "message": "Unauthorized"}, 401


def update_password(user_id, password):
    if user_id == current_user.id:
        user = User.query.filter_by(id=int(user_id)).first()
        user.password(password)
        save_changes(user)
        mail_datas = {"url": environments[config_name]["web_manager_url"]}
        try :
            mail = Mail("password_changed")
        except Exception as e:
            log.exception(e, exc_info=True)
            return None
        mail.send_mail(
            mail_datas,
            current_user.email,
            "Yacka: Votre mot de passe a été modifié avec succès.",
        )


def get_data_of_user(user_id):
    user = getUserById(user_id)
    messages = Message.query.filter(
        or_(Message.user1 == user_id, Message.user2 == user_id)
    ).all()
    # trips = Trip.query.filter(Trip.driver_id == user_id).all()
    # waiting_trips = Waiting_trip.query.filter(
    #     Waiting_trip.passenger_id == user_id
    # ).all()
    addresses = Address.query.filter(Address.user_id == user_id).all()
    cars = Car.query.filter(Car.user_id == user_id).all()
    # history = History.query.filter(
    #     or_(History.driver_id == user_id, History.passenger_id == user_id)
    # ).all()

    data = {
        "user": str(user),
        "messages": messages,
        # "trips": [str(trip) for trip in trips],
        # "waiting_trips": [str(trip) for trip in waiting_trips],
        "addresses": [str(address) for address in addresses],
        "cars": [str(car) for car in cars],
        # "history": [str(action) for action in history],
    }

    return json.dumps(data, indent=4, sort_keys=True, default=str)


def setup_password(user_id, password):
    user = User.query.filter_by(id=int(user_id)).first()
    user.password(password)
    save_changes(user)


def update_last_login(user_id):
    if user_id == current_user.id:
        User.query.filter_by(id=int(user_id)).update(
            {"last_login": datetime.datetime.now()}
        )
        save_changes(User.query.filter_by(id=int(user_id)).first())
    return {"status": "fail", "message": "Unauthorized"}, 401


def validate_email(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    user.email_ok = True
    save_changes(user)
    return user.email_ok


def delete_check(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    user.check = None
    save_changes(user)


def new_problem(user_id, comment):
    mail = Mail("new_problem_suggestion")
    user = getUserById(user_id)
    mail.send_mail(
        {
            "nom": user.surname + " " + user.name + " (" + str(user_id) + ")",
            "messagecontent": comment,
        },
        "contact@yacka.fr",
        "Nouveau problème/suggestion",
    )
    return {"status": "success", "message": "Message sent"}


def commit() :
    db.session.commit()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
