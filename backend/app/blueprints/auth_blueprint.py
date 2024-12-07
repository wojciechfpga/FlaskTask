from flask import Blueprint, jsonify, request
from app.commands.auth_commands import LoginUserCommand, RegisterUserCommand

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_id = RegisterUserCommand.execute(
            username=data['username'], 
            password=data['password'], 
            role=data.get('role', 'employee')
        )
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        token = LoginUserCommand.execute(
            username=data['username'], 
            password=data['password']
        )
        return jsonify({"message": "Login successful", "token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
