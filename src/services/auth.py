import bcrypt
import re
from src.models import find_user


# TODO: add google oauth SSO
def authenticate_user(email, password, role):
    user = find_user(email, role)

    if user is not None:
        is_valid_password = verify_password(password, user['password'])
        if is_valid_password:
            return user

    return None


def verify_password(provided_password, stored_password):
    encoded_provided_password = provided_password.encode('utf-8')
    encoded_stored_password = stored_password.encode('utf-8')

    password_matches = bcrypt.checkpw(encoded_provided_password, encoded_stored_password)
    return password_matches


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)


def is_valid_role(role):
    if role in ['admin', 'user']:
        return True
    else:
        return False
