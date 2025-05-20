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

def add_test_todo(client):
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

def fetch_item_by_uuid(uuid_string):
    """
    Test Utility function:\n
    Grabs a todo item directly from db by its title (a UUID for tests writted by Matthew)
    """
    with app.app_context():
        todo = db.session.execute(db.select(Todo).where(Todo.title == uuid_string)).scalar()
    return todo

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
