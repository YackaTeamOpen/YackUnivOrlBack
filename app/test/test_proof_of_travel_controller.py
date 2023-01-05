import pytest
from main.controller.proof_of_travel_controller import *
from main.model.user import User
from main.service.user_service import setup_password,getUserByEmail,getUserById
from main.service.proof_of_travel_service import (
    list_shared_trip_terminate_candidates,
    get_one_shared_trip_terminate_candidates
)
from main.model.incentive import Incentive
from main.model.incentives import Incentives
from main import db
from main.service.incentive_service import (
    create_incentive,
    create_incentives,
    get_incentive,
    get_incentives,
    get_incentives_by_id,
    get_incentives_by_user,
    get_incentives_by_wtrip
)
from main.service.history_service import get_history_by_shared_trip_id
from main.service.proof_of_travel_service import getProofByUser
from . import client


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


def test_login_driver_successful(client,get_user_sht):
    login = client.post("/login",data=dict(email=get_user_sht.email,
                                           password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                        follow_redirects=True)
    assert login.status_code == 200

def test_login_passenger_successful(client,get_passenger_sht):
    login = client.post("/login",data=dict(email=get_passenger_sht.email,
                                           password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                        follow_redirects=True)
    assert login.status_code == 200

def test_proof_of_travel_created(client,get_user_sht,get_sht_terminate_candidate):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    proof = client.post("/proof/create",data=dict(sht_id=get_sht_terminate_candidate["shared_trip"].id))
    assert proof.status_code == 201

def test_proof_of_travel_already_created(client,get_user_sht,get_sht_terminate_candidate):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    proof = client.post("/proof/create", data=dict(sht_id=get_sht_terminate_candidate["shared_trip"].id))
    assert proof.status_code == 409

def test_proof_of_travel_unauthorized(client,get_user_sht,get_sht_terminate_candidate):
    proof = client.post("/proof/create", data={"sht_id": get_sht_terminate_candidate["shared_trip"].id})
    assert proof.status_code == 401


def test_get_proof_of_travel_by_id(client,get_user_sht):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    id = getProofByUser(get_user_sht.id).id
    proof = client.get("/proof/"+str(id))
    assert proof.status_code == 200


def test_get_proof_of_travel_by_id_unauthorized(client,get_user_sht):
    id = getProofByUser(get_user_sht.id).id
    proof = client.get("/proof/"+str(id))
    assert proof.status_code == 401

def test_get_proof_of_travel_by_id_notfound(client, get_user_sht):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    proof = client.get("/proof/blabla")
    assert proof.status_code == 404

def test_modify_proof_of_travel(client,get_user_sht):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    id = getProofByUser(get_user_sht.id).id
    proof = client.put("/proof/"+str(id))
    assert proof.status_code == 204

def test_modify_proof_of_travel_unauthorized(client,get_user_sht):
    id = getProofByUser(get_user_sht.id).id
    proof = client.put("/proof/"+str(id))
    assert proof.status_code == 401

def test_modify_proof_of_travel(client, get_user_sht):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    proof = client.put("/proof/blabla")
    assert proof.status_code == 404


def test_count_proofs_by_company(client,get_user_sht):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    nb = client.get("/proof/"+str(get_user_sht.organization_id)+"/counts/"+str(get_user_sht.id))
    assert nb.status_code == 200

def test_count_proofs_by_company_unauthorized(client,get_user_sht):
    nb = client.get("/proof/"+str(get_user_sht.organization_id)+"/counts/"+str(get_user_sht.id))
    assert nb.status_code == 401


def test_count_proofs_by_driver(client,get_user_sht):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    nb = client.get("/proof/"+str(get_user_sht.organization_id)+"/counts/"+str(get_user_sht.id)+"/driver")
    assert nb.status_code == 200

def test_count_proofs_by_driver_unauthorized(client,get_user_sht):
    nb = client.get("/proof/"+str(get_user_sht.organization_id)+"/counts/"+str(get_user_sht.id)+"/driver")
    assert nb.status_code == 401

def test_count_proofs_by_passenger(client,get_passenger_sht):
    client.post("/login", data=dict(email=get_passenger_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    nb = client.get("/proof/"+str(get_passenger_sht.organization_id)+"/counts/"+str(get_passenger_sht.id)+"/passenger")
    assert nb.status_code == 200

def test_count_proofs_by_passenger_unauthorized(client,get_passenger_sht):
    nb = client.get("/proof/"+str(get_passenger_sht.organization_id)+"/counts/"+str(get_passenger_sht.id)+"/passenger")
    assert nb.status_code == 401