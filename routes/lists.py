from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from helpers.date_utils import auto_date_parse
from models import *
from db import db
from datetime import datetime as dt
from flask_login import current_user, login_required

list_route = Blueprint("lists", __name__)

@list_route.route("/<int:id>")
@login_required
def get_list(id):
    """ Renders the todo list template for the list given via ID """
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()

    if current_list is None: # check if the list exists and return a 404 error if it does not
        return f"<h1>404</h1><br><h2>List {id} not found</h2>", 404
    
    user = current_user
    if user.is_anonymous or current_list.user.id != user.id:
        return render_template("error.html", message="Forbidden", code=403), 403    

    # Logic for order by and show hidden
    select_query = db.select(Todo).where(Todo.list_id == current_list.id)
    match request.args.get("show", None):
        case "true":
            pass
        case _:
            select_query = select_query.where(Todo.complete == False)

    match request.args.get("order", None):
        case "created":
            select_query = select_query.order_by(Todo.created_on.desc())
        case "title":
            select_query = select_query.order_by(Todo.title.asc())
        case "deadline":
            select_query = select_query.order_by(Todo.deadline.asc())

    reminders = db.session.execute(select_query).scalars()

    return render_template("todolist.html", list=current_list, user=user, reminders=reminders)

@list_route.route("/<int:id>/add", methods=["GET"])
@login_required
def get_add_item_form(id):
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()
    if current_list is None: # check if the list exists and return a 404 error if it does not
        return f"<h1>404</h1><br><h2>List {id} not found</h2>", 404
    
    user = current_user
    if user.is_anonymous or current_list.user.id != user.id:
        return render_template("error.html", message="Forbidden", code=403), 403    
    
    return render_template("add-item-form.html", list=current_list)


@list_route.route("/<int:id>/add", methods=["POST"])
@login_required
def add_reminder_to_list(id):
    """ Adds a reminder from the add-item-form to the list """
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()
    if current_list is None: # check if the list exists and return a 404 error if it does not
        return f"<h1>404</h1><br><h2>List {id} not found</h2>", 404
    
    user = current_user
    if user.is_anonymous or current_list.user.id != user.id:
        return render_template("error.html", message="Forbidden", code=403), 403 
    

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

@list_route.route("/create_list", methods=["GET"])
@login_required
def creation_page():
    """ Serves the list creation page """
    return render_template("create-list.html", user=current_user.id)

@list_route.route("/create_list/completion", methods=["POST"])
@login_required
def list_created():
    """Creating the list with info user provided"""
    session = db.session
    form = request.form
    new_list = List(name=form["list-name"], user=session.execute(db.select(User).where(User.id == current_user.id)).scalar())
    session.add(new_list)
    session.commit()
    return redirect(url_for("lists.get_list", id=new_list.id))

@list_route.route("/rename_list/<int:id>", methods=["GET"])
@login_required
def list_rename_page(id):
    """Sends the HTML Rename page to the user"""
    session = db.session
    list = session.execute(db.select(List).where(List.id == id)).scalar()
    user = current_user
    if user.is_anonymous or list.user.id != user.id:
        return render_template("error.html", message="Forbidden", code=403), 403 

    return render_template("rename-list.html", list=list)

@list_route.route("/rename_list/<int:id>/completion", methods=["POST"])
@login_required
def list_rename_done(id):
    """Completing the rename list"""
    session = db.session
    form = request.form
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()

    user = current_user
    if user.is_anonymous or current_list.user.id != user.id:
        return render_template("error.html", message="Forbidden", code=403), 403 

    current_list.name = form["new-list-name"]
    session.add(current_list)
    session.commit()
    return redirect(url_for("lists.get_list", id=current_list.id))

@list_route.route("/delete_list/<int:id>", methods=["GET"])
@login_required
def list_delete_page(id):
    """ This will get the delete confirmaation page for the user"""
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()

    user = current_user
    if user.is_anonymous or current_list.user.id != user.id:
        return render_template("error.html", message="Forbidden", code=403), 403 

    return render_template("delete-list.html", list=current_list)

@list_route.route("/delete_list/<int:id>/completion", methods=["POST"])
@login_required
def list_delete_done(id):
    """ This will get the delete confirmaation page for the user"""
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()
    
    if current_list is None: # check if the list exists and return a 404 error if it does not
        return render_template("error.html", message=f"List does not exist", code = 404), 404
    
    # Check ownership
    user = current_user
    if current_user.is_anonymous or current_list.user.id != current_user.id:
        return render_template("error.html", message="Forbidden", code=403), 403

    db.session.delete(current_list)
    db.session.commit()    
    
    return redirect(url_for("dashboard"))

@list_route.route("/<int:id>/delete-complete", methods = ["GET", "POST"])
@login_required
def delete_complete(id):
    """ Deletes all completed reminders in a given list  """
    current_list = db.session.execute(db.select(List).where(List.id == id)).scalar()
    if current_list is None: # check if the list exists and return a 404 error if it does not
        return render_template("error.html", code=404, message="Could not find that list"), 404
    
    # Auth Check
    user = current_user
    if current_user.is_anonymous or current_list.user.id != current_user.id:
        return render_template("error.html", message="Forbidden", code=403), 403
    
    if request.method == "GET":
        return render_template("post-confirm-dialogue.html", question=f'Delete all completed reminders on "{current_list.name}"', confirm_text="Delete", cancel_text="Cancel", action=url_for("lists.delete_complete", id=id, **request.args))
    
    result = request.form.get("result", None)
    if result == "confirm":
        for todo in current_list.todos:
            if todo.complete:
                db.session.delete(todo)
        db.session.commit()

    return redirect(url_for('lists.get_list', id = current_list.id, **request.args))


