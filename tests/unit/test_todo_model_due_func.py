import pytest
from models import *
from datetime import datetime, timedelta


# Future Tests
def test_todo_model_date_in_days_to():
    """ Checks to see if the todo model """
    three_days_from_now = datetime.now()+timedelta(days=3, minutes=10)
    todo = Todo(deadline=three_days_from_now)
    assert todo.due() == "3 Days"

def test_todo_model_date_in_1_day_to():
    """ Makes sure the todo model's due function does not show and S if it is 1 day away"""
    one_day_from_now = datetime.now()+timedelta(days=1, minutes=10)
    todo = Todo(deadline=one_day_from_now)
    assert todo.due() == "1 Day"

def test_todo_model_does_not_show_days_if_under_24_hours():
    """ Tests to see if the due function shows the time in hours and minutes if under 24 hours """
    twenty_three_hours_from_now = datetime.now()+timedelta(hours=23)
    todo = Todo(deadline=twenty_three_hours_from_now)
    assert "Day" not in todo.due() 

def test_todo_model_shows_no_hours_if_under_1_hour():
    """ Makes sure the due function of the Todo model does not return hours if less than 1 hour """
    fifty_nine_minutes_from_now = datetime.now()+timedelta(minutes=59)
    todo = Todo(deadline=fifty_nine_minutes_from_now)
    assert "Day" not in todo.due() # Tests that days does not show
    assert "Hour" not in todo.due() # Tests that hours do not show if there are none

def test_todo_model_shows_no_s_if_hour_is_singular():
    """ Tests to make sure that the hour field does not have an s if there is only 1 minute"""
    one_hour_from_now = datetime.now()+timedelta(hours=1, minutes=1)
    todo = Todo(deadline=one_hour_from_now)
    assert "1 Hour" in todo.due() # Tests hour shows 1 Hour
    assert "Hours" not in todo.due() # Tests that hour shows singular

def test_todo_model_shows_no_s_if_minute_is_singular():
    """ Tests to make sure that the minute field does not have an s if there is only 1 minute"""
    some_hours_1_minute_from_now = datetime.now()+timedelta(hours=2, minutes=1, seconds=1) # incldue seconds otherwise test fall behind
    todo = Todo(deadline=some_hours_1_minute_from_now)
    assert "1 Minute" in todo.due() # Tests minute shows 1 Minute
    assert "Minutes" not in todo.due() # Tests that minute shows singular

# Tests for the past tense
def test_todo_model_adds_ago_if_overdue():
    """ Makes sure that any variant of todo adds ago at the end of the sentence if it is overdue"""
    three_days_ago = datetime.now()-timedelta(days=5, hours=2)
    todo = Todo(deadline = three_days_ago)
    assert "Ago" in todo.due() # Tests ago is there and in upper case

def test_todo_model_uses_days_if_overdue():
    """ Test to make sure the rendering stays consistant for days of overdue"""
    three_days_ago = datetime.now()-timedelta(days=5, hours=2)
    todo = Todo(deadline = three_days_ago)
    assert "5 Days" in todo.due() # Tests that it shows 5 days
