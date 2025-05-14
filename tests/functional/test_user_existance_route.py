import pytest
from app import app
import uuid
from db import db
from models import User

@pytest.fixture
def client():
    """ Testing client for functions regarding completion """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_route_with_non_existant_user(client):
    """ Tries the route with a user known to not exist """
    nonexistant_username = str(uuid.uuid4())
    res = client.get(f"/auth/exists/{nonexistant_username}")
    assert res.status_code == 404
    assert res.data == b"" # Assure only a blank string gets sent back

def test_route_with_user_known_to_exist(client):
    """ Tries the route with a user known to exist """
    username = str(uuid.uuid4())
    with app.app_context():
        new_user = User(username=username, name=username, password=username, salt=username)
        db.session.add(new_user)
        db.session.commit()

    res = client.get(f"/auth/exists/{username}")
    assert res.status_code == 200 # 200 success
    assert res.data == b"" # Assure only a blank string gets sent back
    
    # Delete the new user to try and cut down on database testing mess
    with app.app_context():
        db.session.delete(new_user)
        db.session.commit()
    