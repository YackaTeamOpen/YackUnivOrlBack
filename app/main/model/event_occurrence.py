from .. import db

from main.model.event import Event
from main.model.community import Community


class Event_occurrence(db.Model):
    """ Event_occurrence Model for storing event occurrences details """
    __tablename__ = "event_occurrence"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    open_occurrence = db.Column(db.Boolean, nullable=False, default=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)

    event = db.relationship("Event",foreign_keys=[event_id])
    community = db.relationship("Community",foreign_keys=[community_id])

    def __repr__(self):
        return "<Event_occurrence {} {} {} {} {} {} {} {} {}>".format(
          repr(self.id),
          repr(self.event_id),
          repr(self.name),
          repr(self.open_occurrence),
          repr(self.community_id),
          repr(self.start_time),
          repr(self.comment),
          repr(self.state),
          repr(self.creation_date)
          )
