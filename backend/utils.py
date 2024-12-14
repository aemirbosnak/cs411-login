import jwt
from flask import request
from config import Config

import logging

logging.basicConfig(level=logging.INFO)


def get_user_role(req):
    logging.info('hey3')
    auth_header = req.headers.get('Authorization')
    logging.info(auth_header)
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    logging.info(f'token: {token}')
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        logging.info(payload)
        logging.info(payload.get('role'))
        return payload.get('role')
    except:
        return None


def check_admin_role(req):
    return get_user_role(req) == 'admin'


def check_doctor_role(req):
    logging.info('hey2')
    return get_user_role(req) == 'doctor'
