from .. import db

from main.model.shared_trip import Shared_trip
from main.model.waiting_trip import Waiting_trip

class Wtrip_list(db.Model):
    """ Model for storing shared_trip passengers-specific details """
    __tablename__ = "wtrip_list"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shared_trip_id = db.Column(db.Integer, db.ForeignKey('shared_trip.id'))
    waiting_trip_id = db.Column(db.Integer, db.ForeignKey('waiting_trip.id'))
    waiting_trip_comment = db.Column(db.String(255), nullable=False)
    passenger_status = db.Column(db.String(55), nullable=False)
    shared_distance = db.Column(db.Float, nullable=False)
    yacka_points_amount = db.Column(db.Float, nullable=False)
    fr_info = db.Column(db.Integer, nullable=False)
    pickled_when = db.Column(db.PickleType, nullable = False)

    shared_trip = db.relationship("Shared_trip",foreign_keys=[shared_trip_id], lazy="joined")
    waiting_trip = db.relationship("Waiting_trip",foreign_keys=[waiting_trip_id], lazy="joined")

    def __repr__(self):
        return "<Wtrip_list {} {} {} {} {} {} {} {} {}>".format(
          repr(self.id),
          repr(self.shared_trip_id),
          repr(self.waiting_trip_id),
          repr(self.waiting_trip_comment),
          repr(self.passenger_status),
          repr(self.shared_distance),
          repr(self.yacka_points_amount),
          repr(self.fr_info),
          repr(self.pickled_when)
          )
