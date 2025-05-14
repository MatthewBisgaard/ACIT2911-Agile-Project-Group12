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

@pytest.fixture
def new_user_data():
    new_user_name = str(uuid.uuid4())
    return {
        "username": new_user_name,
        "name": new_user_name+"name",
        "hashpasswd": "1234"
    }


def test_handle_missing_values(client):
    """ Tests to see that the fucntion handles missing form values\n
NOTE: Once flash messages implemented on the forntend uncomment the commented assertations """
    # Test missing username
    res = client.post("/auth/login", data={"hashpasswd": "1234"})
    assert res.status_code == 302 # Test redirect
    # assert b"Username cannot be blank" in res.data

    # Test missing password
    res = client.post("/auth/login", data={"username": "1234"})
    assert res.status_code == 302 # Test redirect
    # assert b"Password cannot be blank" in res.data

    res = client.post("/auth/login")
    assert res.status_code == 302
    # assert b"cannot be blank" in res.data

def test_regular_signin(client, new_user_data):
    """ Tests signing in as a regular user  """
    
    hash = hashlib.sha256(new_user_data["hashpasswd"].encode())
    hash.update(b"salt")
    db_version_password_hash = hash.hexdigest()

    with app.app_context():
        new_user = User(name=new_user_data["name"], username = new_user_data["username"], password=db_version_password_hash, salt = "salt")
        db.session.add(new_user)
        db.session.commit()

    res = client.post("/auth/login", data=new_user_data)
    assert client.get_cookie("session") is not None # Test signin cookie received
    assert res.status_code == 302 # Test redirect after successful signin