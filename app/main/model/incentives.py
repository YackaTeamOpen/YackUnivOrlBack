from .. import  db


class Incentives(db.Model):
    """Model for storing the trip details once 2+ people consider to share it"""

    __tablename__ = "incentives"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incentive_driver_id = db.Column(db.Integer, db.ForeignKey("incentive.id"), nullable=True)
    incentive_passenger_id = db.Column(db.Integer, db.ForeignKey("incentive.id"), nullable=True)


    incentive_driver = db.relationship("Incentive", foreign_keys=[incentive_driver_id])
    incentive_passenger = db.relationship("Incentive", foreign_keys=[incentive_passenger_id])