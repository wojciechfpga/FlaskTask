from app.models import db, User
import jwt
import datetime
from flask import current_app,abort
from app.models import User

from flask import jsonify
import flask_monitoringdashboard as dashboard

#from app import app

class RegisterUserCommand:
    @staticmethod
    def execute(username, password, role):
        """
        Register a new user with a hashed password.
        """
        try:
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
        except ValueError as ve:
            current_app.logger.info(ve)
            abort(409, description=str(ve)) 
        except Exception as e:
            current_app.logger.info(e)
            abort(500, description="Some Error...") 
        finally:
            print("User registration attempt logged")




class LoginUserCommand:
    @staticmethod
    def execute(username, password):
        """
        Authenticate user and generate JWT token if credentials are valid.
        """
        try:
            user = db.session.query(User).filter_by(username=username).first()

            if not user or not user.check_password(password):
                raise ValueError("Invalid username or password")

            token = jwt.encode(
                {"user_id": user.id, "role": user.role, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            return token
        except ValueError as ve:
            current_app.logger.info(ve)
            abort(403, description=str(ve)) 
        except Exception as e:
            current_app.logger.info(e)
            abort(500, description="Some error occured. Try later") 
        finally:
            print("Login attempt logged")

