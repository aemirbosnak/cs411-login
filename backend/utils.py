import jwt
from flask import request
from config import Config


def get_user_role(req):
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload.get('role')
    except:
        return None


def check_admin_role(req):
    return get_user_role(req) == 'admin'


def check_doctor_role(req):
    return get_user_role(req) == 'doctor'
