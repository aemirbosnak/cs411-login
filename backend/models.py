import re
import datetime
from enum import Enum
from pymongo.errors import InvalidOperation
from config import Config
from bson import ObjectId


class UserRole(Enum):
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    # Add more roles as needed


def convert_objectid_to_string(document):
    if '_id' in document:
        document['_id'] = str(document['_id'])
    if 'patientId' in document and isinstance(document['patientId'], ObjectId):
        document['patientId'] = str(document['patientId'])
    return document


def find_user(email, role):
    if is_valid_email(email) and is_valid_role(role):
        try:
            user = Config.mongo_db.Users.find_one({"email": email, "role": role},
                                           {"email": 1, "firstName": 1, "lastName": 1, "role": 1, "password": 1})
            return user
        except InvalidOperation:
            return None


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(regex, email))


def is_valid_role(role):
    return role in (member.value for member in UserRole)


def add_patient(data):
    """Add a patient to the database."""
    new_patient = {
        "firstName": data['firstName'],
        "lastName": data['lastName'],
        "dob": data['dob'],
        "gender": data['gender'],
        "address": data['address'],
        "contactNumber": data['contactNumber'],
        "emergencyContact": data['emergencyContact'],
        "insuranceInfo": data.get('insuranceInfo', 'N/A'),
        "occupation": data.get('occupation', 'N/A'),
        "maritalStatus": data.get('maritalStatus', 'N/A'),
        "complaint": data.get('complaint', 'N/A'),
        "severity": data.get('severity', 'low'),
        "doctorId": data['doctorId'],
        "createdAt": datetime.datetime.now(),
        "updatedAt": datetime.datetime.now(),
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


def add_inpatient(data):
    inpatient = {
        "patientId": ObjectId(data['patientId']),
        "roomNumber": data['roomNumber'],
        "assignedDoctor": data['assignedDoctor'],
        "admissionReason": data['admissionReason'],
        "admissionDate": data['admissionDate'],
        "operationDetails": data.get('operationDetails', None),
        "dischargeDate": data.get('dischargeDate', None),
        "createdAt": datetime.datetime.now(),
        "updatedAt": datetime.datetime.now()
    }
    result = Config.mongo_db.Inpatients.insert_one(inpatient)
    inpatient['_id'] = str(result.inserted_id)
    inpatient['patientId'] = str(inpatient['patientId'])
    return inpatient


def update_inpatient(inpatient_id, updates):
    # updates could include roomNumber, operationDetails, dischargeDate
    updates["updatedAt"] = datetime.datetime.now()
    Config.mongo_db.Inpatients.update_one({"_id": ObjectId(inpatient_id)}, {"$set": updates})
    return True


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
