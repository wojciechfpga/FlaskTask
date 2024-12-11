from flask import Blueprint, jsonify, request
from app.commands.reservation_commands import CreateReservationCommand, SoftDeleteReservationCommand, UpdateReservationCommand
from app.queries.reservation_queries import ReservationQueries
from app.auth.middleware import authorization_jwt
from datetime import datetime

from app import db
from app.models import Reservation

bp = Blueprint('reservation', __name__)

@bp.route('/reservations', methods=['POST'])
@authorization_jwt("employee","admin")
def create_reservation(user_id):
    data = request.get_json()
    try:
        reservation_id = CreateReservationCommand.execute(
            room_id=data['room_id'],
            user_id=user_id,
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time'])
        )
        return jsonify({"message": "Reservation created", "id": reservation_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route('reservations/<int:reservation_id>', methods=['DELETE'])
@authorization_jwt("employee","admin")
def delete_reservation(reservation_id):
    SoftDeleteReservationCommand.execute(reservation_id)
    return jsonify({"message": "Reservation deleted"}), 200

    
@bp.route('/reservations/all', methods=['GET'])
@authorization_jwt("admin")
def get_all_reservations(user_id):
    """
    All reservations - admins only
    """
    reservations = ReservationQueries.get_reservations()
    return jsonify([{
        "id": r.id,
        "room_id": r.room_id,
        "user_id": r.user_id,
        "start_time": r.start_time.isoformat(),
        "end_time": r.end_time.isoformat()
    } for r in reservations])

@bp.route('/reservations/my', methods=['GET'])
@authorization_jwt("employee","admin")
def get_my_reservations(user_id):
    """
    Pobieranie rezerwacji zalogowanego użytkownika.
    """
    reservations = ReservationQueries.get_reservations_by_user_id(user_id)
    return jsonify([{
        "id": r.id,
        "room_id": r.room_id,
        "room_name": r.room.name, 
        "start_time": r.start_time.isoformat(),
        "end_time": r.end_time.isoformat()
    } for r in reservations])

@bp.route('reservations/<int:reservation_id>', methods=['PATCH'])
@authorization_jwt("employee","admin")
def update_reservation(user_id,reservation_id):
    data = request.get_json()
    reservation = UpdateReservationCommand.execute(reservation_id,data['room_id'],data['start_time'],data['end_time'])
    return jsonify({"id": reservation["id"],
                    "start_time": reservation["start_time"],
                    "end_time": reservation["end_time"],
                    "room_id": reservation["room_id"],
                    "room_name": reservation["room_name"],
                    }), 200