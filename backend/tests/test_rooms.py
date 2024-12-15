import pytest
from config import Config
from modules.rooms.services import create_room_service, list_rooms_service, remove_room_service, assign_room_service


def test_create_room_success(mock_db):
    # Create a new room
    data = {"roomNumber": "103", "roomType": "VIP"}
    result = create_room_service(data)

    assert "error" not in result
    assert result["roomNumber"] == "103"
    assert result["roomType"] == "VIP"
    assert result["occupied"] is False


def test_create_room_missing_room_number(mock_db):
    # Missing room number should return an error
    data = {"roomType": "Deluxe"}
    result = create_room_service(data)

    assert "error" in result
    assert result["error"] == "Room number is required."


def test_list_rooms_success(mock_db):
    # Add rooms to the database
    Config.mongo_db.Rooms.insert_many([
        {"roomNumber": "101", "roomType": "Standard", "occupied": False},
        {"roomNumber": "102", "roomType": "Deluxe", "occupied": True}
    ])

    # Call the service to list rooms
    result = list_rooms_service()

    assert "rooms" in result
    assert len(result["rooms"]) == 2


def test_remove_room_success(mock_db):
    # Add a room to the database
    Config.mongo_db.Rooms.insert_one({"roomNumber": "101", "roomType": "Deluxe", "occupied": False})

    # Remove the room
    result = remove_room_service("101")

    assert "error" not in result
    assert result["message"] == "Room successfully removed."

    # Verify the room no longer exists
    room = Config.mongo_db.Rooms.find_one({"roomNumber": "101"})
    assert room is None


def test_remove_room_not_found(mock_db):
    # Try to remove a non-existent room
    result = remove_room_service("999")

    assert "error" in result
    assert result["error"] == "Room not found."


def test_assign_room_success(mock_db):
    # Add a room to the database
    Config.mongo_db.Rooms.insert_one({
        "roomNumber": "101",
        "roomType": "Deluxe",
        "occupied": False
    })

    # Assign the room to a patient
    room_id = "101"
    patient_data = {
        "assignedDoctor": "doctor123",
        "patientId": "patient123",
        "patientFirstName": "John",
        "patientLastName": "Doe"
    }
    result = assign_room_service(room_id, patient_data)

    assert "error" not in result
    assert result["message"] == "Patient successfully assigned to the room."

    # Verify the room is marked as occupied
    room = Config.mongo_db.Rooms.find_one({"roomNumber": "101"})
    assert room["occupied"] is True
    assert room["patientFirstName"] == "John"
    assert room["patientLastName"] == "Doe"


def test_assign_room_not_available(mock_db):
    # Add an occupied room to the database
    Config.mongo_db.Rooms.insert_one({
        "roomNumber": "101",
        "roomType": "Deluxe",
        "occupied": True
    })

    # Attempt to assign the room to a patient
    room_id = "101"
    patient_data = {
        "assignedDoctor": "doctor123",
        "patientId": "patient123",
        "patientFirstName": "John",
        "patientLastName": "Doe"
    }
    result = assign_room_service(room_id, patient_data)

    assert "error" in result
    assert result["error"] == "Room not found or already occupied."
