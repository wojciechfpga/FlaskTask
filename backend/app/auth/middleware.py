from functools import wraps
import jwt
from flask import request, jsonify, current_app

from app import db
from app.models import User

class AuthorizationMiddleware:
    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Token is missing"}), 401

            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                kwargs['user_id'] = data["user_id"]
                #kwargs['role'] = data["role"]
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)
        return decorated

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Token is missing"}), 401

            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                user_id = data.get("user_id")
                user = db.session.query(User).filter_by(id=user_id).first()
                if not user or user.role != required_role:
                    return jsonify({"error": "Access denied"}), 403
                kwargs['user_id'] = user_id
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)
        return decorated
    return decorator
