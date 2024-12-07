from flask import Blueprint, jsonify, request

from app.commands.rooms_commands import CreateRoomCommand
from app.queries.rooms_queries import GetRoomsQuery


bp = Blueprint('room', __name__)

@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = GetRoomsQuery.execute()
    return jsonify(rooms)

@bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    room_id = CreateRoomCommand.execute(name=data['name'], capacity=data['capacity'])
    return jsonify({"message": "Room created successfully", "id": room_id}), 201
