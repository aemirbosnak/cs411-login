from flask import session


def initialize_user_session(user):
    session['email'] = user['email']
    session['role'] = user['role']
    session['firstName'] = user['firstName']
    session['lastName'] = user['lastName']
