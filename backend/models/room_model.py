from config import Config
from bson import ObjectId

def create_room(data):
    new_room = {
        "roomNumber": data["roomNumber"],
        "roomType": data["roomType"],
        "occupied": False,
        "patientId": None,
        "patientFirstName": None,
        "patientLastName": None,
    }
    result = Config.mongo_db.Rooms.insert_one(new_room)
    new_room['_id'] = str(result.inserted_id)
    return new_room


def remove_room(room_id):
    # Convert the room_id to ObjectId format if it's a valid string
    try:
        room_object_id = ObjectId(room_id)
    except Exception as e:
        return {"error": "Invalid room ID format."}

    # Find and delete the room
    result = Config.mongo_db.Rooms.find_one_and_delete({"_id": room_object_id})

    if result:
        # Successfully deleted the room
        result["_id"] = str(result["_id"])  # Convert ObjectId to string for consistency
        return {"message": "Room successfully removed.", "room": result}
    else:
        # Room not found
        return {"error": "Room not found."}


def list_rooms():
    rooms = list(Config.mongo_db.Rooms.find({
        "roomNumber": 1,
        "roomType": 1,
        "occupied": 1,
        "patientFirstName": 1,
        "patientLastName": 1,
    }))
    return rooms

def assign_room(room_id, patient_data):
    try:
        room_object_id = ObjectId(room_id)
    except Exception as e:
        return {"error": "Invalid room ID format."}

    required_fields = ["patientId", "patientFirstName", "patientLastName"]
    if not all(field in patient_data for field in required_fields):
        return {"error": "Incomplete patient data provided."}

    update_result = Config.mongo_db.Rooms.update_one(
        {"_id": room_object_id, "occupied": False},  # Only assign if the room is not occupied
        {
            "$set": {
                "roomType": patient_data["roomType"],
                "occupied": True,
                "patientId": patient_data["patientId"],
                "patientFirstName": patient_data["patientFirstName"],
                "patientLastName": patient_data["patientLastName"],
            }
        }
    )

    if update_result.matched_count == 0:
        return {"error": "Room not found or already occupied."}

    return {"message": "Patient successfully assigned to the room."}
