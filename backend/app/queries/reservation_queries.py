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

        return query.order_by(Reservation.start_time).limit(100).all()

    @staticmethod
    def get_reservations_by_user_id(user_id):
        """
        Pobiera wszystkie aktywne rezerwacje dla danego użytkownika.
        """
        return db.session.query(Reservation).filter_by(user_id=user_id, is_deleted=False).all()

    @staticmethod
    def get_reservation_by_id(reservation_id):
        """
        Pobiera jedną rezerwację na podstawie ID.
        """
        return db.session.query(Reservation).filter_by(id=reservation_id, is_deleted=False).first()
