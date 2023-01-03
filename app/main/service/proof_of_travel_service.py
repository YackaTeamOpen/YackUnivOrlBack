from flask_login import current_user

from main import db
from main.model.proof_of_travel import Proof_of_travel

def getAllProof():
    return Proof_of_travel.query.all()

def createProof(driver_id, passenger_id, trip_id):
    pass

def validateProof(proof_id):
    pass

def getProofById(proof_id):
    proof = Proof_of_travel.query.filter_by(id=proof_id).first()
    return proof

def getProofByUser(user_id):
    pass

def getNbProofByUserAsDriver(user_id):
    proofs = Proof_of_travel.query.filter_by(driver_id=user_id)
    return len(proofs)

def getNbProofByUserAsPassenger(user_id):
    proofs = Proof_of_travel.query.filter_by(passenger_id=user_id)
    return len(proofs)

def getNbKmByUserAsDriver(user_id):
    proofs = Proof_of_travel.query.filter_by(driver_id=user_id)
    pass

def getNbKmByUserAsPassenger(user_id):
    proofs = Proof_of_travel.query.filter_by(passenger_id=user_id)
    pass


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def commit():
    db.session.commit()