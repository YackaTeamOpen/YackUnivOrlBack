from .. import db


class Address(db.Model):
    """Address Model for storing address related details"""

    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    state = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return "<Address {}	{} {} {} {} {} {} {}>".format(
            self.id,
            self.user_id,
            self.street,
            self.city,
            self.zipcode,
            self.latitude,
            self.longitude,
            self.state
        )
