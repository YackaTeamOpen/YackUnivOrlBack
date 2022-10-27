from .. import db

class Music_pref(db.Model):
    """ Music_pref Model for storing music_pref related details """
    __tablename__ = "music_pref"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Music_pref {} {}>".format(self.id, self.label)
