from flask import url_for
import pytest
from app import app
import uuid
from db import db
from models import *
import datetime as dt

@pytest.fixture
def client():
    """ Testing client for functions regarding completion """
    app.config["TESTING"] = True
    with app.test_client() as client:
        client.post("/auth/login", data={"username":"tom", "hashpasswd": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"})
        yield client

def add_test_list(client):
    """
    Test utility function:\n
    Adds a test todo via the item and returns uuid coresponding to the title of the test todo
    """
    unique_name = str(uuid.uuid4())
    res = client.post("/lists/create_list/completion", data={
        "list-name": unique_name 
    })
    return unique_name

def fetch_list_by_uuid(uuid_string):
    """
    Test Utility function:\n
    Grabs a todo item directly from db by its title (a UUID for tests writted by Matthew)
    """
    with app.app_context():
        remlist = db.session.execute(db.select(List).where(List.name == uuid_string)).scalar()
    return remlist

# Test for 404s
def test_all_list_will_return_404(client):
    """ Tests to make sure a list that does not exist returns a 404 error """
    list_name = add_test_list(client)
    list_id = fetch_list_by_uuid(list_name).id
    with app.app_context():
        remlist = db.session.execute(db.select(List).where(List.id == list_id)).scalar()
        db.session.delete(remlist)
        db.session.commit()

    res = client.get(f"/lists/{list_id}")
    assert res.status_code == 404 # Test you cannot get a list which doe snot exist

    res = client.get(f"/lists/{list_id}/add")
    assert res.status_code == 404 # SHould have a 404 for gettng the add item form for a list that does not exist

    res = client.post(f"/lists/{list_id}/add")
    assert res.status_code == 404 # 404 for adding an item to a list that does not exist 

    res = client.get(f"/lists/rename_list/{list_id}")
    assert res.status_code == 404 # 404 for getting the rename form for a list that does not exist

    res = client.post(f"/lists/rename_list/{list_id}/completion")
    assert res.status_code == 404 # 404 for submitting the rename form for a list that does not exist

    res = client.get(f"/lists/delete_list/{list_id}")
    assert res.status_code == 404 # 404 for getting the delete form for a list that does not exist

    res = client.post(f"/lists/delete_list/{list_id}/completion")
    assert res.status_code == 404 # 404 for submitting the delete form for a list that does not exist

    res = client.get(f"/lists/{list_id}/delete-complete")
    assert res.status_code == 404 # Check that a 404 is given when deleting all on a list that does not exist. Only one check needed due to the logic order in the function
    