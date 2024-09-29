from flask import Blueprint, request, jsonify, session
from backend.services.auth import authenticate_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    auth_response = authenticate_user(email, password, role)

    if auth_response:
        return jsonify(
            {"message": "Login successful",
             "token": auth_response['token'],
             "user": auth_response['user']}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    # The client should handle JWT token deletion
    return jsonify({"message": "Logout successful"}), 200
