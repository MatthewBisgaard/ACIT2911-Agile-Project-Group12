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

def creating_list(client):
    """Test to make sure list is being created"""
    title = 