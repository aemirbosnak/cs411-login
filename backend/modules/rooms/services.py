from models.room_model import create_room, remove_room, list_rooms, assign_room


def create_room_service(data):
    if "roomNumber" not in data:
        return {"error": "Room number is required."}

    return create_room(data)


def list_rooms_service():
    rooms = list_rooms()
    return {"rooms": rooms}


def remove_room_service(room_id):
    if not room_id:
        return {"error": "Room ID is required."}

    return remove_room(room_id)


def assign_room_service(room_id, patient_data):
    if not room_id:
        return {"error": "Room ID is required."}

    required_fields = ["patientId", "patientFirstName", "patientLastName"]
    if not all(field in patient_data for field in required_fields):
        return {"error": "Incomplete patient data provided."}

    return assign_room(room_id, patient_data)
