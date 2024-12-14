from datetime import datetime
from config import Config
from bson import ObjectId
from . import convert_objectid_to_string

def add_patient(data):
    """Add a admission to the database."""
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
        "roomNumber": data['roomNumber'],
        "admissionReason": data['admissionReason'],
        "admissionDate": data['admissionDate'],
        "operationDetails": data.get('operationDetails', None),
        "dischargeDate": data.get('dischargeDate', None),
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
        "severity": 1,
        "roomNumber": 1,
        "admissionReason": 1,
        "admissionDate": 1,
        "dischargeDate": 1
    }))
    return [convert_objectid_to_string(patient) for patient in patients]
