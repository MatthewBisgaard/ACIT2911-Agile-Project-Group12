from db import db
import datetime as dt

class Todo(db.Model):
    __tablename__ = "todo"

    id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String, nullable=False, default="")
    deadline = db.mapped_column(db.DateTime, nullable=True)
    complete = db.mapped_column(db.Boolean, nullable=False, default=False)
    completed_on = db.mapped_column(db.DateTime, nullable=True, default=None)
    created_on = db.mapped_column(db.DateTime, nullable=False, default=db.func.now())
    description = db.mapped_column(db.String, nullable=False, default="")

    rem_list = db.relationship("List", back_populates="todos")
    list_id = db.mapped_column(db.Integer, db.ForeignKey("list.id"))

    def due(self):
        """ Returns a string that represents the time until the reminder is due. Will adjust dynamically based on whether there are days left or hours """
        if self.deadline is None:
            return ""
        
        now = dt.datetime.now()
        
        diff = self.deadline - now
        days = diff.days
        if days>0:
            return f"{days} Day"+("" if days == 1 else "s")
    
        total_seconds = diff.seconds
        minutes = total_seconds // 60
        hours = minutes // 60
        minutes = minutes - (hours * 60)
        hour_string = "" if hours<1 else (f"{hours}"+("" if hours == 1 else "s") + " ")
        minute_string = f"{minutes} Minute"+ ("" if minutes == 1 else "s")
        return f"{hour_string}{minute_string}"
            



            
            


            
            
            
