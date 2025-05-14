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


def test_creating_todo_item(client):
    """Test that a todo item can be created via Flask"""
    unique_name = str(uuid.uuid4())
    res = client.post("/lists/1/add", data={
        "item-name": unique_name, 
        "description": unique_name, 
        "deadline":"2029-03-09T11:32"
    })
    assert res.status_code == 302 # redirect to the list works
    with app.app_context():
        todo = db.session.execute(db.select(Todo).where(Todo.title == unique_name)).scalar()
    assert todo is not None # Make sure reminder was created

def test_newly_created_is_incomplete(client):
    """ 
    Check that a newly created reminder will be Incomplete\n
    TODO: Check the html page once it shows completion
    """
    todo = fetch_item_by_uuid(add_test_todo(client))
    assert not todo.complete # Make sure the new todo is not completed


def test_completion_and_decompletion_bool(client):
    """
    Tests if the route for completing todo items actually works
    """
    title = add_test_todo(client)
    todo = fetch_item_by_uuid(title)

    # Test Completeion boolean status
    res = client.post(f"/reminders/complete/{todo.id}")
    todo = fetch_item_by_uuid(title) # get todo again now that it has been updated
    assert todo.complete # Verify todo is complete after calling the route

    # Test Decomplete boolean status
    res = client.post(f"/reminders/de-complete/{todo.id}")
    todo = fetch_item_by_uuid(title) # get todo again now that it has been updated
    assert not todo.complete # Make sure the change applied

def test_completion_and_decompletion_date_changes(client):
    """
    Tests the completion date fucntion of completing a route 
    """
    title = add_test_todo(client)
    todo = fetch_item_by_uuid(title)

    # Test compeltion time setting
    res = client.post(f"/reminders/complete/{todo.id}")
    now = dt.datetime.now()
    plus_minus_1_second = dt.timedelta(seconds=1)
    todo = fetch_item_by_uuid(title) # get todo again now that it has been updated
    assert (now-plus_minus_1_second) < todo.completed_on and todo.completed_on < (now+plus_minus_1_second) # assert that the date of completion si relatively cose to when the request was made

    # Test de-completion time removal
    res = client.post(f"/reminders/de-complete/{todo.id}")
    todo = fetch_item_by_uuid(title) # get todo again now that it has been updated
    assert todo.completed_on is None # Make sure the change applied

def test_error_de_completing_incomplete(client):
    """
    Makes sure code 409 is returned when try to de-complete an incomplete task
    """
    title = add_test_todo(client)
    todo = fetch_item_by_uuid(title)

    # Test Completeion boolean status
    res = client.post(f"/reminders/de-complete/{todo.id}")
    assert res.status_code == 409 # Check that you get an failure code de-completing an incomplete reminder 

def test_error_for_completing_a_compelte_reminder(client):
    """
    Makes sure that code 409 is returned when attempting to mark a complete reminder as complete again
    """
    title = add_test_todo(client)
    todo = fetch_item_by_uuid(title)
    client.post(f"/reminders/complete/{todo.id}")
    res = client.post(f"/reminders/complete/{todo.id}")
    assert res.status_code == 409 # Check you cannot doubel complete

def test_delete_route_for_reminder(client):
    """ Makes sure the delete route removes a reminder from the database """
    title = add_test_todo(client)
    todo = fetch_item_by_uuid(title)

    res = client.get(f"/reminders/remove/{todo.id}")
    assert res.status_code == 302 # test that client is redirected back to the list
    res = client.get(f"/lists/1") # NOTE: Issue may arise if tests switch to a different list
    assert title.encode() not in res.data # Test that the UUID is nolonger on the reminder page
    assert fetch_item_by_uuid(title) is None # Tests the delete route removes it from the db

def test_delete_route_returns_404_if_not_found(client):
    """ Makes sure the delete route will return a 404 status code if attempting to delete a reminder which does not exist\n
     This is acheived by creating then deleting a reminder then attempting to delete it again """
    title = add_test_todo(client)
    todo = fetch_item_by_uuid(title)

    client.get(f"/reminders/remove/{todo.id}")
    res = client.get(f"/reminders/remove/{todo.id}")
    assert res.status_code == 404