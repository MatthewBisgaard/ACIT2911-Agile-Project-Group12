from flask import Blueprint, flash, render_template, request, redirect, url_for
from models import *
from db import db
from flask_login import login_required, logout_user, login_user
import hashlib
import secrets

auth_route = Blueprint("auth", __name__)

@auth_route.route("/login", methods=["GET", "POST"])
def login():
    """ Logs in a user OR serves the login page if GET """
    if request.method == "GET": # Check if get then return the login page
        return render_template("login.html")
    
    # Get the username and password from the request
    username = request.form.get("username", None)
    password = request.form.get("hashpasswd", None)
    remember = True if "remember" in request.form else False
    
    # Check to see if username or password are blank. These flash rather than send to error
    if username is None or username == "":
        flash("Username cannot be blank")
        return redirect(url_for("auth.login"))

    if password is None or password == "":
        flash("Password cannot be blank")
        return redirect(url_for("auth.login"))
    
    # Strip Username and password
    username = username.strip()
    password = password.strip()

    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if user is None: # Redirect if user is not found
        flash("Username or password may be correct")
        return redirect(url_for("auth.login"))
    
    # Check if password matches 
    hash = hashlib.sha256(password.encode())
    hash.update(user.salt.encode())
    if user.password == hash.hexdigest():
        login_user(user, remember=remember)
        
        # Check if there is a next argument and save the value
        redirect_url = request.args.get("next", None)

        if redirect_url is None:
            return redirect(url_for('dashboard'))
        else:
            return redirect(redirect_url)
    
    flash("Username or password may be correct")
    return redirect(url_for("auth.login"))

@auth_route.route("/signup", methods=["GET", "POST"])
def signup():
    """ Handles the signup process for a new user """
    if request.method == "GET":
        return render_template("signup.html")
    
    # Get the username, password and name from the request
    username = request.form.get("username", None)
    password = request.form.get("hashpasswd", None)
    name = request.form.get("name", username)

    # Check if username or password values are empty. The name will default to username if left blank
    if username is None:
        return render_template("error.html", code=400, message="Username field cannot be left blank"), 400
    
    if password is None:
        return render_template("error.html", code=400, message="Password field cannot be left blank"), 400
    
    # Strip values of trailing spaces
    username = username.strip()
    password = password.strip()
    name = name.strip()

    # Check that the username is not in use
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if user is not None:
        flash("That username already exists")
        return redirect(url_for("auth.signup")), 409
    
    # Generate a salt for the new user
    new_salt = secrets.token_hex(32)
    hash = hashlib.sha256(password.encode())
    hash.update(new_salt.encode())
    password = hash.hexdigest()
    
    # Create the new user and add them to the database
    new_user = User(username=username, name=name, password=password, salt=new_salt)
    db.session.add(new_user)
    db.session.commit()
    
    # Login the user and send them to their homepage
    login_user(new_user)
    return redirect(url_for("dashboard")) # NOTE: Needs to be changed


@auth_route.route("/exists/<string:username>", methods=["GET"])
def get_user_exists(username):
    """ Returns a code to determine if a username exists """
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    if user is None:
        return "", 404
    
    # Send the result back
    return "", 200

@auth_route.route("/logout")
@login_required
def logout():
    """ This route when acceced by a logged in user will sign them out of the application """
    logout_user()
    return redirect("/")