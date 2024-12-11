from datetime import datetime
from config import Config
from bson import ObjectId
from . import convert_objectid_to_string


def add_inpatient(data):
    inpatient = {
        "patientId": ObjectId(data['patientId']),
        "roomNumber": data['roomNumber'],
        "assignedDoctor": data['assignedDoctor'],
        "admissionReason": data['admissionReason'],
        "admissionDate": data['admissionDate'],
        "operationDetails": data.get('operationDetails', None),
        "dischargeDate": data.get('dischargeDate', None),
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    }
    result = Config.mongo_db.Inpatients.insert_one(inpatient)
    inpatient['_id'] = str(result.inserted_id)
    inpatient['patientId'] = str(inpatient['patientId'])
    return inpatient


def list_inpatients():
    """List all inpatients (for admin)."""
    inpatients = list(Config.mongo_db.Inpatients.find({}, {
        "patientId": 1,
        "roomNumber": 1,
        "assignedDoctor": 1,
        "admissionReason": 1,
        "admissionDate": 1,
        "dischargeDate": 1
    }))
    return [convert_objectid_to_string(inpatient) for inpatient in inpatients]


def list_doctor_inpatients(doctor_email):
    """List inpatients for a specific doctor."""
    inpatients = list(Config.mongo_db.Inpatients.find({"assignedDoctor": doctor_email}, {
        "patientId": 1,
        "roomNumber": 1,
        "admissionReason": 1,
        "admissionDate": 1,
        "dischargeDate": 1
    }))
    return [convert_objectid_to_string(inpatient) for inpatient in inpatients]


def update_inpatient(inpatient_id, updates):
    updates["updatedAt"] = datetime.now()
    Config.mongo_db.Inpatients.update_one({"_id": ObjectId(inpatient_id)}, {"$set": updates})
    return True
