from flask import Blueprint, request, jsonify
from modules.admission.services import (
    admit_patient,
    update_patient_service,
    get_patients_service,
)

patient_bp = Blueprint("admission", __name__, url_prefix="/api/patient")


@patient_bp.route("/admit", methods=["POST"])
def admit():
    data = request.json
    try:
        patient = admit_patient(data)
        return jsonify({"message": "Patient admitted successfully", "patient": patient}), 201
    except Exception as e:
        return jsonify({"message": f"Error admitting patient: {str(e)}"}), 500


@patient_bp.route("/update/<id>", methods=["PUT"])
def update(id):
    data = request.json
    updated = update_patient_service(id, data)
    return jsonify({"message": "Patient updated", "updatedData": updated}), 200


@patient_bp.route("/list", methods=["GET"])
def get_admitted():
    doctor_id = request.args.get("doctorId")
    patients = get_patients_service(doctor_id)
    return jsonify({"patients": patients}), 200
