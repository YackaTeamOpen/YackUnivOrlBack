from .. import  db
from main.model.incentive import Incentive


class Incentives(db.Model):
    """Model for storing the table of the incentives of a driver and a passenger"""

    __tablename__ = "incentives"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incentive_driver_id = db.Column(db.Integer, db.ForeignKey("incentive.id"), nullable=True)
    incentive_passenger_id = db.Column(db.Integer, db.ForeignKey("incentive.id"), nullable=True)
    wtrip_list_id = db.Column(db.Integer, nullable=False)


    incentive_driver = db.relationship("Incentive", foreign_keys=[incentive_driver_id])
    incentive_passenger = db.relationship("Incentive", foreign_keys=[incentive_passenger_id])

    def __repr__(self):
        return "<Incentives {} {} {} {}>".format(
            self.id,
            self.incentive_driver_id,
            self.incentive_passenger_id,
            self.wtrip_list_id
        )