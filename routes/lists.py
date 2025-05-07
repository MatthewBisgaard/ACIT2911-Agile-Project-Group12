from flask import Blueprint, render_template, request, redirect, url_for
from helpers.date_utils import auto_date_parse
from models import *
from db import db
from datetime import datetime as dt

list_route = Blueprint("lists", __name__)

@list_route.route("/<int:id>")
def get_list(id):
    """ Renders the todo list template for the list given via ID """
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()

    if current_list is None: # check if the list exists and return a 404 error if it does not
        return f"<h1>404</h1><br><h2>List {id} not found</h2>", 404
    
    return render_template("todolist.html", list=current_list)

@list_route.route("/<int:id>/add", methods=["GET"])
def get_add_item_form(id):
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()
    if current_list is None: # check if the list exists and return a 404 error if it does not
        return f"<h1>404</h1><br><h2>List {id} not found</h2>", 404
    
    return render_template("add-item-form.html", list=current_list)


@list_route.route("/<int:id>/add", methods=["POST"])
def add_reminder_to_list(id):
    """ Adds a reminder from the add-item-form to the list """
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()
    if current_list is None: # check if the list exists and return a 404 error if it does not
        return f"<h1>404</h1><br><h2>List {id} not found</h2>", 404
    

    form = request.form
    new_reminder = Todo(
        title = form["item-name"],
        description = form["description"],
        deadline = auto_date_parse(form["deadline"]),
        rem_list = current_list
    )
    session.add(new_reminder)
    session.commit()
    return redirect(url_for("lists.get_list", id=id))