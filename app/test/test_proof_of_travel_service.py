import pytest
from sqlalchemy.orm import aliased
from main.model.user import User
from main.model.incentive import Incentive
from main.model.incentives import Incentives
from main.model.history import History
from main.model.wtrip_list import Wtrip_list
from main.model.shared_trip import Shared_trip
from main.model.proof_of_travel import Proof_of_travel
from main.service.user_service import setup_password,getUserByEmail,getUserById
from main.service.proof_of_travel_service import (
    list_shared_trip_terminate_candidates,
    get_one_shared_trip_terminate_candidates,
    createProof,
    getAllProof,
    validateProof,
    getProofById,
    getProofByUser,
    getNbProofByUserAsDriver,
    getNbProofByUserAsPassenger,
    getNbKmByUserAsDriver,
    getNbKmByUserAsPassenger
)
from datetime import datetime
from main.service.trip_service import getTripById
from main.service.history_service import get_history_by_shared_trip_id
from main.service.path_when_service import estimate_real_distance_between,make_path_point_tuple_from_trip
from main.service.incentive_service import (
    create_incentive,
    create_incentives,
    get_incentive,
    get_incentives,
    get_incentives_by_id,
    get_incentives_by_user,
    get_incentives_by_wtrip
)
from pytest_mock import mocker
from main import db
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
def history_shared_trip(get_sht_terminate_candidate):
    history = get_history_by_shared_trip_id(get_sht_terminate_candidate["shared_trip"].id)[0]
    yield history

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
def proof(create_proof_of_travel):
    proof = getProofById(create_proof_of_travel[0].id)
    yield proof

@pytest.fixture()
def get_wtriplist_driver(get_user_sht,get_sht_terminate_candidate):
    proof = getProofByUser(get_user_sht.id)
    wtrip_sht = db.session.query(Wtrip_list, Shared_trip)\
        .join(Proof_of_travel, Wtrip_list.id==proof.wtrip_list_id)\
        .join(Shared_trip, Shared_trip.id == Wtrip_list.shared_trip_id)\
        .filter((Wtrip_list.id == proof.wtrip_list_id)
                & (Wtrip_list.shared_trip_id == get_sht_terminate_candidate["shared_trip"].id)
                & (Wtrip_list.id == get_sht_terminate_candidate["wtrip_list"].id)
                ).first()
    yield wtrip_sht

@pytest.fixture()
def get_wtriplist_passenger(get_passenger_sht,get_sht_terminate_candidate):
    proof = getProofByUser(get_passenger_sht.id)
    wtrip_sht = db.session.query(Wtrip_list, Shared_trip,Proof_of_travel)\
        .join(Proof_of_travel, Wtrip_list.id==proof.wtrip_list_id)\
        .join(Shared_trip, Shared_trip.id == Wtrip_list.shared_trip_id)\
        .filter(
                (Wtrip_list.id == proof.wtrip_list_id) & (Wtrip_list.shared_trip_id == get_sht_terminate_candidate["shared_trip"].id)
                & (Wtrip_list.id == get_sht_terminate_candidate["wtrip_list"].id))\
        .first()
    yield wtrip_sht


def test_create_proof_OK(mocker,history_shared_trip,incentives,get_sht_terminate_candidate):
    dict = {}

    for i in range(len(history_shared_trip.path_json)):
        if i == history_shared_trip.occ_details_pickle[0]["start_path_index"]:
            dict["driver_start_latitude"] = history_shared_trip.path_json[i][1]
            dict["driver_start_longitude"] = history_shared_trip.path_json[i][0]
        if i == history_shared_trip.occ_details_pickle[0]["arrival_path_index"]:
            dict["driver_end_latitude"] = history_shared_trip.path_json[i][1]
            dict["driver_end_longitude"] = history_shared_trip.path_json[i][0]

        if i == history_shared_trip.occ_details_pickle[len(history_shared_trip.occ_details_pickle) - 1]["start_path_index"]:
            dict["passenger_start_latitude"] = history_shared_trip.path_json[i][1]
            dict["passenger_start_longitude"] = history_shared_trip.path_json[i][0]
        if i == history_shared_trip.occ_details_pickle[len(history_shared_trip.occ_details_pickle) - 1]["arrival_path_index"]:
            dict["passenger_end_latitude"] = history_shared_trip.path_json[i][1]
            dict["passenger_end_longitude"] = history_shared_trip.path_json[i][0]
    proof = Proof_of_travel(proof_class="C",
                            driver_id=history_shared_trip.driver_id,
                            driver_iso_start_time=history_shared_trip.occ_details_pickle[0]["start_time"],
                            driver_start_latitude=dict["driver_start_latitude"],
                            driver_start_longitude=dict["driver_start_longitude"],
                            driver_iso_end_time=history_shared_trip.occ_details_pickle[0]["arrival_time"],
                            driver_end_latitude=dict["driver_end_latitude"],
                            driver_end_longitude=dict["driver_end_longitude"],
                            passenger_id=history_shared_trip.passenger_id,
                            passenger_iso_start_time=
                            history_shared_trip.occ_details_pickle[len(history_shared_trip.occ_details_pickle) - 1]["start_time"],
                            passenger_start_latitude=dict["passenger_start_latitude"],
                            passenger_start_longitude=dict["passenger_start_longitude"],
                            passenger_iso_end_time=
                            history_shared_trip.occ_details_pickle[len(history_shared_trip.occ_details_pickle) - 1]["arrival_time"],
                            passenger_end_latitude=dict["passenger_end_latitude"],
                            passenger_end_longitude=dict["passenger_end_longitude"],
                            passenger_seats=1,
                            passenger_contribution=0,
                            driver_revenue=0,
                            incentive_id=incentives.id,
                            wtrip_list_id=history_shared_trip.wtrip_list_id
                            )
    db.session.add(proof)
    db.session.commit()
    result = {"id": proof.id, "status": "success", "message": "Proof of travel created"}, 200
    mock_createProof = mocker.patch("main.service.proof_of_travel_service.createProof", return_value=result)
    mock_createProof(history_shared_trip.driver_id, history_shared_trip.passenger_id, get_sht_terminate_candidate["shared_trip"].trip_id)
    assert mock_createProof.return_value == result

def test_create_proof_not_OK(mocker,history_shared_trip,get_wtriplist_passenger):
    result = {"status": "fail", "message": "Bad datetime"}, 400
    mock_createProof = mocker.patch("main.service.proof_of_travel_service.createProof", return_value=result)
    mock_createProof(history_shared_trip.driver_id, history_shared_trip.passenger_id, get_wtriplist_passenger[1].trip_id)
    assert mock_createProof.return_value == result
def test_get_all_proof_OK():
    proofs = getAllProof()
    print(proofs)
    assert len(proofs) != 0


def test_get_proof_by_id_OK(proof):
    proofs = getProofById(proof.id)
    assert proofs.id is not None
    

def test_get_proof_by_id_not_OK():
    id=1000
    proofs = getProofById(id)
    assert proofs is None

def test_get_proof_by_driver_OK(get_user_sht):
    proof = getProofByUser(get_user_sht.id)
    assert proof.driver_id == get_user_sht.id

def test_get_proof_by_driver_not_OK():
    user_id=1
    proof = getProofByUser(user_id)
    assert proof == None

def test_get_proof_by_passenger_OK(get_passenger_sht):
    proof = getProofByUser(get_passenger_sht.id)
    assert proof.passenger_id == get_passenger_sht.id

def test_get_proof_by_passenger_not_OK():
    user_id=1
    proof = getProofByUser(user_id)
    assert proof == None

def test_get_nb_proofs_by_user_as_driver_OK(get_user_sht):
    length = getNbProofByUserAsDriver(get_user_sht.id)
    assert length > 0

def test_get_nb_proofs_by_user_as_driver_not_OK(get_passenger_sht):
    length = getNbProofByUserAsDriver(get_passenger_sht.id)
    assert length == 0


def test_get_nb_proofs_by_user_as_passenger_OK(get_passenger_sht):
    length = getNbProofByUserAsPassenger(get_passenger_sht.id)
    assert length > 0

def test_get_nb_proofs_by_user_as_passenger_not_OK(get_user_sht):
    length = getNbProofByUserAsPassenger(get_user_sht.id)
    assert length == 0

def test_get_nb_km_by_user_as_driver_OK(mocker,get_user_sht,get_wtriplist_driver):

    trip = getTripById(get_wtriplist_driver[1].trip_id)
    tuple_driver = make_path_point_tuple_from_trip(trip)
    distance_driver =estimate_real_distance_between(tuple_driver[0],tuple_driver[1])/1000
    mock_getNbKmByUserAsDriver = mocker.patch("main.service.proof_of_travel_service.getNbKmByUserAsDriver",return_value=distance_driver)
    mock_getNbKmByUserAsDriver(get_user_sht.id)
    mock_getNbKmByUserAsDriver.assert_called_once_with(get_user_sht.id)
    assert mock_getNbKmByUserAsDriver.return_value == distance_driver

def test_get_nb_km_by_user_as_driver_not_OK(mocker,get_user_sht,get_wtriplist_driver):

    trip = getTripById(get_wtriplist_driver[1].trip_id)
    tuple_driver = make_path_point_tuple_from_trip(trip)
    distance_driver =estimate_real_distance_between(tuple_driver[0],tuple_driver[1])/1000
    mock_getNbKmByUserAsDriver = mocker.patch("main.service.proof_of_travel_service.getNbKmByUserAsDriver",return_value=distance_driver/100)
    mock_getNbKmByUserAsDriver(get_user_sht.id)
    mock_getNbKmByUserAsDriver.assert_called_once_with(get_user_sht.id)
    assert mock_getNbKmByUserAsDriver.return_value != distance_driver


def test_get_nb_km_by_user_as_passenger_OK(mocker,get_passenger_sht,get_wtriplist_passenger):
    trip = getTripById(get_wtriplist_passenger[1].trip_id)
    tuple_passenger = make_path_point_tuple_from_trip(trip)
    distance_passenger =estimate_real_distance_between(tuple_passenger[0],tuple_passenger[1])/1000
    mock_getNbKmByUserAsPassenger = mocker.patch("main.service.proof_of_travel_service.getNbKmByUserAsPassenger",return_value=distance_passenger)
    mock_getNbKmByUserAsPassenger(get_passenger_sht.id)
    mock_getNbKmByUserAsPassenger.assert_called_once_with(get_passenger_sht.id)
    assert mock_getNbKmByUserAsPassenger.return_value == distance_passenger

def test_get_nb_km_by_user_as_passenger_not_OK(mocker,get_passenger_sht,get_wtriplist_passenger):
    trip = getTripById(get_wtriplist_passenger[1].trip_id)
    tuple_passenger = make_path_point_tuple_from_trip(trip)
    distance_passenger =estimate_real_distance_between(tuple_passenger[0],tuple_passenger[1])/1000
    mock_getNbKmByUserAsPassenger = mocker.patch("main.service.proof_of_travel_service.getNbKmByUserAsPassenger",return_value=distance_passenger/100)
    mock_getNbKmByUserAsPassenger(get_passenger_sht.id)
    mock_getNbKmByUserAsPassenger.assert_called_once_with(get_passenger_sht.id)
    assert mock_getNbKmByUserAsPassenger.return_value != distance_passenger

def test_validate_proof_of_travel_passenger_OK(mocker,get_passenger_sht):
    proof = getProofByUser(get_passenger_sht.id)
    mock_validateProof = mocker.patch("main.service.proof_of_travel_service.validateProof",return_value=True)
    mock_validateProof(proof.id)
    mock_validateProof.assert_called_once_with(proof.id)
    assert mock_validateProof.return_value == True

def test_validate_proof_of_travel_passenger_not_OK(mocker,get_passenger_sht):
    proof = getProofByUser(get_passenger_sht.id)
    mock_validateProof = mocker.patch("main.service.proof_of_travel_service.validateProof",return_value=False)
    mock_validateProof(proof.id)
    mock_validateProof.assert_called_once_with(proof.id)
    assert mock_validateProof.return_value == False