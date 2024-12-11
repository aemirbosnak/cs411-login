from config import Config
from bson import ObjectId
from . import convert_objectid_to_string

def list_available_rooms():
    rooms = list(Config.mongo_db.Rooms.find({"occupied": False}))
    return [convert_objectid_to_string(r) for r in rooms]


def assign_room(room_number, patient_id):
    """Mark a room as occupied and link it to a patient."""
    Config.mongo_db.Rooms.update_one({"roomNumber": room_number}, {"$set": {"occupied": True, "patientId": ObjectId(patient_id)}})
    return True


def free_room(room_number):
    """Mark a room as free."""
    Config.mongo_db.Rooms.update_one({"roomNumber": room_number}, {"$set": {"occupied": False, "patientId": None}})
    return True


def get_room_info(room_number):
    room = Config.mongo_db.Rooms.find_one({"roomNumber": room_number})
    if room:
        return convert_objectid_to_string(room)
    return None
