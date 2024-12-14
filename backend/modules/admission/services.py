from models.patient_model import add_patient, list_patients, update_patient
import logging

logging.basicConfig(level=logging.INFO)

def admit_patient(data):
    logging.info(data)
    required_fields = ["firstName", "lastName", "dob", "doctorId"]
    if not all(field in data for field in required_fields):
        return {"error": "Missing required patient data."}

    return add_patient(data)


def update_patient_service(patient_id, updated_data):
    if not patient_id:
        return {"error": "Patient ID is required."}

    return update_patient(patient_id, updated_data)


def get_patients_service(doctor_id=None):
    return list_patients(doctor_id)
