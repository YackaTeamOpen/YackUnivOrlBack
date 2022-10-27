from .. import db

from main.model.address import Address
from main.model.user import User
from main.model.car import Car
from main.model.event_occurrence import Event_occurrence

class Trip(db.Model):
    """ Trip Model for storing trip related details """
    __tablename__ = "trip"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    arrival_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    state = db.Column(db.Integer, nullable=False)
    waypoint_address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable = True)
    creation_date = db.Column(db.DateTime, nullable=False)
    heading = db.Column(db.Float, nullable=False)
    single_trip = db.Column(db.Integer, nullable=False)
    validity_start_date = db.Column(db.DateTime, nullable=True)
    validity_end_date = db.Column(db.DateTime, nullable=True)
    recurrence_rule = db.Column(db.String(500), nullable=True)
    pickled_when = db.Column(db.PickleType, nullable = False)
    directions_json = db.Column(db.JSON, nullable=True)
    free_ratio = db.Column(db.Integer, nullable=False)
    event_occurrence_id = db.Column(db.Integer, db.ForeignKey('event_occurrence.id'), nullable=True)
    nb_seats = db.Column(db.Integer, nullable=True)
    nb_stops = db.Column(db.Integer, nullable=True)

    start_address = db.relationship("Address",foreign_keys=[start_address_id], lazy="joined")
    arrival_address = db.relationship("Address",foreign_keys=[arrival_address_id], lazy="joined")
    waypoint_address = db.relationship("Address",foreign_keys=[waypoint_address_id])
    driver = db.relationship("User",foreign_keys=[driver_id])
    car = db.relationship("Car",foreign_keys=[car_id])

    def __repr__(self):
        return "<Trip {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}>".format(
          self.id,
          self.start_address_id,
          self.arrival_address_id,
          self.driver_id,
          self.start_time,
          self.arrival_time,
          self.comment,
          self.car_id,
          self.state,
          self.waypoint_address_id,
          self.creation_date,
          self.heading,
          self.single_trip,
          self.validity_start_date,
          self.validity_end_date,
          self.recurrence_rule,
          self.pickled_when,
          self.directions_json,
          self.free_ratio,
          self.event_occurrence_id,
          self.nb_seats,
          self.nb_stops
          )
