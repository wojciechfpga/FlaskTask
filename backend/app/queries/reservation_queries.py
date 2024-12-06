from datetime import datetime
from app.models import db, Reservation

class ReservationQueries:
    @staticmethod
    def get_reservations(room_id=None, start_time=None, end_time=None):
        """
        Downloading list of reservations
        """
        query = db.session.query(Reservation).filter_by(is_deleted=False)

        if room_id:
            query = query.filter(Reservation.room_id == room_id)
        if start_time and end_time:
            query = query.filter(
                Reservation.start_time >= start_time,
                Reservation.end_time <= end_time
            )

        return query.all()

    @staticmethod
    def get_reservation_by_id(reservation_id):
        """
        Downloading one reservation based on ID
        """
        return db.session.query(Reservation).filter_by(id=reservation_id, is_deleted=False).first()
