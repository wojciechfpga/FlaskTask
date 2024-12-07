from datetime import datetime
from app.models import db, Reservation

class ReservationQueries:
    @staticmethod
    def get_reservations(room_id=None, start_time=None, end_time=None):
        """
        Pobiera listę aktywnych rezerwacji z optymalizacją zapytań.
        """
        query = db.session.query(Reservation).filter(Reservation.is_deleted == False)

        if room_id:
            query = query.filter(Reservation.room_id == room_id)
        if start_time:
            query = query.filter(Reservation.end_time > start_time)
        if end_time:
            query = query.filter(Reservation.start_time < end_time)

        # Ograniczenie liczby zwracanych wyników
        return query.order_by(Reservation.start_time).limit(100).all()

    @staticmethod
    def get_reservation_by_id(reservation_id):
        """
        Downloading one reservation based on ID
        """
        return db.session.query(Reservation).filter_by(id=reservation_id, is_deleted=False).first()
