from .. import db

from main.model.organization import Organization

class Bill(db.Model):
    """ Bill Model for storing bill related details """
    __tablename__ = "bill"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False)
    nb_max_employees = db.Column(db.Integer, nullable=False)
