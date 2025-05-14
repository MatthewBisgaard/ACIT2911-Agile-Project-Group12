from db import db
import datetime as dt

class Todo(db.Model):
    """ Model that represents a reminder item in the database """
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
        # Return an empty string if the reminder is dateless
        if self.deadline is None:
            return ""
        
        # Find the current dattime and retreive the difference between the reminder and now
        now = dt.datetime.now()
        diff = self.deadline - now

        past_tense_string = "" # This string is appended to the final date string to define if it is past tense or present
        # Check to see if the date is in the future or in the past and make some adjustments to the math 
        if self.deadline <= now: 
            past_tense_string = " Ago" # Set the past tense string to ago if it it overdue
            diff = now - self.deadline # Change the difference so the logic below still wokrs

        # Look at the number of days difference. If there is 1 day or more then show the time unil due in days
        days = diff.days
        if days > 0:
            return f"{days} Day{("" if days == 1 else "s")}{past_tense_string}"
        
        # This logic looks at the hours and minutes and reports back
        total_seconds = diff.seconds
        minutes = total_seconds // 60
        hours = minutes // 60
        minutes = minutes - (hours * 60)
        # The hour string is only populated if there is more than 1 hour from due. Also it only adds an s if there is more than 1 hour
        hour_string = "" if hours<1 else (f"{hours} Hour"+("" if hours == 1 else "s") + " ")
        # The minute string will report the minutes minus the hours until due. Minutes is made plural only if there is a non-1 minute.
        minute_string = f"{minutes} Minute"+ ("" if minutes == 1 else "s")
        return f"{hour_string}{minute_string}{past_tense_string}"
            
            



            
            


            
            
            
