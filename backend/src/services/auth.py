import datetime
import jwt
import bcrypt
from backend.src.models import find_user
from backend.src.config import Config

SECRET_KEY = Config.JWT_SECRET_KEY


def authenticate_user(email, password, role):
    user = find_user(email, role)

    if user and verify_password(password, user['password']):
        token = create_jwt(user)
        return {
            "user": {
                "firstName": user['firstName'],
                "lastName": user['lastName'],
                "role": user['role']
            },
            "token": token
        }

    return None


def verify_password(provided_password, stored_password):
    encoded_provided_password = provided_password.encode('utf-8')
    encoded_stored_password = stored_password.encode('utf-8')

    password_matches = bcrypt.checkpw(encoded_provided_password, encoded_stored_password)
    return password_matches


def create_jwt(user):
    payload = {
        "email": user['email'],
        "role": user['role'],
        "firstName": user['firstName'],
        "lastName": user['lastName'],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiry time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
