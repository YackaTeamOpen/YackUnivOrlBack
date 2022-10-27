from .. import db

from main.model.user import User


class Message(db.Model):
    """ Message Model for storing messages related details """
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(500), nullable=False)
    alert_level = db.Column(db.Integer, nullable=True)
    send_date = db.Column(db.DateTime, nullable=False)
    read_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<Message {} {} {} {} {} {} {}>".format(self.id, self.user1, self.user2, self.message, self.alert_level, self.send_date, self.read_date)
