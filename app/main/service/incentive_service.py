from main import db
from sqlalchemy.orm import aliased
from main.model.incentive import Incentive
from main.model.incentives import Incentives
from main.model.user import User


def create_incentive(amont,user_id):
    user = User.query.filter(User.id==user_id).first()
    incentive=Incentive(amont=amont,user_id=user.id)
    db.session.add(incentive)
    db.session.commit()

def create_incentives(passenger_id,driver_id,wtrip_list_id):
    incentiveDriver = Incentive.query.filter(Incentive.user_id==driver_id).first()
    incentivePassenger = Incentive.query.filter(Incentive.user_id == passenger_id).first()
    incentives=Incentives(incentive_passenger_id=incentivePassenger.id,incentive_driver_id=incentiveDriver.id,wtrip_list_id=wtrip_list_id)
    db.session.add(incentives)
    db.session.commit()

def get_incentive(incentive_id):
    return Incentive.query.filter(Incentive.id == incentive_id).first()

def get_incentives_by_user(user_id):
    return Incentive.query.filter(Incentive.user_id == user_id).all()

def get_incentivesDriver(driver_id):
    incentivesDriver = Incentives.query\
                                .join(Incentive, (Incentive.id==Incentives.incentive_driver_id))\
                            .filter((Incentive.user_id==driver_id)).all()
    return incentivesDriver

def get_incentivesPassenger(passenger_id):
    incentives = Incentives.query.join(Incentive, (Incentive.id==Incentives.incentive_passenger_id))\
                               .filter((Incentive.user_id==passenger_id)).all()
    return incentives

def get_incentives(driver_id, passenger_id, wtrip_list_id):
    incentiveDriver = aliased(Incentive)
    incentivePassenger=aliased(Incentive)
    incentives = Incentives.query.join(incentiveDriver, (incentiveDriver.id == Incentives.incentive_driver_id)) \
            .join(incentivePassenger, incentivePassenger.id== Incentives.incentive_passenger_id)\
        .filter((incentiveDriver.user_id == driver_id) & (incentivePassenger.user_id == passenger_id)
                & (Incentives.wtrip_list_id==wtrip_list_id)).first()
    return incentives

def get_incentives_by_wtrip(wtrip_list_id):
    incentives = Incentives.query.filter(Incentives.wtrip_list_id==wtrip_list_id).first()
    return incentives