from models.admission_model import add_inpatient, list_inpatients, list_doctor_inpatients, update_inpatient
from models.patient_model import list_admitted_patients_not_in_inpatients
from models.room_model import list_available_rooms, assign_room, free_room

WAITLIST = []  # In-memory waitlist. For production, store in DB


def search_patient(query):
    # This would call admission services or models to find admission by query
    # For demo, return a fake result
    if query == "John Doe":
        return {"patientId": "some_patient_id", "found": True}
    return {"found": False}


def place_on_waitlist(patient_id):
    WAITLIST.append(patient_id)
    return True


def assign_doctor_to_patient(patient_id, doctor_id):
    # In reality, you'd update the inpatient record or admission record to link doctor
    # Not implemented in the model yet, but you could extend `update_inpatient` or create a new method
    # For demo:
    return True


def save_admission(data):
    # Validate data fields first
    required_fields = ['patientId', 'roomNumber', 'assignedDoctor', 'admissionReason', 'admissionDate']
    if not all(field in data for field in required_fields):
        raise ValueError("Missing required fields")

    # Create inpatient record
    inpatient = add_inpatient(data)
    return inpatient


def get_admission_summary(admission_id):
    # For a real summary, you need admission, room, doctor info
    # Could query admission by `inpatient['patientId']`, room by `roomNumber`, etc.
    # For demo:
    return {
        "admissionId": admission_id,
        "admission": {"firstName": "John", "lastName": "Doe"},
        "room": {"roomNumber": "101"},
        "doctor": {"email": "doctor@hospital.com"},
        "admissionDetails": {"admissionReason": "Surgery", "admissionDate": "2024-12-10"}
    }


def get_available_rooms_service():
    return list_available_rooms()


def assign_room_service(patient_id, room_number):
    # Ensure the room is available before assigning
    available_rooms = list_available_rooms()
    if any(r['roomNumber'] == room_number for r in available_rooms):
        assign_room(room_number, patient_id)
        return True
    else:
        return False


def list_all_inpatients_service():
    return list_inpatients()


def list_doctor_inpatients_service(doctor_email):
    return list_doctor_inpatients(doctor_email)


def update_inpatient_service(inpatient_id, updates):
    update_inpatient(inpatient_id, updates)
    return True
