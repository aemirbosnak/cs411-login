from flask import Blueprint, request, jsonify
from modules.rooms.services import (
    create_room_service,
    list_rooms_service,
    remove_room_service,
    assign_room_service,
)

room_bp = Blueprint("room", __name__, url_prefix="/api/room")

@room_bp.route("/create", methods=["POST"])
def create_room():
    data = request.json
    result = create_room_service(data)
    return jsonify(result)


@room_bp.route("/list", methods=["GET"])
def list_rooms():
    result = list_rooms_service()
    return jsonify(result)


@room_bp.route("/remove/<room_number>", methods=["DELETE"])
def remove_room(room_number):
    result = remove_room_service(room_number)
    return jsonify(result)
