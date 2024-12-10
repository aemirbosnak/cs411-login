from flask import Blueprint, request, jsonify
from models import add_inpatient, list_inpatients, list_doctor_inpatients

inpatient_bp = Blueprint('inpatient', __name__)

@inpatient_bp.route('/api/inpatient/add', methods=['POST'])
def add_inpatient_entry():
    data = request.json
    required_fields = ['patientId', 'roomNumber', 'assignedDoctor', 'admissionReason', 'admissionDate']

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        inpatient = add_inpatient(data)
        return jsonify({"message": "Inpatient entry created successfully", "inpatient": inpatient}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating inpatient entry: {str(e)}"}), 500


@inpatient_bp.route('/api/inpatient/list', methods=['GET'])
def list_inpatients_for_admin():
    try:
        inpatients = list_inpatients()
        return jsonify({"inpatients": inpatients}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching inpatients: {str(e)}"}), 500


@inpatient_bp.route('/api/inpatient/list-doctor', methods=['GET'])
def list_inpatients_for_doctor():
    doctor_email = request.args.get('doctorEmail')
    if not doctor_email:
        return jsonify({"message": "Missing doctorEmail parameter"}), 400

    try:
        inpatients = list_doctor_inpatients(doctor_email)
        return jsonify({"inpatients": inpatients}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching inpatients for doctor: {str(e)}"}), 500
