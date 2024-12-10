from flask import Blueprint, request, jsonify
from models import add_patient, list_patients, list_admitted_patients_not_in_inpatients

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


@patient_bp.route('/api/patient/admitted', methods=['GET'])
def get_admitted_not_in_inpatients():
    # Check if user is admin
    # Assume you have a function `check_admin_role()` that verifies the role from the token
    # Pseudocode:
    # if not check_admin_role(request):
    #     return jsonify({"message": "Unauthorized"}), 403

    try:
        patients = list_admitted_patients_not_in_inpatients()
        return jsonify({"patients": patients}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching admitted patients: {str(e)}"}), 500