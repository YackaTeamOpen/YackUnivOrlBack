from .. import  db


class Incentive(db.Model):
    """Model for storing the trip details once 2+ people consider to share it"""

    __tablename__ = "incentive"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    amont = db.Column(db.Float, nullable=False)


    user = db.relationship("User", foreign_keys=[user_id])