from .. import db

from main.model.address import Address
from main.model.user import User
from main.model.event_occurrence import Event_occurrence

class Waiting_trip(db.Model):
    """ Waiting_trip Model for storing waiting_trip related details """
    __tablename__ = "waiting_trip"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    arrival_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    passenger_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    heading = db.Column(db.Float, nullable=False)
    single_trip = db.Column(db.Integer, nullable=False)
    validity_start_date = db.Column(db.DateTime, nullable=True)
    validity_end_date = db.Column(db.DateTime, nullable=True)
    recurrence_rule = db.Column(db.String(500), nullable=True)
    pickled_when = db.Column(db.PickleType, nullable = False)
    directions_json = db.Column(db.JSON, nullable=True)
    event_occurrence_id = db.Column(db.Integer, db.ForeignKey('event_occurrence.id'), nullable=True)
    nb_passengers = db.Column(db.Integer, nullable=True)

    start_address = db.relationship("Address", foreign_keys=[start_address_id], lazy="joined")
    arrival_address = db.relationship("Address", foreign_keys=[arrival_address_id], lazy="joined")
    passenger = db.relationship("User", foreign_keys=[passenger_id])

    def __repr__(self):
        return "<Waiting_trip {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} >".format(
          self.id,
          self.start_address_id,
          self.arrival_address_id,
          self.passenger_id,
          self.start_time,
          self.creation_date,
          self.comment,
          self.state,
          self.heading,
          self.single_trip,
          self.validity_start_date,
          self.validity_end_date,
          self.recurrence_rule,
          self.pickled_when,
          self.directions_json,
          self.event_occurrence_id,
          self.nb_passengers
          )
