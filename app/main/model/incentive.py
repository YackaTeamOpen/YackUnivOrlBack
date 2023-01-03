from .. import  db


class Incentive(db.Model):
    """Model for storing the incentive of an user"""

    __tablename__ = "incentive"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    amont = db.Column(db.Float, nullable=False)

    user = db.relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return "<Incentive {} {} {}>".format(
            self.id,
            self.user_id,
            self.amont
        )