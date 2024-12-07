from flask import abort, current_app
from app.models import Room,db


class CreateRoomCommand:
    @staticmethod
    def execute(name, capacity):
        """
        Create a new room and save to the database.
        """
        try:
            room = Room(name=name, capacity=capacity)
            db.session.add(room)
            db.session.commit()
            return room.id
        except Exception as e:
            current_app.logger.error(f"Error creating room: {e}")
            abort(500, description="Error creating room")
