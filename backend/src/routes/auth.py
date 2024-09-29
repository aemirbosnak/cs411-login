from flask import Blueprint, request, jsonify, session
from backend.src.services.auth import authenticate_user
from backend.src.services.session import initialize_user_session

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    user = authenticate_user(email, password, role)

    if user:
        initialize_user_session(user)
        return jsonify({"message": "Login successful",
                        "user": {"firstName": user['firstName'],
                                 "lastName": user['lastName'],
                                 "role": user['role']}}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200
