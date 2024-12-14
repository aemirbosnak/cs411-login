from flask import Blueprint, request, jsonify
from modules.room.services import (
    create_room_service,
    list_rooms_service,
    remove_room_service,
    assign_room_service,
)

room_bp = Blueprint("room", __name__)


@room_bp.route("/create_room", methods=["POST"])
def create_room():
    data = request.json
    result = create_room_service(data)
    return jsonify(result)


@room_bp.route("/list_rooms", methods=["GET"])
def list_rooms():
    result = list_rooms_service()
    return jsonify(result)


@room_bp.route("/remove_room/<room_id>", methods=["DELETE"])
def remove_room(room_id):
    result = remove_room_service(room_id)
    return jsonify(result)


@room_bp.route("/assign_room/<room_id>", methods=["POST"])
def assign_room(room_id):
    patient_data = request.json
    result = assign_room_service(room_id, patient_data)
    return jsonify(result)
