import pytest
from sqlalchemy.orm import aliased
from main.model.user import User
from main.model.incentive import Incentive
from main.model.incentives import Incentives
from main.service.user_service import setup_password,getUserByEmail,getUserById
from main.service.proof_of_travel_service import (
    list_shared_trip_terminate_candidates,
    get_one_shared_trip_terminate_candidates
)
from main.service.history_service import get_history_by_shared_trip_id
from main.service.incentive_service import (
    create_incentive,
    create_incentives,
    get_incentive,
    get_incentives_by_id,
    get_incentives_by_user,
    get_incentivesDriver,
    get_incentivesPassenger,
    get_incentives,
    get_incentives_by_wtrip
)
from . import *

@pytest.fixture()
def get_sht_terminate_candidate():
    sht_wtl = get_one_shared_trip_terminate_candidates()
    sht = sht_wtl[0]
    wtl=sht_wtl[1]
    dicti={}
    dicti["shared_trip"]=sht
    dicti["wtrip_list"]=wtl
    yield dicti

@pytest.fixture()
def get_user_sht(get_sht_terminate_candidate):
    history=get_history_by_shared_trip_id(get_sht_terminate_candidate["shared_trip"].id)[0]
    driver=getUserById(history.driver_id)
    yield driver

@pytest.fixture()
def get_passenger_sht(get_sht_terminate_candidate):
    history=get_history_by_shared_trip_id(get_sht_terminate_candidate["shared_trip"].id)[0]
    passenger=getUserById(history.passenger_id)
    yield passenger



@pytest.fixture()
def incentive_driver_created(get_user_sht):
    incentive = create_incentive(50,get_user_sht.id)
    yield incentive["id"]


@pytest.fixture()
def incentive_passenger_created(get_passenger_sht):
    incentive = create_incentive(50,get_passenger_sht.id)
    yield incentive["id"]

@pytest.fixture()
def incentives_created(get_user_sht,get_passenger_sht,get_sht_terminate_candidate):
    incentives = create_incentives(get_passenger_sht.id,get_user_sht.id, get_sht_terminate_candidate["wtrip_list"].id)
    yield incentives["id"]


@pytest.fixture()
def incentive_driver(incentive_driver_created):
    incentive = get_incentive(incentive_driver_created)
    yield incentive

@pytest.fixture()
def incentive_passenger(incentive_passenger_created):
    incentive = get_incentive(incentive_passenger_created)
    yield incentive

@pytest.fixture()
def incentives(incentives_created):
    incentive = get_incentives_by_id(incentives_created)
    yield incentive

def test_get_incentive_driver_by_id(incentive_driver):
    incentive = get_incentive(incentive_driver.id)

    assert incentive.id == incentive_driver.id

def test_get_incentive_passenger_by_id(incentive_passenger):
    incentive = get_incentive(incentive_passenger.id)
    assert incentive.id == incentive_passenger.id


def test_get_incentive_by_id_not_exist():
    id=100
    incentive = get_incentive(id)
    assert incentive == None


def test_get_incentives_existing(get_user_sht,get_passenger_sht,get_sht_terminate_candidate,incentives):
    incentive = get_incentives(get_user_sht.id,get_passenger_sht.id,get_sht_terminate_candidate["wtrip_list"].id)
    assert incentive.id == incentives.id

def test_get_incentives_not_existing():
    id_driver=1000
    id_passenger=1000
    id_wtrip=1000
    incentives = get_incentives(id_driver,id_passenger,id_wtrip)
    assert incentives == None

def test_get_incentive_by_id_driver_existing(get_user_sht,incentives):
    incentive = get_incentivesDriver(get_user_sht.id)
    assert incentives in incentive

def test_get_incentive_by_id_driver_not_existing(get_passenger_sht):
    incentive = get_incentivesDriver(get_passenger_sht.id)
    assert incentive == []

def test_get_incentive_by_id_passenger_existing(get_passenger_sht,incentives):
    incentive = get_incentivesPassenger(get_passenger_sht.id)
    assert incentives in incentive

def test_get_incentive_by_id_passenger_not_existing(get_user_sht):
    incentive = get_incentivesPassenger(get_user_sht.id)
    assert incentive == []

def test_get_incentive_by_user_existing(get_user_sht,incentive_driver):
    incentives = get_incentives_by_user(get_user_sht.id)
    assert incentive_driver in incentives

def test_get_incentive_by_user_not_existing(get_user_sht):
    id_user=1000
    incentive = get_incentives_by_user(id_user)
    assert incentive == []

def test_get_incentive_by_wtrip_existing(get_user_sht,get_sht_terminate_candidate):
    incentives = get_incentives_by_wtrip(get_sht_terminate_candidate["wtrip_list"].id)
    assert incentives.wtrip_list_id == get_sht_terminate_candidate["wtrip_list"].id


def test_get_incentive_by_wtrip_not_existing(get_user_sht,get_sht_terminate_candidate):
    id_wtrip=1
    incentives = get_incentives_by_wtrip(id_wtrip)
    assert incentives == None