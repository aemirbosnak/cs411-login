from flask import Blueprint, request, jsonify
from models import add_patient, list_patients

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/api/patient/admit', methods=['POST'])
def admit_patient():
    data = request.json
    required_fields = ['firstName', 'lastName', 'dob', 'address', 'doctorId']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        new_patient = add_patient(data)
        return jsonify({"message": "Patient admitted successfully", "patient": new_patient}), 201
    except Exception as e:
        return jsonify({"message": f"Error admitting patient: {str(e)}"}), 500


@patient_bp.route('/api/patient/list', methods=['GET'])
def get_patients():
    doctor_id = request.args.get('doctorId')

    if not doctor_id:
        return jsonify({"message": "Missing doctorId parameter"}), 400

    try:
        patients = list_patients(doctor_id)
        return jsonify({"patients": patients}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching patients: {str(e)}"}), 500
