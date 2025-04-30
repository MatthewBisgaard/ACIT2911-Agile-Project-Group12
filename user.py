from db import db

class User(db.Model):
    id = db.mapped_column(db.Integer,primary_key = True)
    name = db.mapped_column(db.String)

