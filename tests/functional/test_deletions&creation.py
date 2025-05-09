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
        yield client

def add_test_todo(client):
    """
    Test utility function:\n
    Adds a test todo via the item and returns uuid coresponding to the title of the test todo
    """
    unique_name = str(uuid.uuid4())
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


def test_delete_route_when_todo_completed(client):
    """This test to make sure that the item gets deleted when completed"""
    title = add_test_todo(client)
    todo = fetch_item_by_uuid(title)

    client.post(f"/reminders/complete/{todo.id}")
    res = client.get(f"/reminders/remove/{todo.id}")
    assert res.status_code == 302

def test_create_reminder_appear_on_webpage(client):

    title = add_test_todo(client)
    todo = fetch_item_by_uuid(title)
    
    res= client.get(f"/reminders/edit/1")

    assert res.status_code == 200

