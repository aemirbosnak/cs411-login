import pytest
import bcrypt
from config import Config
from modules.auth.services import (authenticate_user, verify_password)
from bson import ObjectId


def hash_password(plain):
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


@pytest.fixture(scope="function")
def setup_users(mock_db):
    # Insert a known admin user
    admin_password = hash_password("adminpass")
    Config.mongo_db.Users.insert_one({
        "_id": ObjectId(),
        "email": "admin@hospital.com",
        "firstName": "Alice",
        "lastName": "Admin",
        "password": admin_password,
        "role": "admin"
    })

    # Insert a known doctor user
    doctor_password = hash_password("doctorpass")
    Config.mongo_db.Users.insert_one({
        "_id": ObjectId(),
        "email": "doctor@hospital.com",
        "firstName": "Bob",
        "lastName": "Doctor",
        "password": doctor_password,
        "role": "doctor"
    })


def test_authenticate_user_success(mock_db, setup_users):
    # Test successful authentication for admin
    auth_response = authenticate_user("admin@hospital.com", "adminpass", "admin")
    assert auth_response is not None
    assert auth_response["user"]["role"] == "admin"
    assert "token" in auth_response

    # Test successful authentication for doctor
    auth_response = authenticate_user("doctor@hospital.com", "doctorpass", "doctor")
    assert auth_response is not None
    assert auth_response["user"]["role"] == "doctor"
    assert "token" in auth_response


def test_authenticate_user_wrong_password(mock_db, setup_users):
    # Wrong password should fail
    auth_response = authenticate_user("admin@hospital.com", "wrongpass", "admin")
    assert auth_response is None


def test_authenticate_user_wrong_role(mock_db, setup_users):
    # Correct credentials but wrong role
    auth_response = authenticate_user("admin@hospital.com", "adminpass", "doctor")
    assert auth_response is None


def test_verify_password():
    hashed = hash_password("test123")
    assert verify_password("test123", hashed) is True
    assert verify_password("wrong", hashed) is False


def test_login_endpoint_success(mock_db, setup_users, test_client):
    # Test login endpoint with correct creds
    response = test_client.post('/api/auth/login', json={
        "email": "admin@hospital.com",
        "password": "adminpass",
        "role": "admin"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Login successful"
    assert "token" in data

def test_login_endpoint_fail(mock_db, setup_users, test_client):
    # Wrong password
    response = test_client.post('/api/auth/login', json={
        "email": "admin@hospital.com",
        "password": "wrongpass",
        "role": "admin"
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data["message"] == "Invalid credentials"

    # Wrong role
    response = test_client.post('/api/auth/login', json={
        "email": "admin@hospital.com",
        "password": "adminpass",
        "role": "doctor"
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data["message"] == "Invalid credentials"

def test_logout_endpoint(test_client):
    # Logout doesn't check token, just returns success
    # But normally you'd send a token if logic was added.
    response = test_client.post('/api/auth/logout')
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Logout successful"
