import bcrypt
from src.extensions import mongo
from datetime import datetime


def create_user(email, first_name, last_name, phone_number, password, role):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    mongo.db.users.insert_one({
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "phoneNumber": phone_number,
        "password": hashed_password.decode('utf-8'),
        "role": role,
        "createdAt": datetime.now().timestamp(),
        "updatedAt": datetime.now().timestamp(),
    })


def find_by_email_role(email, role):
    return mongo.db.Users.find_one({"email": email, "role": role},
                                   {"email": 1, "firstName": 1, "lastName": 1, "role": 1, "password": 1})

