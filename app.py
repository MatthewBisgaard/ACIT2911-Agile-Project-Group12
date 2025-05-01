from pathlib import Path
from flask import Flask, render_template
from db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reminders.db"
app.instance_path = Path(".").resolve()
db.init_app(app)

@app.route("/")
def root_page():
    """ Function used for the homepage of the application """
    return "Flask is operational"

if __name__=="__main__":
    app.run(debug=True, port=3000)