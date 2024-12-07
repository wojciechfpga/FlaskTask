from backend.app import db
from backend.app.models import User


class UserQueries:
    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch a user by their ID.
        """
        return db.session.query(User).filter_by(id=user_id).first()

    @staticmethod
    def get_all_users():
        """
        Fetch all users.
        """
        return db.session.query(User).all()
