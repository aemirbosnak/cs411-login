from pymongo.errors import InvalidOperation
from src.extensions import mongo
from src.services.auth import is_valid_email, is_valid_role


def find_user(email, role):
    if is_valid_email(email) and is_valid_role(role):
        try:
            user = mongo.db.Users.find_one({"email": email, "role": role},
                                           {"email": 1, "firstName": 1, "lastName": 1, "role": 1, "password": 1})
            return user
        except InvalidOperation:
            return None
