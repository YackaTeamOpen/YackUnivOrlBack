from .. import db

class Organization(db.Model):
    """ Organization Model for storing organization related details """
    __tablename__ = "organization"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    siret = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(191), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'))

    bill = db.relationship("Bill",foreign_keys=[bill_id])

    def __repr__(self):
        return "<Organization {} {} {} {} {} {} {}>".format(self.id, self.name, self.siret, self.address, self.creation_date, self.bill_id, self.bill)
