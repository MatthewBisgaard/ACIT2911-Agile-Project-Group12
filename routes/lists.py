from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
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
    
    # NOTE: TESTING ONLY
    user = session.execute(db.select(User).where(User.id == 1)).scalar()
    
    return render_template("todolist.html", list=current_list, user=user)

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

@list_route.route("/create_list/<int:id>}", methods=["GET"])
def creation_page(id):
    """ Serves the list creation page """
    return render_template("create-list.html", user=id)

@list_route.route("/create_list/<int:id>/completion", methods=["POST"])
def list_created(id):
    """Creating the list with info user provided"""
    session = db.session
    form = request.form
    new_list = List(name=form["list-name"], user=session.execute(db.select(User).where(User.id == id)).scalar())
    session.add(new_list)
    session.commit()
    return redirect(url_for("lists.get_list", id=new_list.id))

@list_route.route("/rename_list/<int:id>", methods=["GET"])
def list_rename_page(id):
    """Sends the HTML Rename page to the user"""
    session = db.session
    return render_template("rename-list.html", list=session.execute(db.select(List).where(List.id == id)).scalar())

@list_route.route("/rename_list/<int:id>/completion", methods=["POST"])
def list_rename_done(id):
    """Completing the rename list"""
    session = db.session
    form = request.form
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()
    current_list.name = form["new-list-name"]
    session.add(current_list)
    session.commit()
    return redirect(url_for("lists.get_list", id=current_list.id))

@list_route.route("/delete_list/<int:id>", methods=["GET"])
def list_delete_page(id):
    """ This will get the delete confirmaation page for the user"""
    session = db.session
    return render_template("delete-list.html", list=session.execute(db.select(List).where(List.id == id)).scalar())

@list_route.route("/delete_list/<int:id>/completion", methods=["POST"])
# @login_required
def list_delete_done(id):
    """ This will get the delete confirmaation page for the user"""
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()
    
    if current_list is None: # check if the list exists and return a 404 error if it does not
        return render_template("error.html", message=f"List does not exist", code = 404), 404
    
    # Check ownership
    # if current_user.is_anonymous or current_list.user.id != current_user.id:
    #     return render_template("error.html", message="Forbidden", code=403), 403

    db.session.delete(current_list)
    db.session.commit()    
    
    return redirect(url_for("lists.get_list", id=1))

