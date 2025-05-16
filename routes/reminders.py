from flask import Blueprint, render_template, request, redirect, url_for
from helpers.date_utils import auto_date_parse
from models import *
from db import db
from datetime import datetime as dt
from flask_login import login_required, current_user

reminders_route = Blueprint("reminders", __name__)

@reminders_route.route("/complete/<int:id>", methods=["POST", "PUT"])
@login_required
def mark_reminder_completed_route(id):
    """
    Marks the reminder with the given ID as completed and updating the completion date.\n
    Takes both POST and PUT Requests
    """
    reminder = db.session.execute(db.select(Todo).where(Todo.id == id)).scalar()

    if reminder is None: # test that the reminder exists
        return render_template("error.html", message=f"Reminder could not be found", code = 404), 404
    
    # Check ownership
    if current_user.is_anonymous or reminder.rem_list.user.id != current_user.id:
        return render_template("error.html", message="Forbidden", code=403), 403

    if reminder.complete: # check reminder not already complete
        return render_template("error.html", message=f"Reminder already completed", code = 409), 409

    
    # Set reminder complete
    reminder.complete = True
    reminder.completed_on = dt.now()

    # Update status in the db
    db.session.add(reminder)
    db.session.commit()

    return redirect(url_for("lists.get_list", id=reminder.rem_list.id))

@reminders_route.route("/de-complete/<int:id>", methods=["POST", "PUT"])
@login_required
def mark_reminder_incomplete_route(id):
    """
    Marks an already completed reminder as incomplete again.\n
    This removes the completion date
    """
    reminder = db.session.execute(db.select(Todo).where(Todo.id == id)).scalar()

    if reminder is None: # test that the reminder exists
        return render_template("error.html", message=f"Reminder could not be found", code = 404), 404

    # Check ownership
    if current_user.is_anonymous or reminder.rem_list.user.id != current_user.id:
        return render_template("error.html", message="Forbidden", code=403), 403
    
    if not reminder.complete: # check reminder already complete
        return render_template("error.html", message=f"Reminder not currently completed", code = 409), 409

    
    reminder.complete = False
    reminder.completed_on = None

    # Update status in the db
    db.session.add(reminder)
    db.session.commit()

    return redirect(url_for("lists.get_list", id=reminder.rem_list.id))

@reminders_route.route("/edit/<int:id>", methods=["GET"])
@login_required
def edit_item(id):
    session = db.session
    current_item = session.execute(db.select(Todo).where(Todo.id == id)).scalar()

    if current_item is None: # check if the item exists and return a 404 error if it does not
        return render_template("error.html", message=f"Item does not exist", code = 404), 404
    
    # Check ownership
    if current_user.is_anonymous or current_item.rem_list.user.id != current_user.id:
        return render_template("error.html", message="Forbidden", code=403), 403
    
    return render_template("edit-item-form.html", reminder=current_item)

@reminders_route.route("/edit/<int:id>/completion", methods=["POST"])
@login_required
def done_edit(id):
    session = db.session
    current_item = session.execute(db.select(Todo).where(Todo.id == id)).scalar()
    
    if current_item is None: # check if the item exists and return a 404 error if it does not
        return render_template("error.html", message=f"Item does not exist", code = 404), 404
    
    # Check ownership
    if current_user.is_anonymous or current_item.rem_list.user.id != current_user.id:
        return render_template("error.html", message="Forbidden", code=403), 403
    
    form = request.form
    current_item.title = form["item-name"]
    current_item.description = form["description"]
    current_item.deadline = auto_date_parse(form["deadline"])
    session.add(current_item)
    session.commit()
    return redirect(url_for("lists.get_list", id=current_item.rem_list.id))

@reminders_route.route("/remove/<int:id>", methods=["GET"])
@login_required
def rm_todo(id):
    session = db.session
    current_item = session.execute(db.select(Todo).where(Todo.id == id)).scalar()
    if current_item is None: # check if the item exists and return a 404 error if it does not
        return render_template("error.html", message=f"Item does not exist", code = 404), 404
    
    # Check ownership
    if current_user.is_anonymous or current_item.rem_list.user.id != current_user.id:
        return render_template("error.html", message="Forbidden", code=403), 403

    item_id = current_item.rem_list.id

    db.session.delete(current_item)
    db.session.commit()    
    
    return redirect(url_for("lists.get_list", id=item_id))
