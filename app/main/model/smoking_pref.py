from .. import db

class Smoking_pref(db.Model):
    """ Smoking_pref Model for storing smoking_pref related details """
    __tablename__ = "smoking_pref"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Smoking_pref {} {}>".format(self.id, self.label)
