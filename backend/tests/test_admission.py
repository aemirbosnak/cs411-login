import pytest
from bson import ObjectId
from config import Config
from modules.admission.services import admit_patient, update_patient_service, get_patients_service


@pytest.fixture(scope="function")
def setup_patients_and_rooms(mock_db):
    # Add a doctor to assign to patients
    Config.mongo_db.Users.insert_one({
        "_id": ObjectId(),
        "email": "doctor@hospital.com",
        "firstName": "Bob",
        "lastName": "Doctor",
        "password": "hashedpassword",
        "role": "doctor"
    })

    # Insert available rooms
    Config.mongo_db.Rooms.insert_many([
        {
            "_id": ObjectId(),
            "roomNumber": "101",
            "roomType": "Deluxe",
            "occupied": False,
            "assignedDoctor": None,
            "patientId": None,
            "patientFirstName": None,
            "patientLastName": None
        },
        {
            "_id": ObjectId(),
            "roomNumber": "102",
            "roomType": "Standard",
            "occupied": True,  # Already occupied
            "assignedDoctor": "doctorId",
            "patientId": ObjectId(),
            "patientFirstName": "John",
            "patientLastName": "Doe"
        }
    ])


def test_admit_patient_with_room_success(mock_db, setup_patients_and_rooms):
    # Admit a patient into an available room
    data = {
        "firstName": "Alice",
        "lastName": "Brown",
        "dob": "1992-05-14",
        "doctorId": "doctorId",
        "roomNumber": "101",
        "admissionReason": "Routine Checkup"
    }

    result = admit_patient(data)

    assert "error" not in result
    assert result["firstName"] == "Alice"
    assert result["roomNumber"] == "101"

    # Verify the room is now marked as occupied
    room = Config.mongo_db.Rooms.find_one({"roomNumber": "101"})
    assert room["occupied"] is True
    assert room["patientFirstName"] == "Alice"
    assert room["patientLastName"] == "Brown"


def test_admit_patient_room_not_available(mock_db, setup_patients_and_rooms):
    # Attempt to admit a patient into an occupied room
    data = {
        "firstName": "Charlie",
        "lastName": "Smith",
        "dob": "1985-07-22",
        "doctorId": "doctorId",
        "roomNumber": "102",  # This room is already occupied
        "admissionReason": "Observation"
    }

    result = admit_patient(data)

    assert "error" in result
    assert result["error"] == "Room 102 is already occupied."


def test_admit_patient_no_room(mock_db, setup_patients_and_rooms):
    # Admit a patient without specifying a room
    data = {
        "firstName": "Diana",
        "lastName": "Jones",
        "dob": "1990-01-01",
        "doctorId": "doctorId",
        "admissionReason": "General Checkup"
    }

    result = admit_patient(data)

    assert "error" not in result
    assert result["firstName"] == "Diana"
    assert result["roomNumber"] is None

def test_get_patients_service(mock_db, setup_patients_and_rooms):
    # Add a patient assigned to a doctor
    Config.mongo_db.Patients.insert_one({
        "_id": ObjectId(),
        "firstName": "John",
        "lastName": "Doe",
        "doctorId": "doctorId",
        "roomNumber": "101"
    })

    # Call the service to get patients for the doctor
    patients = get_patients_service("doctorId")

    assert len(patients) == 1
    assert patients[0]["firstName"] == "John"


def test_update_patient_service(mock_db, setup_patients_and_rooms):
    # Add a patient to update
    patient_id = Config.mongo_db.Patients.insert_one({
        "_id": ObjectId(),
        "firstName": "Eve",
        "lastName": "Taylor",
        "doctorId": "doctorId"
    }).inserted_id

    # Update the patient's last name
    updated_data = {"lastName": "Johnson"}
    result = update_patient_service(str(patient_id), updated_data)

    assert "error" not in result
    assert result["lastName"] == "Johnson"
