from app import app
from db import db
from models import *
from datetime import datetime, timedelta
import sys

#Make the table
def create():
    db.create_all()
    
#Remove table
def drop():
    db.drop_all()

def dummy_data():
    """ A function that inserts some dummy data into the application db for testing"""
    session = db.session
    user = User(name="Tom", password="1234", username="tom", salt="ab26e0")
    main_list = List(name="Reminders", user=user)
    reminder1 = Todo(title="Buy coffee", deadline=(datetime.now()+timedelta(days=3)), description="Something medium with notes of apricot", rem_list=main_list)
    reminder2 = Todo(title="Feed sourdough starter", deadline=(datetime.now()+timedelta(hours=3)), description="BREAD!", rem_list=main_list)
    reminder3 = Todo(title="Change engine oil", deadline=(datetime.now()+timedelta(minutes=30)), description="Please don't forget, it is a toyota but still", rem_list=main_list)
    session.add(user)
    session.add(main_list)
    session.add(reminder1)
    session.add(reminder2)
    session.add(reminder3)
    session.commit()
    print("dummy data created")


#Start session code
if __name__ == "__main__":
    with app.app_context():
        if len(sys.argv) > 0:
            for arg in sys.argv:
                match arg:
                    case "create":
                        create()
                    case "drop":
                        drop()
                    case "start":
                        drop()
                        create()
                    case "dummy":
                        dummy_data()
        else:
            # Else for the if statment checking sys.argv length
            print("Please inlude 1 or more arguments")
        