from config import Config
from bson import ObjectId
from . import convert_objectid_to_string


def create_room(data):
    new_room = {
        "roomNumber": data["roomNumber"],
        "roomType": data["roomType"],
        "occupied": False,
        "assignedDoctor": None,
        "patientId": None,
        "patientFirstName": None,
        "patientLastName": None,
    }
    result = Config.mongo_db.Rooms.insert_one(new_room)
    new_room['_id'] = str(result.inserted_id)
    return new_room


def remove_room(room_number):
    # Find and delete the room
    result = Config.mongo_db.Rooms.find_one_and_delete({"roomNumber": room_number})

    if result:
        # Successfully deleted the room
        return {"message": "Room successfully removed.", "room": result["roomNumber"]}
    else:
        # Room not found
        return {"error": "Room not found."}


def list_rooms():
    rooms = list(Config.mongo_db.Rooms.find())
    return [convert_objectid_to_string(room) for room in rooms]


def assign_room(room_number, patient_data):
    required_fields = ["patientId", "patientFirstName", "patientLastName"]
    if not all(field in patient_data for field in required_fields):
        return {"error": "Incomplete patient data provided."}

    update_result = Config.mongo_db.Rooms.update_one(
        {"roomNumber": room_number, "occupied": False},  # Only assign if the room is not occupied
        {
            "$set": {
                "occupied": True,
                "assignedDoctor": patient_data["assignedDoctor"],
                "patientId": patient_data["patientId"],
                "patientFirstName": patient_data["patientFirstName"],
                "patientLastName": patient_data["patientLastName"],
            }
        }
    )

    if update_result.matched_count == 0:
        return {"error": "Room not found or already occupied."}

    return {"message": "Patient successfully assigned to the room."}
