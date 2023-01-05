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
@pytest.fixture()
def incentive_driver_created(get_user_sht):
    incentive = create_incentive(50,get_user_sht.id)
    yield incentive["id"]


@pytest.fixture()
def incentive_passenger_created(get_passenger_sht):
    incentive = create_incentive(50,get_passenger_sht.id)
    yield incentive["id"]

@pytest.fixture()
def incentives_created(get_sht_terminate_candidate,incentive_passenger_created,incentive_driver_created):
    incentiveDriver = get_incentive(incentive_driver_created).user_id
    incentivePassenger = get_incentive(incentive_passenger_created).user_id
    incentives = create_incentives(incentivePassenger,incentiveDriver, get_sht_terminate_candidate["wtrip_list"].id)
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

@pytest.fixture()
def histories_shared_trip(get_sht_terminate_candidate):
    histories = get_history_by_shared_trip_id(get_sht_terminate_candidate["shared_trip"].id)
    yield histories

@pytest.fixture()
def create_proof_of_travel(histories_shared_trip,get_sht_terminate_candidate,incentives):
    dict={}
    proofs=[]
    for history in histories_shared_trip:
        for i in range(len(history.path_json)):
            if i == history.occ_details_pickle[0]["start_path_index"]:
                dict["driver_start_latitude"] = history.path_json[i][1]
                dict["driver_start_longitude"] = history.path_json[i][0]
            if i == history.occ_details_pickle[0]["arrival_path_index"]:
                dict["driver_end_latitude"] = history.path_json[i][1]
                dict["driver_end_longitude"] = history.path_json[i][0]

            if i == history.occ_details_pickle[len(history.occ_details_pickle) - 1]["start_path_index"]:
                dict["passenger_start_latitude"] = history.path_json[i][1]
                dict["passenger_start_longitude"] = history.path_json[i][0]
            if i == history.occ_details_pickle[len(history.occ_details_pickle) - 1]["arrival_path_index"]:
                dict["passenger_end_latitude"] = history.path_json[i][1]
                dict["passenger_end_longitude"] = history.path_json[i][0]
        proof = Proof_of_travel(proof_class="C",
                driver_id=history.driver_id,
                driver_iso_start_time=history.occ_details_pickle[0]["start_time"],
                driver_start_latitude=dict["driver_start_latitude"],
                driver_start_longitude=dict["driver_start_longitude"],
                driver_iso_end_time=history.occ_details_pickle[0]["arrival_time"],
                driver_end_latitude=dict["driver_end_latitude"],
                driver_end_longitude=dict["driver_end_longitude"],
                passenger_id=history.passenger_id,
                passenger_iso_start_time=history.occ_details_pickle[len(history.occ_details_pickle) - 1]["start_time"],
                passenger_start_latitude=dict["passenger_start_latitude"],
                passenger_start_longitude=dict["passenger_start_longitude"],
                passenger_iso_end_time=history.occ_details_pickle[len(history.occ_details_pickle) - 1]["arrival_time"],
                passenger_end_latitude=dict["passenger_end_latitude"],
                passenger_end_longitude=dict["passenger_end_longitude"],
                passenger_seats=1,
                passenger_contribution=0,
                driver_revenue=0,
                incentive_id=incentives.id,
                wtrip_list_id=history.wtrip_list_id
        )
        db.session.add(proof)
        db.session.commit()
        proofs.append(proof)
    yield proofs


@pytest.fixture()
def get_id_proof_driver(get_user_sht,create_proof_of_travel):
    proof=getProofByUser(get_user_sht.id)
    yield proof.id

@pytest.fixture()
def get_id_proof_passenger(get_passenger_sht,create_proof_of_travel):
    proof=getProofByUser(get_passenger_sht.id)
    yield proof.id

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
    proof = client.post("/proof/create",data={"sht_id":get_sht_terminate_candidate["shared_trip"].id})
    assert proof.status_code == 201

def test_proof_of_travel_already_created(client,get_user_sht,get_sht_terminate_candidate):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    proof = client.post("/proof/create", data={"sht_id": get_sht_terminate_candidate["shared_trip"].id})
    assert proof.status_code == 409

def test_proof_of_travel_unauthorized(client,get_user_sht,get_sht_terminate_candidate):
    proof = client.post("/proof/create", data={"sht_id": get_sht_terminate_candidate["shared_trip"].id})
    assert proof.status_code == 401


def test_get_proof_of_travel_by_id(client,get_user_sht,get_id_proof_driver):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    proof = client.get("/proof/"+str(get_id_proof_driver))
    assert proof.status_code == 200


def test_get_proof_of_travel_by_id_unauthorized(client,get_user_sht,get_id_proof_driver):
    proof = client.get("/proof/"+str(get_id_proof_driver))
    assert proof.status_code == 401

def test_get_proof_of_travel_by_id_notfound(client, get_user_sht, get_id_proof_driver):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    proof = client.get("/proof/blabla")
    assert proof.status_code == 404

def test_modify_proof_of_travel(client,get_user_sht,get_id_proof_driver):
    client.post("/login", data=dict(email=get_user_sht.email,
                                    password="6aa07aaf6f8a0a553d257f048770304d483c92fdfea159c7ebcdbe3b72df49ea"),
                follow_redirects=True)
    proof = client.put("/proof/"+str(get_id_proof_driver))
    assert proof.status_code == 204

def test_modify_proof_of_travel_unauthorized(client,get_id_proof_driver):
    proof = client.put("/proof/"+str(get_id_proof_driver))
    assert proof.status_code == 401

def test_modify_proof_of_travel(client, get_user_sht, get_id_proof_driver):
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