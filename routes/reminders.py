from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from db import db
from datetime import datetime as dt

reminders_route = Blueprint("reminders", __name__)

@reminders_route.route("/complete/<int:id>", methods=["POST", "PUT"])
def mark_reminder_completed_route(id):
    """
    Marks the reminder with the given ID as completed and updating the completion date.\n
    Takes both POST and PUT Requests
    """
    reminder = db.session.execute(db.select(Todo).where(Todo.id == id)).scalar()
    if reminder is None: # test that the reminder exists
        return "Error 404: Reminder could not be found", 404
    
    if reminder.complete: # check reminder not already complete
        return "Error 409: Reminder already completed", 409
    
    # Set reminder complete
    reminder.complete = True
    reminder.completed_on = dt.now()

    # Update status in the db
    db.session.add(reminder)
    db.session.commit()

    return redirect(url_for("lists.get_list", id=reminder.rem_list.id))

@reminders_route.route("/de-complete/<int:id>", methods=["POST", "PUT"])
def mark_reminder_incomplete_route(id):
    """
    Marks an already completed reminder as incomplete again.\n
    This removes the completion date
    """
    reminder = db.session.execute(db.select(Todo).where(Todo.id == id)).scalar()
    if reminder is None: # test that the reminder exists
        return "Error 404: Reminder could not be found", 404
    
    if not reminder.complete: # check reminder already complete
        return "Error 409: Reminder not currently completed", 409
    
    reminder.complete = False
    reminder.completed_on = None

    # Update status in the db
    db.session.add(reminder)
    db.session.commit()

    return redirect(url_for("lists.get_list", id=reminder.rem_list.id))
