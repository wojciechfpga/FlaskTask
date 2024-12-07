from flask import Blueprint, jsonify, request

from app.commands.rooms_commands import CreateRoomCommand, DeleteRoomCommand, UpdateRoomCommand
from app.queries.rooms_queries import GetRoomsQuery
from app.auth.middleware import authorization_jwt


bp = Blueprint('room', __name__)

@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = GetRoomsQuery.execute()
    return jsonify(rooms)


@bp.route('/rooms', methods=['POST'])
@authorization_jwt("admin")
def create_room(user_id):
    data = request.get_json()
    room_id = CreateRoomCommand.execute(name=data['name'], capacity=data['capacity'])
    return jsonify({"message": "Room created successfully", "id": room_id}), 201

@bp.route('/rooms/<int:room_id>', methods=['PUT'])
@authorization_jwt("admin")
def update_room(user_id,room_id):
    data = request.get_json()
    UpdateRoomCommand.execute(
        room_id=room_id, 
        name=data.get('name'), 
        capacity=data.get('capacity'), 
        is_active=data.get('is_active')
    )
    return jsonify({"message": "Room updated successfully"}), 200

@bp.route('/rooms/<int:room_id>', methods=['DELETE'])
@authorization_jwt("admin")
def delete_room(user_id,room_id):
    DeleteRoomCommand.execute(
        room_id=room_id
    )
    return jsonify({"message": "Room deleted successfully"}), 200
