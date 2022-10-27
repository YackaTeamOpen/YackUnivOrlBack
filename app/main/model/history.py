# Redéfini par Olivier pour faire de cette table l'endroit où on stocke les états
# successifs d'un shared_trip (pour garder une trace et éventuellement faire des
# statistiques). Février 2021.

from .. import db

from main.model.user import User

class History(db.Model):
    """ History Model for saving the successive status and details of a shared_trip """
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    passenger_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    path_json = db.Column(db.JSON, nullable=False)
    occ_details_pickle = db.Column(db.PickleType, nullable=False)
    shared_trip_status= db.Column(db.String(55),nullable=False)
    driver_status = db.Column(db.String(55), nullable=False)
    passenger_status = db.Column(db.String(55), nullable=False)
    pickled_when = db.Column(db.PickleType, nullable = False)
    shared_distance = db.Column(db.Float, nullable=False)
    yacka_points_amount = db.Column(db.Float, nullable=False)
    status_set_date = db.Column(db.DateTime, nullable=False)
    # On garde trace aussi du shared_trip.id et du wtrip_list.id, mais sans
    # créer de relation, car il se peut qu'on supprime à terme (après sauvegarde)
    # les shared_trip/wrip_list inactifs ("terminated") pour éviter une BDD
    # trop volumineuse. Les 2 champs suivants ne serviront donc à accéder (avec
    # jointure au moment requis) au contenu des shared_trip/wtrip_list qu'autant
    # que les enregistrements correspondants existent encore dans les tables
    # shared_trip et wtrip_list.
    # En revanche, c'est le champ wtrip_list qui permettra de faire un lien entre
    # le shared_trip/wtrip_list à un moment donné (càd ce qui est convenu à un
    # moment donné entre deux usagers) et le trajet réel tel qu'il a été effectué
    # (info qui se trouvera dans la table proof_of_travel), afin de faire le lien,
    # même longtemps après, entre ce qui était convenu et ce qui s'est réellement
    # passé.
    shared_trip_id = db.Column(db.Integer, nullable=False)
    wtrip_list_id = db.Column(db.Integer, nullable=False)

    driver = db.relationship("User",foreign_keys=[driver_id])
    passenger = db.relationship("User",foreign_keys=[passenger_id])

    def __repr__(self) :
        return "<History object " + repr(self.id)\
            + " " + repr(self.driver_id)\
            + " " + repr(self.passenger_id)\
            + " " + repr(self.path_json)\
            + " " + repr(self.occ_details_pickle)\
            + " " + repr(self.shared_trip_status)\
            + " " + repr(self.driver_status)\
            + " " + repr(self.passenger_status)\
            + " " + repr(self.pickled_when)\
            + " " + repr(self.shared_distance)\
            + " " + repr(self.yacka_points_amount)\
            + " " + repr(self.status_set_date)\
            + " " + repr(self.shared_trip_id)\
            + " " + repr(self.wtrip_list_id)\
            + ">"
