from app.models import db, User
import jwt
import datetime
from flask import current_app
from app.models import User

class RegisterUserCommand:
    @staticmethod
    def execute(username, password, role="employee"):
        """
        Register a new user with a hashed password.
        """
        if not username or not password:
            raise ValueError("Username and password are required")

        existing_user = db.session.query(User).filter_by(username=username).first()
        if existing_user:
            raise ValueError("Username already exists")

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return user.id



class LoginUserCommand:
    @staticmethod
    def execute(username, password):
        """
        Authenticate user and generate JWT token if credentials are valid.
        """
        user = db.session.query(User).filter_by(username=username).first()

        if not user or not user.check_password(password):
            raise ValueError("Invalid username or password")
 
       
        try:
            token = jwt.encode(
                {"user_id": user.id, "role": user.role, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )            
            return token
        except Exception as e:
            my=str(e)
            return my
