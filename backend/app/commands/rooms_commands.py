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


class UpdateRoomCommand:
    @staticmethod
    def execute(room_id, name=None, capacity=None, is_active=None):
        """
        Update a room's details based on the given parameters.
        """
        try:
            room = Room.query.get(room_id)
            if not room:
                raise ValueError("Room not found.")

            # Update room details only if new values are provided
            if name is not None:
                if Room.query.filter(Room.name == name, Room.id != room_id).first():
                    raise ValueError(f"A room with name '{name}' already exists.")
                room.name = name

            if capacity is not None:
                room.capacity = capacity
            
            if is_active is not None:
                room.is_active = is_active

            db.session.commit()

        except ValueError as ve:
            current_app.logger.info(ve)
            abort(400, description=str(ve))

        except Exception as e:
            current_app.logger.error(f"Error updating room: {e}")
            abort(500, description="Error updating room")


