from flask_login import current_user
import random
from main import db
from main.model.welcome_msg import WelcomeMessage


def create_new_welcome_msg(data):
    if current_user.type == 1:
        welcome_msg = WelcomeMessage(
            message=data["message"],
            state=data["state"] if data.get("state", None) != None else 1
        )
        save_changes(welcome_msg)
        return {"status": "success", "message": "welcome_msg inserted"}, 201
    return {"status": "fail", "message": "Unauthorized"}, 401


def get_all_welcome_msg(data):
    if current_user.type == 1:
        request_deactivated = False if data.get("state", None) == None or data["state"] == 0 else True
        if request_deactivated:
            wmsgs = WelcomeMessage.query.all()
        else:
            wmsgs = WelcomeMessage.query.filter_by(state=1).all()
        return wmsgs
    return {"status": "fail", "message": "Unauthorized"}, 401


def delete_welcome_msg(welcome_msg_id):
    if current_user.type == 1:
        WelcomeMessage.query.filter_by(id=welcome_msg_id).delete()
        db.session.commit()
        return {"status": "success", "message": "Address deleted"}, 200
    return {"status": "fail", "message": "Unauthorized"}, 401


def getWelcomeMessage(user):
    wmsgs = WelcomeMessage.query.filter_by(state=1).all()
    wmsg = "Merci d'utiliser Yacka"
    if len(wmsgs) > 1:
        wmsg = random.choice(wmsgs).message
    elif len(wmsgs) == 1:
        wmsg = wmsgs[0].message
    return wmsg


def save_changes(data):
    db.session.add(data)
    db.session.commit()

# Remplacer welcome_msg ==> "nom_de_la_table"
# Remplacer WelcomeMessage ==> "Nom_de_la_table"
