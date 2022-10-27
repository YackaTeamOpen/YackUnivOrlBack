from .. import db

class Speaking_pref(db.Model):
    """ Speaking_pref Model for storing speaking_pref related details """
    __tablename__ = "speaking_pref"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Speaking_pref {} {}>".format(self.id, self.label)
