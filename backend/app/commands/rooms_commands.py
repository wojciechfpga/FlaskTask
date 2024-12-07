from flask import abort, current_app
from app.models import Room,db


class CreateRoomCommand:
    @staticmethod
    def execute(name, capacity):
        """
        Create a new room and save to the database, ensuring no room with the same name exists.
        """
        try:
            existing_room = Room.query.filter_by(name=name).first()
            if existing_room:
                raise ValueError(f"A room with this name already exists.")

            room = Room(name=name, capacity=capacity)
            db.session.add(room)
            db.session.commit()
            return room.id
        
        except ValueError as ve:
            current_app.logger.info(ve)
            abort(409, description=str(ve))
        
        except Exception as e:
            current_app.logger.error(f"Error creating room: {e}")
            abort(500, description="Error creating room") 
        
        finally:
            print("Create room operation attempt logged")

