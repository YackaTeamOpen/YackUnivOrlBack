from main import db
from main.model.incentive import Incentive
from main.model.incentives import Incentives


def create_incentive(amont):
    incentive=Incentive(amont=amont)
    db.session.add(incentive)
    db.session.commit()

def get_incentive(incentive_id):
    return Incentive.query.filter(Incentive.id == incentive_id).first()

def get_incentives_by_user(user_id):
    return Incentive.query.filter(Incentive.user_id == user_id).all()

def get_incentives(driver_id,passenger_id):
    return Incentives.query.join(Incentive,
                                 (Incentive.user_id==Incentives.incentive_driver_id)
                                 | (Incentive.user_id==Incentives.incentive_passenger_id) ).\
                            filter((Incentives.incentive_driver.user_id==driver_id)
                                   & (Incentives.incentive_passenger.user_id==passenger_id)).all()
