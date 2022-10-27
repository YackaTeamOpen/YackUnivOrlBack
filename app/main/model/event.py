from .. import db
from sqlalchemy.dialects.mysql import LONGTEXT
from main.model.address import Address
from main.model.organization import Organization


class Event(db.Model):
    """ Event Model for storing event related details """
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    event_org_name = db.Column(db.String(100), nullable=False)
    single_date = db.Column(db.Boolean, nullable=False)
    beginning_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    name = db.Column(db.String(200), nullable=False)
    event_url = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(191), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    sht_url_ext = db.Column(db.String(40), nullable=True)
    sht_preferred_url_ext = db.Column(db.String(20), nullable=True)
    full_sht_url = db.Column(db.String(255), nullable=True)
    logo = db.Column(LONGTEXT, nullable=True)
    state = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)

    address = db.relationship("Address", foreign_keys=[address_id], lazy="joined")
    organization = db.relationship("Organization", foreign_keys=[organization_id])
    occurrences = db.relationship("Event_occurrence", order_by="Event_occurrence.start_time", back_populates="event", lazy="joined")

    def __repr__(self):
        return "<Event {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}>".format(
          repr(self.id),
          repr(self.organization_id),
          repr(self.event_org_name),
          repr(self.single_date),
          repr(self.beginning_date),
          repr(self.end_date),
          repr(self.name),
          repr(self.event_url),
          repr(self.email),
          repr(self.phone),
          repr(self.address_id),
          repr(self.comment),
          repr(self.sht_url_ext),
          repr(self.sht_preferred_url_ext),
          repr(self.full_sht_url),
          repr(self.state),
          repr(self.creation_date)
          )

