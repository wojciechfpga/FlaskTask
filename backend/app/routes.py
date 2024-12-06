from flask import Blueprint, jsonify, request
from app.models import db, Room

bp = Blueprint('room', __name__)

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
