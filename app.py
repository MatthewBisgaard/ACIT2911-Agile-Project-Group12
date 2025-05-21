from pathlib import Path
from flask import Flask, render_template
from db import db
from routes import list_route, reminders_route

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reminders.db"
app.instance_path = Path(".").resolve()
db.init_app(app)

app.register_blueprint(list_route, url_prefix="/lists")
app.register_blueprint(reminders_route, url_prefix="/reminders")

@app.route("/")
def root_page():
    """ Function used for the homepage of the application """
    return render_template("homepage.html")

if __name__=="__main__":
    app.run(debug=True, port=3000)