from yacka import app,config_name,environments
from main import db
from flask import request
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client