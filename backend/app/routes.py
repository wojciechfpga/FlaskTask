from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models import Reservation, db, Room
from app.services.room_service import is_time_conflict
from app.commands.reservation_commands import CreateReservationCommand, SoftDeleteReservationCommand
from app.queries.reservation_queries import ReservationQueries
from app.auth.middleware import AuthorizationMiddleware
from app.commands.auth_commands import LoginUserCommand, RegisterUserCommand

bp = Blueprint('room', __name__)
bp_reservation = Blueprint('reservation', __name__)
bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{"id": room.id, "name": room.name, "capacity": room.capacity} for room in rooms])

@bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    room = Room(name=data['name'], capacity=data['capacity'])
    db.session.add(room)
    db.session.commit()
    return jsonify({"message": "Room created successfully", "id": room.id}), 201


@bp_reservation.route('/reservations', methods=['POST'])
@AuthorizationMiddleware.token_required
def create_reservation():
    """
    Tworzenie nowej rezerwacji.
    """
    data = request.get_json()
    try:
        reservation_id = CreateReservationCommand.execute(
            room_id=data.get("room_id"),
            start_time=datetime.fromisoformat(data.get("start_time")),
            end_time=datetime.fromisoformat(data.get("end_time"))
        )
        return jsonify({"message": "Reservation created", "id": reservation_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp_reservation.route('/reservations', methods=['GET'])
def get_reservations():
    """
    Pobieranie listy aktywnych rezerwacji.
    """
    room_id = request.args.get("room_id")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    reservations = ReservationQueries.get_reservations(
        room_id=int(room_id) if room_id else None,
        start_time=datetime.fromisoformat(start_time) if start_time else None,
        end_time=datetime.fromisoformat(end_time) if end_time else None
    )
    return jsonify([
        {
            "id": r.id,
            "room_id": r.room_id,
            "start_time": r.start_time.isoformat(),
            "end_time": r.end_time.isoformat()
        } for r in reservations
    ])

@bp_reservation.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    """
    Soft delete rezerwacji.
    """
    try:
        SoftDeleteReservationCommand.execute(reservation_id)
        return jsonify({"message": "Reservation deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
@bp_auth.route('/register', methods=['POST'])
def register():
    """
    Endpoint to register of user
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'employee')

        user_id = RegisterUserCommand.execute(username, password, role)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@bp_auth.route('/login', methods=['POST'])
def login():
    """
    Endpoint to login of user
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        token = LoginUserCommand.execute(username, password)
        return jsonify({"message": "Login successful", "token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500
