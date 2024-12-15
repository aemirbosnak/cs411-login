from models.patient_model import add_patient, list_patients, update_patient
from models.room_model import assign_room, availability

def admit_patient(data):
    required_fields = ["firstName", "lastName", "dob", "doctorId"]
    if not all(field in data for field in required_fields):
        return {"error": "Missing required patient data."}

    if "roomNumber" in data and data["roomNumber"]:
        # Verify the room exists and is available
        room_check_result = availability(data["roomNumber"])
        if "error" in room_check_result:
            return room_check_result

    new_patient = add_patient(data)

    # Check if room data is provided
    if "roomNumber" in data and data["roomNumber"]:
        room_data = {
            "assignedDoctor": new_patient["doctorId"],
            "patientId": str(new_patient["_id"]),
            "patientFirstName": new_patient["firstName"],
            "patientLastName": new_patient["lastName"],
        }

        # Attempt to assign the room
        room_assignment_result = assign_room(data["roomNumber"], room_data)
        if "error" in room_assignment_result:
            return room_assignment_result

    return new_patient


def update_patient_service(patient_id, updated_data):
    if not patient_id:
        return {"error": "Patient ID is required."}

    return update_patient(patient_id, updated_data)


def get_patients_service(doctor_id=None):
    return list_patients(doctor_id)
