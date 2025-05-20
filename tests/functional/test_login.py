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
    """ Tests to see that the fucntion handles missing form values """
    # Test missing username
    res = client.post("/auth/login", data={"hashpasswd": "1234"})
    assert res.status_code == 302 # Test redirect
    res = client.get("/auth/login")
    assert b"Username cannot be blank" in res.data

    # Test missing password
    res = client.post("/auth/login", data={"username": "1234"})
    assert res.status_code == 302 # Test redirect
    res = client.get("/auth/login")
    assert b"Password cannot be blank" in res.data

    res = client.post("/auth/login")
    assert res.status_code == 302
    res = client.get("/auth/login")

    assert b"cannot be blank" in res.data

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
    assert res.status_code == 302 # Test redirect after successful 
    
def test_get_signin_page(client):
    """ Test that a get request to the route will get the login page (Looks at title)"""
    res = client.get("/auth/login")
    assert b"<title>Log In</title>" in res.data

def test_signin_with_user_that_does_not_exist(client):
    """ Tries to sign in with a user that does not exist. Checks for a redirect and the expected error message"""
    res = client.post("/auth/login", data={"username": "Richard Hammond", "hashpasswd": "BlitheringIdiot"})
    assert res.status_code == 302 # Check redirect
    
    res = client.get("/auth/login")
    assert b"Username or password may be correct" in res.data # Check that the correct error message pops up

def test_signin_with_bad_password(client):
    """ Checks that the message for signing into an existing user with a bad password does not work """
    res = client.post("/auth/login", data={"username": "tom", "hashpasswd": "KHANNNNN"})
    assert res.status_code == 302 # Redirects back to login

    res = client.get("/auth/login")
    assert b"Username or password may be correct" in res.data # Check that the correct error message pops up
    
def test_redirect_with_next(client, new_user_data):
    """ Tests to make sure the url in the next query string is what the client gets redirected to after sign in """
    hash = hashlib.sha256(new_user_data["hashpasswd"].encode())
    hash.update(b"salt")
    db_version_password_hash = hash.hexdigest()

    with app.app_context():
        new_user = User(name=new_user_data["name"], username = new_user_data["username"], password=db_version_password_hash, salt = "salt")
        db.session.add(new_user)
        db.session.commit()

    res = client.post("/auth/login?next=%2Fdashboard", data=new_user_data, follow_redirects=True)
    assert res.request.path == "/dashboard" # Check that the new user is redirected to the dahsboard as the next param indicates