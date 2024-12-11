from flask import Blueprint, request, jsonify
from modules.patient.services import (collect_patient_data, validate_patient_data, admit_patient,
                                      update_patient_data, search_patient, get_admitted_not_in_inpatients)
from utils import check_admin_role

patient_bp = Blueprint('patient', __name__, url_prefix='/api/patient')


@patient_bp.route('/collect', methods=['POST'])
def collect_info():
    data = request.json
    temp_id = collect_patient_data(data)
    return jsonify({"message": "Data collected", "tempDataId": temp_id}), 200


@patient_bp.route('/validate', methods=['POST'])
def validate():
    data = request.json
    result = validate_patient_data(data)
    if not result['valid']:
        return jsonify({"message": "Data invalid", "errors": result['errors']}), 400
    return jsonify({"message": "Data valid"}), 200


@patient_bp.route('/admit', methods=['POST'])
def admit():
    data = request.json
    try:
        patient = admit_patient(data)
        return jsonify({"message": "Patient admitted successfully", "patient": patient}), 201
    except Exception as e:
        return jsonify({"message": f"Error admitting patient: {str(e)}"}), 500


@patient_bp.route('/update/<id>', methods=['PUT'])
def update(id):
    data = request.json
    updated = update_patient_data(id, data)
    return jsonify({"message": "Patient updated", "updatedData": updated}), 200


@patient_bp.route('/admitted', methods=['GET'])
def get_admitted():
    # if not check_admin_role(request):
    #     return jsonify({"message": "Unauthorized"}), 403
    patients = get_admitted_not_in_inpatients()
    return jsonify({"patients": patients}), 200
