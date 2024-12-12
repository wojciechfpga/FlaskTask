from app import db
from app.models import Room 

def initialize_database():
    """
    Initialization of DB
    """
    db.drop_all()
    db.create_all()

    if not Room.query.first(): 
        example_room = Room(name="Sala Konferencyjna 1", capacity=10)
        db.session.add(example_room)
        db.session.commit()
