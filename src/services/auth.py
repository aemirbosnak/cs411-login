import bcrypt
from src.models import find_by_email_role


def login_user(email, password, role):
    # TODO: Make more readable
    # TODO: Add SSO with Google
    user = find_by_email_role(email, role)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return user
    return None
