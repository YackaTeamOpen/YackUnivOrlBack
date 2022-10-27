from .. import db



class Community(db.Model):
    """Model for a community"""

    __tablename__ = "community"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), unique=True, nullable=False)

    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=True)
    organization = db.relationship("Organization", foreign_keys=[organization_id])

    def __repr__(self):
        return "<Community {} {}>".format(
            self.id,
            self.name,
            self.organization_id,
        )
