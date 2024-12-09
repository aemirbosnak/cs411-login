import re
import datetime
from enum import Enum
from pymongo.errors import InvalidOperation
from config import Config


class UserRole(Enum):
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    # Add more roles as needed


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
    new_patient = {
        "firstName": data['firstName'],
        "lastName": data['lastName'],
        "dob": data['dob'],  # Date of Birth
        "address": data['address'],
        "doctorId": data['doctorId'],
        "createdAt": datetime.datetime.now(),
        "updatedAt": datetime.datetime.now(),
    }
    Config.mongo_db.Patients.insert_one(new_patient)
    return new_patient


def list_patients(doctor_id):
    patients = list(Config.mongo_db.Patients.find({"doctorId": doctor_id}, {
        "firstName": 1, "lastName": 1, "dob": 1, "address": 1, "doctorId": 1
    }))
    return patients
