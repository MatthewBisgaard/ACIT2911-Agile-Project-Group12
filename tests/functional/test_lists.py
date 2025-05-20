from flask import url_for
import pytest
from app import app
from uuid import uuid4
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

    unique_name = str(uuid4())
    res = client.post("/lists/1/add", data={
        "item-name": unique_name, 
        "description": f"{unique_name}desc", 
        "deadline":"2029-03-09T11:32"
    })
    return unique_name
  
def add_test_todo(client):
    """
    Test utility function:\n
    Adds a test todo via the item and returns uuid coresponding to the title of the test todo
    """
    unique_name = str(uuid4())
    res = client.post("/lists/1/add", data={
        "item-name": unique_name, 
        "description": unique_name, 
        "deadline":"2029-03-09T11:32"
    })
    return unique_name

def fetch_item_by_uuid(uuid_string):
    """
    Test Utility function:\n
    Grabs a todo item directly from db by its title (a UUID for tests writted by Matthew)
    """
    with app.app_context():
        todo = db.session.execute(db.select(Todo).where(Todo.title == uuid_string)).scalar()
    return todo

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
    

def test_show_hide_completed(client):
    """ Test that completed reminders are only shown when the query string indicates so """
    title = add_test_todo(client)
    with app.app_context():
        todo = db.session.execute(db.select(Todo).where(Todo.title == title)).scalar()
        todo.complete = True
        db.session.commit()

    res = client.get("/lists/1")
    assert title.encode() not in res.data # Test that it does not show by default

    res = client.get("/lists/1?show=true")
    assert title.encode() in res.data # Assert that it now shows as show is true

    res = client.get("/lists/1?show=false")
    assert title.encode() not in res.data # Assert that it nolonger shows as show is false

def test_strikethrough_when_complete(client):
    """ Test to make sure the title and description of the reminder are surrounded by strikethroughs if completed"""
    title = add_test_todo(client)
    with app.app_context():
        todo = db.session.execute(db.select(Todo).where(Todo.title == title)).scalar()
        todo.complete = True
        db.session.commit()
        strike_description = f'<s>{todo.description}</s>'
        strike_title = f'<s>{todo.title}</s>'

    res = client.get("/lists/1?show=true")
    assert strike_title.encode() in res.data # Test that the title is struck through semantically 
    assert strike_description.encode() in res.data # Test that the desctiption is struck through semantically 

