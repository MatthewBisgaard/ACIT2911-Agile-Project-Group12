from db import db
import sys

#Make the table
def create():
    db.create_all()
    
#Remove table
def drop():
    db.drop_all()


#Start session code
if __name__ == "__main__":
        if 'start' in sys.argv:
            drop()
            create()