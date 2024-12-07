from flask import Blueprint, jsonify, request
from app.commands.reservation_commands import CreateReservationCommand, SoftDeleteReservationCommand
from app.queries.reservation_queries import ReservationQueries
from app.auth.middleware import AuthorizationMiddleware, role_required
from datetime import datetime

from app import db
from app.models import Reservation

bp = Blueprint('reservation', __name__)

@bp.route('/reservations', methods=['POST'])
@AuthorizationMiddleware.token_required
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

@bp.route('/reservations', methods=['GET'])
def get_reservations():
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

@bp.route('reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    try:
        SoftDeleteReservationCommand.execute(reservation_id)
        return jsonify({"message": "Reservation deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
@bp.route('/reservations/all', methods=['GET'])
@role_required("admin")
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
@AuthorizationMiddleware.token_required
def get_my_reservations(user_id):
    """
    Pobieranie rezerwacji zalogowanego użytkownika.
    """
    reservations = ReservationQueries.get_reservations_by_user_id(user_id)
    return jsonify([{
        "id": r.id,
        "room_id": r.room_id,
        "start_time": r.start_time.isoformat(),
        "end_time": r.end_time.isoformat()
    } for r in reservations])