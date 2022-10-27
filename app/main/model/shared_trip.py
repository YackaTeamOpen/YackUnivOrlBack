from .. import db

from main.model.trip import Trip


class Shared_trip(db.Model):
    """Model for storing the trip details once 2+ people consider to share it"""

    __tablename__ = "shared_trip"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"))
    driver_score = db.Column(db.Integer, nullable=False)
    passengers_score = db.Column(db.Integer, nullable=False)
    path_json = db.Column(db.JSON, nullable=False)
    directions_json = db.Column(db.JSON, nullable=False)
    occ_details_pickle = db.Column(db.PickleType, nullable=False)
    shared_trip_comment = db.Column(db.String(255), nullable=False)
    shared_trip_status = db.Column(db.String(55), nullable=False)
    driver_status = db.Column(db.String(55), nullable=False)
    modification_date = db.Column(db.DateTime, nullable=False)

    trip = db.relationship("Trip", foreign_keys=[trip_id])

    def __repr__(self):
        return "<Shared_trip {} {} {} {} {} {} {} {} {} {} {}>".format(
            self.id,
            self.trip_id,
            self.driver_score,
            self.passengers_score,
            self.path_json,
            self.directions_json,
            self.occ_details_pickle,
            self.shared_trip_comment,
            self.shared_trip_status,
            self.driver_status,
            self.modification_date
        )
