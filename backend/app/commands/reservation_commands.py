from datetime import datetime
from flask import abort
from app.models import db, Reservation
from app.services.room_service import is_time_conflict

from app.models import db, Reservation

class CreateReservationCommand:
    @staticmethod
    def execute(room_id, user_id, start_time, end_time):
        """
        Creating new reservation without any conflict
        """
        if start_time >= end_time:
            raise ValueError("Invalid time range")

        if is_time_conflict(room_id, start_time, end_time):
            raise ValueError("Time conflict for the selected room")

        reservation = Reservation(
            room_id=room_id,
            user_id=user_id,  
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation.id


class SoftDeleteReservationCommand:
    @staticmethod
    def execute(reservation_id):
        """
        Mark reservation as deleted (in DB - soft delete)
        """
        reservation = db.session.query(Reservation).filter_by(id=reservation_id).first()
        if not reservation or reservation.is_deleted:
            raise ValueError("Reservation not found or already deleted")

        reservation.is_deleted = True
        db.session.commit()


class UpdateReservationCommand:
    @staticmethod
    def execute(id, room_id, start_time, end_time):
        """
        Updating existing reservation without any conflict
        """
        try:
            if start_time >= end_time or is_time_conflict(room_id, start_time, end_time):
                raise ValueError("Invalid time range or someone already reserved this room for this time")
                

            reservation = db.session.query(Reservation).filter_by(id=id).one()
            reservation.start_time = start_time
            reservation.end_time = end_time

            db.session.commit()
            return {
                "id": reservation.id,
                "start_time": reservation.start_time,
                "end_time": reservation.end_time,
                "room_id": reservation.room_id,
                "room_name": reservation.room.name,
            }
        except ValueError as e:
            abort(409, description=str(e))
        except Exception as e:
            db.session.rollback()
            abort(500, description="Some error..try later")

