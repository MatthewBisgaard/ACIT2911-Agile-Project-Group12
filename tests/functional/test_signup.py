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


def test_create_new_user(client, new_user_data):
    """ To purely test success of creating a user Creates a new user with a uuid username and name to verify operation fo the signup route """
    client.post("/auth/signup", data=new_user_data)
    with app.app_context():
        # Select via the username
        user_from_username = db.session.execute(db.select(User).where(User.username == new_user_data["username"])).scalar()
        assert user_from_username.username == new_user_data["username"]

        user_from_name = db.session.execute(db.select(User).where(User.name == new_user_data['name'])).scalar()
        assert user_from_name.name == new_user_data['name']

def test_login_cookie_appears_after_signup(client, new_user_data):
    """ Tests to make sure the log-in session cookie appears """
    res = client.post("/auth/signup", data=new_user_data)

    assert res.status_code == 302 # Tests redirect after signin NOTE: Add destination 
    assert client.get_cookie("session") is not None # Make sure session cookie is received

def test_failure_upon_using_known_username(client, new_user_data):
    """ Tests a failure to sign up if an already sued username is tried """
    client.post("/auth/signup", data=new_user_data)
    res = client.post("/auth/signup", data=new_user_data)

    assert res.status_code == 409 # Check it reports a conflict

def test_error_page_redirect_upon_missing_values(client, new_user_data):
    """ Makes sure the user gets sent a code 400 if there are missing values NOTE: Update later when flash messages are available """
    del new_user_data["username"]
    res = client.post("/auth/signup", data=new_user_data)
    assert res.status_code == 400 # Check failure on missing username

    new_user_data["username"] = new_user_data["name"]
    del new_user_data["hashpasswd"]
    res = client.post("/auth/signup", data=new_user_data)
    assert res.status_code == 400 # Check failure on missing password

def test_get_signup_page(client):
    """ Test that a get request to the signup route will serve the signup page (Looks at title) """
    res = client.get("/auth/signup")
    assert b"<title>Sign Up</title>" in res.data