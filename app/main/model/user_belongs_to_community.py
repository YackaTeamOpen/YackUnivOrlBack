from .. import db



class User_belongs_to_community(db.Model):
    """Model for storing the relation between a user and a community"""

    __tablename__ = "user_belongs_to_community"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = True)
    community_id = db.Column(db.Integer, db.ForeignKey("community.id"), nullable = True)

    user = db.relationship("User", foreign_keys=[user_id])
    community = db.relationship("Community", foreign_keys=[community_id])

    def __repr__(self):
        return "<User_belongs_to_community {} {}>".format(
            self.user_id,
            self.community_id,
        )
