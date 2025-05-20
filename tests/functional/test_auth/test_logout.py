import pytest
from app import app
import uuid
import hashlib
from db import db
from models import User

@pytest.fixture
def client():
    """ Testing client for functions regarding completion """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_logout_signs_out(client):
    """ Tests that the lgout route actually logs clients out """
    client.post("/auth/login", data={"username":"tom", "hashpasswd": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"})
    res = client.get("/dashboard")
    assert res.status_code == 200 # Login works and we know the client can log out now

    client.get("/auth/logout")
    res = client.get("/dashboard")
    assert res.status_code == 302 # Redirected as client had been logged out
