from pathlib import Path
from flask import Flask, render_template, request
from db import db
from routes import list_route, reminders_route, auth_route
from flask_login import LoginManager
import secrets
from models import User

app = Flask(__name__)
app.secret_key = secrets.token_hex().encode()

# Authentication setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "It appears you are not signed in. Please sign in here."

@login_manager.user_loader
def user_loader(user_id):
    """ Acts as the handler for user requests for flask_login\n
returns a User object from the id which is a string """
    return db.session.execute(db.select(User).where(User.id == int(user_id))).scalar()


# Flask_SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reminders.db"
app.instance_path = Path(".").resolve()
db.init_app(app)

# Blueprint registration
app.register_blueprint(list_route, url_prefix="/lists")
app.register_blueprint(reminders_route, url_prefix="/reminders")
app.register_blueprint(auth_route, url_prefix="/auth")

@app.route("/")
def root_page():
    """ Function used for the homepage of the application """
    return "Flask is operational"

if __name__=="__main__":
    app.run(debug=True, port=3000)