from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models import Reservation, db, Room
from app.services.room_service import is_time_conflict

bp = Blueprint('room', __name__)
bp_reservation = Blueprint('reservation', __name__)

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
def create_reservation():
    """
    Tworzenie nowej rezerwacji.
    """
    data = request.get_json()
    room_id = data.get("room_id")
    start_time = datetime.fromisoformat(data.get("start_time"))
    end_time = datetime.fromisoformat(data.get("end_time"))

    # Walidacja czasu
    if start_time >= end_time:
        return jsonify({"error": "Invalid time range"}), 400

    # Sprawdzenie konfliktu
    if is_time_conflict(room_id, start_time, end_time):
        return jsonify({"error": "Time conflict for the selected room"}), 409

    # Tworzenie rezerwacji
    reservation = Reservation(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Reservation created", "id": reservation.id}), 201

@bp_reservation.route('/reservations', methods=['GET'])
def get_reservations():
    """
    Pobieranie listy rezerwacji z opcjonalnym filtrowaniem.
    """
    room_id = request.args.get("room_id")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    query = db.session.query(Reservation)

    if room_id:
        query = query.filter(Reservation.room_id == int(room_id))
    if start_time and end_time:
        query = query.filter(
            Reservation.start_time >= datetime.fromisoformat(start_time),
            Reservation.end_time <= datetime.fromisoformat(end_time)
        )

    reservations = query.all()
    return jsonify([
        {
            "id": r.id,
            "room_id": r.room_id,
            "start_time": r.start_time.isoformat(),
            "end_time": r.end_time.isoformat()
        } for r in reservations
    ])
