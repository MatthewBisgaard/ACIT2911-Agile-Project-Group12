from db import db

class List(db.Model):
    __tablename__ = "list"
    
    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String, nullable=False)
    
    # Link to User
    user_id = db.mapped_column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="lists")
    
    # Link to Todo items
    todos = db.relationship("Todo", back_populates="rem_list")