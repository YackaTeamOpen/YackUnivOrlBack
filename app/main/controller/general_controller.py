import json
from flask import Response, request
from flask_restx import Resource
from flask_login import login_required, logout_user, login_user, current_user
import logging

from .. import login_manager
from ..util.dto import GeneralDto

from main.config import environments, config_name

from main.service.mails.Mail import Mail
from main.service.user_service import (
    getUserById,
    getUserByEmail,
    update_password,
    update_last_login,
    delete_check,
    setup_password,
    validate_email
)
from main.model.user import User
from main.model.users import Users

log = logging.getLogger(__name__)
api = GeneralDto.api


@api.route("login")
class Login(Resource):
    @api.doc('login first')
    def get(self):
        return Response(json.dumps({"status": -1, "message": "you must login first"}))

    @api.doc('login to api')
    @api.response(200, 'Log in successful')
    @api.response(401, 'Invalid username or password.')
    @api.param('email', 'email address')
    @api.param('password', 'password')
    def post(self):
        data = request.form
        user = User.query.filter_by(email=data.get('email')).first()
        if user and user.password_hash and user.check_password(data.get('password')):
            if user.email_ok :
                flask_user = Users(user.id, user.type, user.password_hash, user.name, user.surname, user.gender, user.email, "", user.phone, user.organization_id, user.speaking_pref_id, user.music_pref_id, user.smoking_pref_id, user.points, "", "", user.creation_date, user.last_login, user.unsubscribe)
                # login_user(flask_user,remember=True) # This would be if the sessions were not set permanent during init...
                login_user(flask_user)
                if user.last_login:
                    update_last_login(user.id)
                    last_login = user.last_login.timestamp() * 1000
                else:
                    last_login = None
                return {"type": user.type, "last_login": last_login, "status": "success", "message": "Log in successful"}, 200
            else :
                return {"status": "fail", "message": "email not validated yet"}, 403
        else:
            return {"status": "fail", "message": "invalid username or password"}, 401


@api.route("logout")
class Logout(Resource):
    @login_required
    @api.doc('logout')
    @api.response(200, 'Log out successful')
    def get(self):
        logout_user()
        return {"status": "success", "message": "Log out successful"}, 200


@api.route("forgot")
class Forgot(Resource):
    @api.doc('forgot password')
    @api.response(200, 'Re-initialize password successful')
    @api.param('email', 'Email address')
    def post(self):
        data = request.form
        user = getUserByEmail(data["email"])
        if user :
            check = delete_password(user.id)
            url = environments[config_name]["web_manager_url"] + "/forgot.html?email=" + data["email"] + "&check=" + check
            try :
                gender = (user.gender + ". ") if (user.gender != "X") else ""
                surname = (user.surname + " ") if (user.surname != "none") else ""
                mail = Mail("forgot_password").send_mail(
                    {
                        "gender": gender,
                        "surname": surname,
                        "url": url
                    },
                    user.email,
                    "Ré-initialisation du mot de passe"
                )
                return {"status": "success", "message": "Re-initialize password successful"}, 200
            except Exception as e:
                log.exception(e, exc_info=True)
                return {"status": "fail", "message": "Unable to send mail"}, 500
        else :
            return {"status": "fail", "message": "invalid username or password"}, 401


@api.route("resendemailcheck")
class Resendemailcheck(Resource):
    @api.doc('resend email check')
    @api.response(200, 'email check email resent')
    @api.param('email', 'Email address')
    def post(self):
        data = request.form
        user = getUserByEmail(data["email"])
        if user :
            resend_email_check(user.id)
        else :
            return {"status": "fail", "message": "invalid username or password"}, 401


@api.route("checkpass")
class Checkpass(Resource):
    @api.doc('validate account')
    @api.param('email', 'Email address')
    @api.param('check', 'Unique hash for checking')
    @api.param('initial', 'initial or reset')
    def post(self):
        data = request.form
        user = getUserByEmail(data["email"])
        initial = data["initial"]
        if user and user.check == data["check"]:
            if (initial == "initial" and not user.email_ok) :
                # C'est la validation intiale de l'identifiant
                is_ok = validate_email(user.id)
                if is_ok :
                    return {"status": "success", "message": "Allowed user"}, 200
                else :
                    return {"status": "fail", "message": "Error validating email"}, 500
            elif (initial == "reset") :
                # On est après le reset du password
                return {"status": "success", "message": "Allowed user"}, 200
            else :
                return {"status": "fail", "message": "Unauthorized"}, 401
        else:
            return {"status": "fail", "message": "Unauthorized"}, 401


@api.route("signup")
class Signup(Resource):
    @api.doc(' signup after passwd reset')
    @api.param('email', 'Email address')
    @api.param('check', 'Check')
    @api.param('password', 'Password')
    def post(self):
        data = request.form
        user = getUserByEmail(data["email"])
        if (user and user.check == data["check"]) :
            setup_password(user.id, data["password"])
            delete_check(user.id)
            return {"status": "success", "message": "Password successfully reinitialized"}, 200
        else:
            return {"status": "fail", "message": "Unauthorized"}, 401


@api.route("contact")
class Contact(Resource):
    @api.doc('contact us at the contact address')
    @api.response(200, 'Send message successful')
    @api.response(400, 'Something wrong with parameters')
    @api.param('name', 'Last name')
    @api.param('surname', 'First name')
    @api.param('email', 'Email address')
    @api.param('organization', 'Name of organization')
    @api.param('subject', 'Subject')
    @api.param('content', 'Message')
    def post(self):
        data = request.form
        surname = data.get("surname", None)
        name = data["name"]
        organization = data.get("organization", None)
        email = data["email"]
        subject = data.get("subject", None)
        content = data["content"]
        if name and email and content:
            mail_datas = {
                "surname": (surname if surname else ""),
                "name": name,
                "organization": (organization if organization else ""),
                "subject": (subject if subject else ""),
                "email": email,
                "content": content
            }
            try :
                mail = Mail("contact")
                mail.send_mail(mail_datas, "contact@yacka.fr", subject)
                return {"status": "success", "message": "Send message successful"}, 200
            except Exception as e:
                log.exception(e, exc_info=True)
                return {"status": "fail", "message": "Unable to send mail"}, 500
        else:
            return {"status": "fail", "message": "Something wrong with parameters"}, 400


@api.route("password")
class Password(Resource):
    @login_required
    @api.doc('change password')
    @api.response(200, 'Change password successful')
    @api.response(400, 'Wrong password')
    @api.param('id', 'User id')
    @api.param('password', 'Old password')
    @api.param('new_password', 'New password')
    def post(self):
        data = request.form.to_dict()
        user = getUserById(current_user.id)
        if user.check_password(data["password"]):
            if (update_password(user.id, data["new_password"]) == None) :
                return {"status": "success", "message": "Change password successful but no mail sent"}, 200
            else :
                return {"status": "success", "message": "Change password successful"}, 200
        else:
            return {"status": "fail", "message": "Wrong password"}, 400


@api.route("/health")
class Health(Resource):
    @api.doc('health check')
    def get(self):
        return Response(json.dumps({"status": "ok"}))


@login_manager.user_loader
def load_user(user_id):
    user = getUserById(user_id)
    if user:
        return Users(user.id, user.type, user.password_hash, user.name, user.surname, user.gender, user.email, "", user.phone, user.organization_id, user.speaking_pref_id, user.music_pref_id, user.smoking_pref_id, user.points, "", "", user.creation_date, user.last_login, user.unsubscribe)
    return None
