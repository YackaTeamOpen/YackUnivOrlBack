from .. import db

class Mail(db.Model):
    """ Mail Model for storing mail related details """
    __tablename__ = "mail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(20), nullable=False)
    file = db.Column(db.String(50), nullable=False)
