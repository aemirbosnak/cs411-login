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
        "address": data['address'],
        "doctorId": data['doctorId'],
        "complaint": data.get('complaint', 'N/A'),  # Default to 'N/A' if not provided
        "severity": data.get('severity', 'low'),  # Default to 'low' if not provided
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
        "address": 1,
        "doctorId": 1,
        "complaint": 1,
        "severity": 1
    }))
    return [convert_objectid_to_string(patient) for patient in patients]