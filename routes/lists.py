from flask import Blueprint, render_template, request
from models import *
from db import db

list_route = Blueprint("lists", __name__)

@list_route.route("/<int:id>")
def get_list(id):
    """ Renders the todo list template for the list given via ID """
    session = db.session
    current_list = session.execute(db.select(List).where(List.id == id)).scalar()

    if current_list is None: # check if the list exists and return a 404 error if it does not
        return f"<h1>404</h1><br><h2>List {id} not found</h2>", 404
    
    return render_template("todolist.html", list=current_list)
