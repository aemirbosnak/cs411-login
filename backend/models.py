import re
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
    return re.match(regex, email)


def is_valid_role(role):
    return role in UserRole.__members__.values()
