from .. import db

class Car(db.Model):
  """ Car Model for storing car related details """
  __tablename__ = "car"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
  label = db.Column(db.String(50), nullable=False)
  state = db.Column(db.Integer, nullable=False)

  user = db.relationship("User",foreign_keys=[user_id])

  def __repr__(self):
    return "<Trip {} {} {} {}>".format(
    self.id,
    self.user_id,
    self.label,
    self.state
    )
