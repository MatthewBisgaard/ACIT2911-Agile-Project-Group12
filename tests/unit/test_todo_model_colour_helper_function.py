from models import Todo
from datetime import datetime, timedelta
import pytest

@pytest.fixture
def now():
    """ Returns datetime.now() """
    return datetime.now()

def test_already_complete(now):
    """ Tests that the colour helper function returns an empty string if already complete """
    todo = Todo(deadline = (now + timedelta(days=5)), complete = True)
    # Test no colour if many days away
    assert todo.colour_helper() == ""

    # Test no colour if 1 day away
    todo.deadline = now + timedelta(days=1, hours=1)
    assert todo.colour_helper() == ""

    # Test no colour if within 24 hours
    todo.deadline = now +timedelta(hours=23)
    assert todo.colour_helper() == ""

    # Test no colour even if overdue
    todo.deadline = now - timedelta(hours=3)
    assert todo.colour_helper() == ""

    # Redo with freedom spelling 
    # Test no colour if many days away
    todo.deadline = now + timedelta(days=5)
    assert todo.color_helper() == ""

    # Test no colour if 1 day away
    todo.deadline = now + timedelta(days=1, hours=1)
    assert todo.color_helper() == ""

    # Test no colour if within 24 hours
    todo.deadline = now +timedelta(hours=23)
    assert todo.color_helper() == ""

    # Test no colour even if overdue
    todo.deadline = now - timedelta(hours=3)
    assert todo.color_helper() == ""

def test_1_day_away_aka_tomorrow(now):
    """ tests that the correct class string gets returned when due tomorrow """
    todo = Todo(deadline = (now + timedelta(days=1, hours=2)))
    assert todo.colour_helper() == "dueTomorrow"

    # Retest with American spelling
    assert todo.color_helper() == "dueTomorrow"

def test_within_24_hours(now):
    """ Tests for the return of the correct class string when due today (within 24 hours)"""
    todo = Todo(deadline = (now + timedelta(hours=5)))
    assert todo.colour_helper() == "dueToday"

    # Re-test with American spelling
    assert todo.color_helper() == "dueToday"

def test_overdue(now):
    """ Test for returning overDue when the reminder is overdue"""
    todo = Todo(deadline = (now - timedelta(hours=2)))
    assert todo.colour_helper() == "overDue"

    # Re-test with American spelling
    assert todo.color_helper() == "overDue"

