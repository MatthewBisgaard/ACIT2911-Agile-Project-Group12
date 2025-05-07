from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from db import db
from datetime import datetime as dt

edit = Blueprint("edit", __name__)

@edit.route("/edit/<int:id>", method=["GET"])
def edit_item(id):
    session = db.session
    current_item = session.execute(db.select(Todo).where(Todo.id == id)).scalar()
    if current_item is None: # check if the item exists and return a 404 error if it does not
        return render_template("error.html", message=f"Item does not exist", code = 404), 404
    
    return render_template("add-item-form.html", list=current_list)