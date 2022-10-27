import datetime
import string
import json
from .. import db, flask_bcrypt
from sqlalchemy.dialects.mysql import LONGTEXT

from main.model.organization import Organization
from main.model.speaking_pref import Speaking_pref
from main.model.smoking_pref import Smoking_pref
from main.model.music_pref import Music_pref


class User(db.Model):
    """User Model for storing user related details"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(1), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(191), nullable=False, unique=True)
    phone = db.Column(db.String(191), nullable=True)
    aboutme = db.Column(db.String(191), nullable=True)
    photo = db.Column(LONGTEXT, nullable=True)
    public_phone = db.Column(db.Boolean, default=False)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=True
    )
    speaking_pref_id = db.Column(
        db.Integer, db.ForeignKey("speaking_pref.id"), nullable=True
    )
    smoking_pref_id = db.Column(
        db.Integer, db.ForeignKey("smoking_pref.id"), nullable=True
    )
    music_pref_id = db.Column(db.Integer, db.ForeignKey("music_pref.id"), nullable=True)
    points = db.Column(db.Integer, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    unsubscribe = db.Column(db.Integer, nullable=True)
    birthdate = db.Column(db.DateTime, nullable=True)
    cgu = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime)
    email_ok = db.Column(db.Boolean, nullable=False, default=False)
    check = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True)

    organization = db.relationship("Organization", foreign_keys=[organization_id])
    speaking_pref = db.relationship("Speaking_pref", foreign_keys=[speaking_pref_id], lazy="joined")
    smoking_pref = db.relationship("Smoking_pref", foreign_keys=[smoking_pref_id], lazy="joined")
    music_pref = db.relationship("Music_pref", foreign_keys=[music_pref_id], lazy="joined")
    current_points = 0.0

    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}>".format(
            self.id,
            self.type,
            self.password_hash,
            self.gender,
            self.name,
            self.surname,
            self.email,
            self.phone,
            self.aboutme,
            self.photo,
            self.public_phone,
            self.points,
            self.last_login,
            self.birthdate,
            self.cgu,
            self.creation_date,
            self.email_ok,
            self.check,
            self.category,
            self.current_points,
        )
