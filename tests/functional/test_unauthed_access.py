from flask import url_for
import pytest
from app import app
import uuid
from db import db
from models import *
import datetime as dt
from hashlib import sha256

# NOTE: THis test file expects the dummy database to exist

@pytest.fixture
def client():
    """ Testing client for functions regarding completion """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def new_signin(client):
    new_user_name = str(uuid.uuid4())
    new_user_data = {
        "username": new_user_name,
        "name": new_user_name+"name",
        "hashpasswd": "1234"
    }
    hash = sha256(new_user_data["hashpasswd"].encode())
    hash.update(b"LayAllYourLoveOnMe")

    with app.app_context():
        new_user = User(name=new_user_data["name"], username=new_user_data["username"], password=hash.hexdigest(), salt="LayAllYourLoveOnMe")
        db.session.add(new_user)
        db.session.commit()

    client.post("/auth/login", data={
        "username": new_user_data["username"],
        "hashpasswd": new_user_data["hashpasswd"]
    })

@pytest.fixture
def client_authed():
    """ Testing client for functions regarding completion """
    app.config["TESTING"] = True
    with app.test_client() as client:
        new_signin(client)
        yield client


# Test unauthenticated use of routes

def test_unauthenticated_delete_reminders(client):
    """Checks to see if a code 401 is sent when deleting a reminder when not signed in """
    res = client.get("/reminders/remove/1")
    assert res.status_code == 401 # No permission to use route

def test_unauthenticated_mark_complete_incomplete(client):
    """ Tests to make sure a code 401 is returned when trying to mark a reminder as complete/incomplete when not signed in """
    res = client.post(f"/reminders/complete/1")
    assert res.status_code == 401 # Reminder not able to be completed

    res = client.post(f"/reminders/de-complete/1")
    assert res.status_code == 401 # Reminder not able to be decompleted

def test_unauthenticated_edit_get_and_post(client):
    """ Test that an unauthenticated in user can neither get the edit page or complete a reminder edit """
    res = client.get("/reminders/edit/1")
    assert res.status_code == 401 # No permission to edit that item

    res = client.post("/reminders/edit/1/completion", data={
        "item-name": "The Great Gig In The Sky",
        "description": "Immigrant Song",
        "deadline": "1977-02-22T00:01"
    })
    assert res.status_code == 401 # No permission to post

# Test unauthorized use of routes

def test_unauthorized_delete_reminders(client_authed):
    """Checks to see if a code 403 is sent when deleting a reminder the user does not own/is not owner of """
    res = client_authed.get("/reminders/remove/1")
    assert res.status_code == 403 # No permission to use route

def test_unauthorized_mark_complete_incomplete(client_authed):
    """ Tests to make sure a code 403 is returned when trying to mark a reminder as complete/incomplete when not owned by the current user """
    res = client_authed.post(f"/reminders/complete/1")
    assert res.status_code == 403 # Reminder not able to be completed

    res = client_authed.post(f"/reminders/de-complete/1")
    assert res.status_code == 403 # Reminder not able to be decompleted

def test_unauthorized_edit_get_and_post(client_authed):
    """ Test that an unauthorized in user can neither get the edit page or complete a reminder edit """
    res = client_authed.get("/reminders/edit/1")
    assert res.status_code == 403 # No permission to edit that item

    res = client_authed.post("/reminders/edit/1/completion", data={
        "item-name": "Electric Funeral",
        "description": "Love Me Two Times",
        "deadline": "1969-02-22T00:01"
    })
    assert res.status_code == 403 # No permission to post




