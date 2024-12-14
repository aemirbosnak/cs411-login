from flask import Blueprint, request, jsonify
from utils import check_admin_role, check_doctor_role
from modules.admission.services import (search_patient, place_on_waitlist, assign_doctor_to_patient,
                                        save_admission, get_admission_summary, get_available_rooms_service,
                                        assign_room_service, list_all_inpatients_service, list_doctor_inpatients_service, update_inpatient_service)

admission_bp = Blueprint('rooms', __name__, url_prefix='/api/rooms')


@admission_bp.route('/search-patient', methods=['GET'])
def search_patient_endpoint():
    query = request.args.get('name')
    if not query:
        return jsonify({"message": "Missing query parameter"}), 400
    result = search_patient(query)
    if result.get('found'):
        return jsonify({"message": "Patient found", "patientId": result['patientId']}), 200
    else:
        return jsonify({"message": "Patient not found"}), 404


@admission_bp.route('/rooms/available', methods=['GET'])
def get_available_rooms():
    rooms = get_available_rooms_service()
    return jsonify({"rooms": rooms}), 200


@admission_bp.route('/waitlist', methods=['POST'])
def waitlist_patient():
    data = request.json
    patient_id = data.get('patientId')
    if not patient_id:
        return jsonify({"message": "Missing patientId"}), 400
    place_on_waitlist(patient_id)
    return jsonify({"message": "Patient added to waitlist"}), 200


@admission_bp.route('/assign-room', methods=['POST'])
def assign_room_endpoint():
    data = request.json
    patient_id = data.get('patientId')
    room_number = data.get('roomNumber')
    if not patient_id or not room_number:
        return jsonify({"message": "Missing patientId or roomNumber"}), 400
    success = assign_room_service(patient_id, room_number)
    if success:
        return jsonify({"message": "Room assigned"}), 200
    else:
        return jsonify({"message": "No available rooms or room not found"}), 404


@admission_bp.route('/assign-doctor', methods=['POST'])
def assign_doctor_endpoint():
    data = request.json
    patient_id = data.get('patientId')
    doctor_id = data.get('doctorId')
    if not patient_id or not doctor_id:
        return jsonify({"message": "Missing patientId or doctorId"}), 400
    assign_doctor_to_patient(patient_id, doctor_id)
    return jsonify({"message": "Doctor assigned"}), 200


@admission_bp.route('/save', methods=['POST'])
def save_admission_endpoint():
    data = request.json
    try:
        inpatient = save_admission(data)
        return jsonify({"message": "Admission saved", "inpatient": inpatient}), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": f"Error saving rooms: {str(e)}"}), 500


@admission_bp.route('/summary/<admission_id>', methods=['GET'])
def admission_summary(admission_id):
    summary = get_admission_summary(admission_id)
    return jsonify(summary), 200


@admission_bp.route('/inpatient/list', methods=['GET'])
def list_all_inpatients():
    try:
        inpatients = list_all_inpatients_service()
        return jsonify({"inpatients": inpatients}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching inpatients: {str(e)}"}), 500


@admission_bp.route('/inpatient/list-doctor', methods=['GET'])
def list_inpatients_for_doctor():
    doctor_email = request.args.get('doctorEmail')
    if not doctor_email:
        return jsonify({"message": "Missing doctorEmail parameter"}), 400
    try:
        inpatients = list_doctor_inpatients_service(doctor_email)
        return jsonify({"inpatients": inpatients}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching inpatients for doctor: {str(e)}"}), 500


@admission_bp.route('/inpatient/update/<inpatient_id>', methods=['PUT'])
def update_inpatient_endpoint(inpatient_id):
    updates = request.json
    try:
        update_inpatient_service(inpatient_id, updates)
        return jsonify({"message": "Inpatient updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error updating inpatient: {str(e)}"}), 500
