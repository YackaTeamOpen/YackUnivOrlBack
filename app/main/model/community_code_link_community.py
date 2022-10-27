from .. import db



class Community_code_link_community(db.Model):
    """Model for a community code link to community"""

    __tablename__ = "community_code_link_community"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    community_id = db.Column(db.Integer, db.ForeignKey("community.id"), nullable=True)
    community_code_id = db.Column(db.Integer, db.ForeignKey("community_code.id"), nullable=True)

    community = db.relationship("Community", foreign_keys=[community_id])
    community_code = db.relationship("Community_code", foreign_keys=[community_code_id])

    def __repr__(self):
        return "<Community_code_link_community {} {}>".format(
            self.id,
            self.community_id,
            self.community_code_id,
        )
