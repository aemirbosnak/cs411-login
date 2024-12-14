import pytest
import datetime
from config import Config
from bson import ObjectId

from models.patient_model import add_patient, list_patients, list_admitted_patients_not_in_inpatients
from models.admission_model import add_inpatient, update_inpatient, list_inpatients, list_doctor_inpatients


def test_add_patient(mock_db):
    patient_data = {
        "firstName": "John",
        "lastName": "Doe",
        "dob": "1990-01-01",
        "gender": "male",
        "address": "123 Main St",
        "contactNumber": "555-1234",
        "emergencyContact": "Jane Doe",
        "doctorId": "doctor@hospital.com",
        "complaint": "Headache",
        "severity": "moderate"
    }
    patient = add_patient(patient_data)
    assert "_id" in patient
    assert patient["firstName"] == "John"
    # Verify admission in DB
    db_patient = Config.mongo_db.Patients.find_one({"_id": ObjectId(patient["_id"])})
    assert db_patient["doctorId"] == "doctor@hospital.com"


def test_list_patients(mock_db):
    # Insert a admission for a specific doctor
    Config.mongo_db.Patients.insert_one({
        "firstName": "Alice",
        "lastName": "Smith",
        "doctorId": "doc@example.com"
    })

    patients = list_patients("doc@example.com")
    assert len(patients) == 1
    assert patients[0]["firstName"] == "Alice"


def test_list_admitted_not_in_inpatients(mock_db):
    # Insert two patients
    p1 = Config.mongo_db.Patients.insert_one({"firstName": "Bob", "doctorId": "doc1@example.com"}).inserted_id
    p2 = Config.mongo_db.Patients.insert_one({"firstName": "Charlie", "doctorId": "doc2@example.com"}).inserted_id

    # Make one of them inpatient
    Config.mongo_db.Inpatients.insert_one({"patientId": p1})

    admitted = list_admitted_patients_not_in_inpatients()
    assert len(admitted) == 1
    assert admitted[0]["firstName"] == "Charlie"


def test_add_inpatient(mock_db):
    # Insert a admission
    patient_id = Config.mongo_db.Patients.insert_one({"firstName": "Daisy", "doctorId": "doc3@example.com"}).inserted_id
    inpatient_data = {
        "patientId": str(patient_id),
        "roomNumber": "101",
        "assignedDoctor": "doc3@example.com",
        "admissionReason": "Surgery",
        "admissionDate": "2024-12-10"
    }
    inpatient = add_inpatient(inpatient_data)
    assert "patientId" in inpatient
    assert inpatient["roomNumber"] == "101"
    # Check in DB
    db_inpatient = Config.mongo_db.Inpatients.find_one({"_id": ObjectId(inpatient["_id"])})
    assert db_inpatient["assignedDoctor"] == "doc3@example.com"


def test_list_inpatients(mock_db):
    # Clear and add a known inpatient
    Config.mongo_db.Inpatients.delete_many({})
    pid = ObjectId()
    Config.mongo_db.Inpatients.insert_one({
        "patientId": pid,
        "roomNumber": "202",
        "assignedDoctor": "doc4@example.com",
        "admissionReason": "Checkup",
        "admissionDate": "2024-12-11"
    })

    inpatients = list_inpatients()
    assert len(inpatients) == 1
    assert inpatients[0]["roomNumber"] == "202"


def test_list_doctor_inpatients(mock_db):
    # Clear and add two inpatients for different doctors
    Config.mongo_db.Inpatients.delete_many({})
    Config.mongo_db.Inpatients.insert_one({
        "patientId": ObjectId(),
        "roomNumber": "303",
        "assignedDoctor": "doc5@example.com",
        "admissionReason": "Flu",
        "admissionDate": "2024-12-12"
    })
    Config.mongo_db.Inpatients.insert_one({
        "patientId": ObjectId(),
        "roomNumber": "404",
        "assignedDoctor": "doc6@example.com",
        "admissionReason": "Injury",
        "admissionDate": "2024-12-13"
    })

    doc5_inpatients = list_doctor_inpatients("doc5@example.com")
    assert len(doc5_inpatients) == 1
    assert doc5_inpatients[0]["roomNumber"] == "303"


def test_update_inpatient(mock_db):
    # Add an inpatient, then update
    inp_id = Config.mongo_db.Inpatients.insert_one({
        "patientId": ObjectId(),
        "roomNumber": "505",
        "assignedDoctor": "doc7@example.com",
        "admissionReason": "Routine",
        "admissionDate": "2024-12-14"
    }).inserted_id

    update_inpatient(str(inp_id), {"roomNumber": "606", "operationDetails": "X-Ray"})
    updated = Config.mongo_db.Inpatients.find_one({"_id": inp_id})
    assert updated["roomNumber"] == "606"
    assert updated["operationDetails"] == "X-Ray"
