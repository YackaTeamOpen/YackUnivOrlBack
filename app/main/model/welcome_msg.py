from .. import db

class WelcomeMessage(db.Model):
    """ Trip Model for storing trip related details """
    __tablename__ = "welcome_msg"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(10000), nullable=False)
    state = db.Column(db.Integer, nullable=False) #0 : deactivated, 1 : activated

    def __repr__(self):
        return "<WelcomeMessage {} {} {}>".format(self.id, self.message, self.state)
