import pytest
from config import Config
from bson import ObjectId
from modules.admission.services import (
    search_patient, place_on_waitlist, assign_doctor_to_patient, save_admission,
    get_admission_summary, get_available_rooms_service, assign_room_service,
    list_all_inpatients_service, list_doctor_inpatients_service, update_inpatient_service
)


def test_search_patient_service(mock_db):
    # Assuming search_patient returns a dict with found: bool
    result = search_patient("John Doe")
    # With current mock logic, "John Doe" = found
    assert "found" in result


def test_place_on_waitlist(mock_db):
    success = place_on_waitlist("patient_id")
    assert success is True
    # Check WAITLIST if accessible from services (not in final code)
    # Just trust return value for now.


def test_assign_doctor_to_patient(mock_db):
    success = assign_doctor_to_patient("patient_id", "doctor_id")
    assert success is True


def test_save_admission_service(mock_db):
    # Insert a admission
    pid = Config.mongo_db.Patients.insert_one({"firstName": "AdmitTest"}).inserted_id
    admission_data = {
        "patientId": str(pid),
        "roomNumber": "101",
        "assignedDoctor": "doc@hospital.com",
        "admissionReason": "Test Reason",
        "admissionDate": "2025-01-01"
    }
    inpatient = save_admission(admission_data)
    assert "patientId" in inpatient
    db_inpatient = Config.mongo_db.Inpatients.find_one({"_id": ObjectId(inpatient["_id"])})
    assert db_inpatient is not None


def test_get_admission_summary(mock_db):
    summary = get_admission_summary("admission_id")
    # Returns dummy data in current implementation
    assert "admissionId" in summary


def test_get_available_rooms_service(mock_db):
    # Insert a free room
    Config.mongo_db.Rooms.insert_one({"roomNumber": "300", "occupied": False})
    rooms = get_available_rooms_service()
    assert len(rooms) == 1
    assert rooms[0]["roomNumber"] == "300"


def test_assign_room_service(mock_db):
    Config.mongo_db.Rooms.insert_one({"roomNumber": "400", "occupied": False})
    success = assign_room_service("507f1f77bcf86cd799439011", "400")
    assert success is True
    room = Config.mongo_db.Rooms.find_one({"roomNumber": "400"})
    assert room["occupied"] is True
    assert str(room["patientId"]) == "507f1f77bcf86cd799439011"
    

def test_list_all_inpatients_service(mock_db):
    Config.mongo_db.Inpatients.insert_one({"patientId": ObjectId(), "roomNumber": "500", "assignedDoctor": "doc9@example.com"})
    inpatients = list_all_inpatients_service()
    assert len(inpatients) == 1
    assert inpatients[0]["roomNumber"] == "500"


def test_list_doctor_inpatients_service(mock_db):
    Config.mongo_db.Inpatients.delete_many({})
    Config.mongo_db.Inpatients.insert_one({"patientId": ObjectId(), "assignedDoctor": "doc10@example.com", "roomNumber": "601"})
    inpatients = list_doctor_inpatients_service("doc10@example.com")
    assert len(inpatients) == 1
    assert inpatients[0]["roomNumber"] == "601"


def test_update_inpatient_service(mock_db):
    inp_id = Config.mongo_db.Inpatients.insert_one({"patientId": ObjectId(), "roomNumber": "700"}).inserted_id
    update_inpatient_service(str(inp_id), {"roomNumber": "701"})
    updated = Config.mongo_db.Inpatients.find_one({"_id": inp_id})
    assert updated["roomNumber"] == "701"


def test_admission_endpoints(mock_db, test_client):
    # /api/rooms/rooms/available (assuming admin check is relaxed for now)
    Config.mongo_db.Rooms.insert_one({"roomNumber": "800", "occupied": False})
    response = test_client.get('/api/rooms/rooms/available')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data["rooms"]) == 1

    # /api/rooms/waitlist
    response = test_client.post('/api/rooms/waitlist', json={"patientId": "p123"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Patient added to waitlist"
