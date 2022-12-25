# Table contenant les infos relatives aux trajets effectivement réalisés par les
# usagers de l'app. Sa structure est inspirée des CGU du repo Github de la
# preuve de covoiturage :
# https://github.com/betagouv/preuve-covoiturage-doc/blob/master/cgu.md
# Olivier - Février 2021.

from .. import db

from main.model.user import User

class Proof_of_travel(db.Model):
    """ Proof_of_travel Model for saving the actual travel made by users. """
    __tablename__ = "proof_of_travel"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proof_class = db.Column(db.String(1), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    driver_iso_start_time = db.Column(db.DateTime, nullable=False)
    driver_start_latitude = db.Column(db.Float, nullable=False)
    driver_start_longitude = db.Column(db.Float, nullable=False)
    driver_iso_end_time = db.Column(db.DateTime, nullable=False)
    driver_end_latitude = db.Column(db.Float, nullable=False)
    driver_end_longitude = db.Column(db.Float, nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    passenger_iso_start_time = db.Column(db.DateTime, nullable=False)
    passenger_start_latitude = db.Column(db.Float, nullable=False)
    passenger_start_longitude = db.Column(db.Float, nullable=False)
    passenger_iso_end_time = db.Column(db.DateTime, nullable=False)
    passenger_end_latitude = db.Column(db.Float, nullable=False)
    passenger_end_longitude = db.Column(db.Float, nullable=False)
    passenger_seats = db.Column(db.Integer, nullable=False)
    passenger_contribution = db.Column(db.Float, nullable=False)
    driver_revenue = db.Column(db.Float, nullable=False)
    # Selon les CGU, les incentives seraient un tableau, donc au cas où, on prévoit
    # une foreignkey, mais on commente.
    incentive_id = db.Column(db.Integer,
        db.ForeignKey('incentives.id'),
        nullable=False)
    # Enfin un champ contenant la valeur du wtrip_list associé au shared_trip
    # d'origine, permettant de retrouver, grâce à la table history, les différents
    # stades du "contrat" initialement passé entre les deux usagers, et notamment
    # les termes de celui-ci en vigueur au moment du voyage réel.
    wtrip_list_id = db.Column(db.Integer, nullable=False)

    driver = db.relationship("User",foreign_keys=[driver_id])
    passenger = db.relationship("User",foreign_keys=[passenger_id])
    incentive = db.relationship("Incentives",foreign_keys=[incentive_id])


    def __repr__(self):
        return "<Proof_of_travel {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} >".format(
            self.id,
            self.proof_class,
            self.driver_id,
            self.driver_iso_start_time,
            self.driver_start_latitude,
            self.driver_start_longitude,
            self.driver_iso_end_time,
            self.driver_end_latitude,
            self.driver_end_longitude,
            self.passenger_id,
            self.passenger_iso_start_time,
            self.passenger_start_latitude,
            self.passenger_start_longitude,
            self.passenger_iso_end_time,
            self.passenger_end_latitude,
            self.passenger_end_longitude,
            self.passenger_seats,
            self.passenger_contribution,
            self.driver_revenue,
            self.incentive_id,
            self.wtrip_list_id
        )
