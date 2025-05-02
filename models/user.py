from db import db

class User(db.Model):
    id = db.mapped_column(db.Integer,primary_key = True)
    name = db.mapped_column(db.String)
    lists = db.relationship('List', back_populates='user')
    password = db.mapped_column(db.Integer,nullable=False)
    username= db.mapped_column(db.String,nullable=False)
    salt = db.mapped_column(db.String)