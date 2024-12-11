# backend/routes/routes.py
from flask import Blueprint, request, jsonify
from models.admission_model import add_inpatient, list_inpatients, list_doctor_inpatients, update_inpatient
from utils import check_admin_role, check_doctor_role

admission_bp = Blueprint('admission', __name__)


@admission_bp.route('/api/inpatient/add', methods=['POST'])
def add_inpatient_entry():
    # Admin only
    if not check_admin_role(request):
        return jsonify({"message": "Unauthorized"}), 403

    data = request.json
    required_fields = ['patientId', 'roomNumber', 'assignedDoctor', 'admissionReason', 'admissionDate']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        inpatient = add_inpatient(data)
        return jsonify({"message": "Inpatient entry created successfully", "inpatient": inpatient}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating inpatient entry: {str(e)}"}), 500


@admission_bp.route('/api/inpatient/list', methods=['GET'])
def list_all_inpatients():
    # Admin only
    if not check_admin_role(request):
        return jsonify({"message": "Unauthorized"}), 403
    try:
        inpatients = list_inpatients()
        return jsonify({"inpatients": inpatients}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching inpatients: {str(e)}"}), 500


@admission_bp.route('/api/inpatient/list-doctor', methods=['GET'])
def list_inpatients_for_doctor():
    # Doctor only
    if not check_doctor_role(request):
        return jsonify({"message": "Unauthorized"}), 403
    doctor_email = request.args.get('doctorEmail')
    if not doctor_email:
        return jsonify({"message": "Missing doctorEmail parameter"}), 400

    try:
        inpatients = list_doctor_inpatients(doctor_email)
        return jsonify({"inpatients": inpatients}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching inpatients for doctor: {str(e)}"}), 500


@admission_bp.route('/api/inpatient/update/<inpatient_id>', methods=['PUT'])
def update_inpatient(inpatient_id):
    # Admin only
    if not check_admin_role(request):
        return jsonify({"message": "Unauthorized"}), 403

    updates = request.json
    try:
        update_inpatient(inpatient_id, updates)
        return jsonify({"message": "Inpatient updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error updating inpatient: {str(e)}"}), 500
