from .. import db

class Problem(db.Model):
    """ Problem Model for storing problem related details """
    __tablename__ = "problem"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(191), nullable=False)
