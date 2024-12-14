from models.patient_model import add_patient, list_patients

# Temporary storage for partial data, for demo only
TEMP_DATA = {}


def admit_patient(data):
    # Called after validate ensures data is good
    return add_patient(data)


def update_patient(patient_id, updated_data):
    # Here you would implement admission update logic by:
    # - Finding admission by patient_id
    # - Merging updated_data with existing fields
    # - Calling a model function to update in DB (not implemented above)
    # For demo, just return updated_data
    # TODO: Implement actual update in `patient_model.py` if needed
    return updated_data


def get_patients():
    return list_patients()

