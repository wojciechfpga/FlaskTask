from datetime import datetime
from app.models import db, Reservation
from app.services.room_service import is_time_conflict

class CreateReservationCommand:
    @staticmethod
    def execute(room_id, start_time, end_time):
        """
        Creating new reservation without any conflict
        """
        if start_time >= end_time:
            raise ValueError("Invalid time range")

        if is_time_conflict(room_id, start_time, end_time):
            raise ValueError("Time conflict for the selected room")

        reservation = Reservation(
            room_id=room_id,
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