from datetime import datetime
from config import Config
from bson import ObjectId
from . import convert_objectid_to_string

def add_patient(data):
    """Add a patient to the database."""
    new_patient = {
        "firstName": data['firstName'],
        "lastName": data['lastName'],
        "dob": data['dob'],
        "gender": data.get('gender', 'N/A'),
        "address": data['address'],
        "contactNumber": data.get('contactNumber', 'N/A'),
        "emergencyContact": data.get('emergencyContact', 'N/A'),
        "insuranceInfo": data.get('insuranceInfo', 'N/A'),
        "occupation": data.get('occupation', 'N/A'),
        "maritalStatus": data.get('maritalStatus', 'N/A'),
        "complaint": data.get('complaint', 'N/A'),
        "severity": data.get('severity', 'low'),
        "doctorId": data['doctorId'],
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    }
    result = Config.mongo_db.Patients.insert_one(new_patient)
    new_patient['_id'] = str(result.inserted_id)
    return new_patient


def list_patients(doctor_id):
    """List all patients assigned to a specific doctor."""
    patients = list(Config.mongo_db.Patients.find({"doctorId": doctor_id}, {
        "firstName": 1,
        "lastName": 1,
        "dob": 1,
        "gender": 1,
        "address": 1,
        "contactNumber": 1,
        "emergencyContact": 1,
        "insuranceInfo": 1,
        "occupation": 1,
        "maritalStatus": 1,
        "complaint": 1,
        "severity": 1
    }))
    return [convert_objectid_to_string(patient) for patient in patients]


def list_admitted_patients_not_in_inpatients():
    admitted_patient_ids = Config.mongo_db.Patients.distinct("_id")
    inpatient_patient_ids = Config.mongo_db.Inpatients.distinct("patientId")
    difference = set(admitted_patient_ids) - set(inpatient_patient_ids)
    patients = list(Config.mongo_db.Patients.find({"_id": {"$in": list(difference)}}))
    return [convert_objectid_to_string(p) for p in patients]
