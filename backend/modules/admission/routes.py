from flask import Blueprint, request, jsonify
from modules.patient.services import (admit_patient, update_patient, get_patients)
from utils import check_admin_role

patient_bp = Blueprint('admission', __name__, url_prefix='/api/patient')


@patient_bp.route('/admit', methods=['POST'])
def admit():
    data = request.json
    try:
        patient = admit_patient(data)
        return jsonify({"message": "Patient admitted successfully", "admission": patient}), 201
    except Exception as e:
        return jsonify({"message": f"Error admitting admission: {str(e)}"}), 500


@patient_bp.route('/update/<id>', methods=['PUT'])
def update(id):
    data = request.json
    updated = update_patient(id, data)
    return jsonify({"message": "Patient updated", "updatedData": updated}), 200


@patient_bp.route('/list', methods=['GET'])
def get_admitted():
    if not check_admin_role(request):
            return jsonify({"message": "Unauthorized"}), 403
    patients = get_patients()
    return jsonify({"patients": patients}), 200
