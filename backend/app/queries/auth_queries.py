from backend.app import db
from backend.app.models import User
from app.constants.errors import ErrorMessages
class UserQueries:
    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch a user by their ID.
        """
        try:
            return db.session.query(User).filter_by(id=user_id).first()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(ErrorMessages.SERVER_ERROR) from e

    @staticmethod
    def get_all_users():
        """
        Fetch all users.
        """
        try:
            return db.session.query(User).all()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(ErrorMessages.SERVER_ERROR) from e