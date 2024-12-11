from models.patient_model import add_patient, list_patients, list_admitted_patients_not_in_inpatients

# Temporary storage for partial data, for demo only
TEMP_DATA = {}

def collect_patient_data(data):
    # Generate a tempDataId to store partial info
    temp_id = str(len(TEMP_DATA) + 1)
    TEMP_DATA[temp_id] = data
    return temp_id


def validate_patient_data(data):
    required_fields = ['firstName', 'lastName', 'dob', 'address', 'doctorId']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return {"valid": False, "errors": [f"Missing fields: {', '.join(missing)}"]}
    # Add more complex validation here (e.g., date formats)
    return {"valid": True, "errors": []}


def admit_patient(data):
    # Called after validate ensures data is good
    return add_patient(data)


def update_patient_data(patient_id, updated_data):
    # Here you would implement patient update logic by:
    # - Finding patient by patient_id
    # - Merging updated_data with existing fields
    # - Calling a model function to update in DB (not implemented above)
    # For demo, just return updated_data
    # TODO: Implement actual update in `patient_model.py` if needed
    return updated_data


def search_patient(query):
    # This could search patients by name or ID
    # For demo, just return a mock result
    # TODO: Implement searching in patient_model
    if query == "John Doe":
        return [{"_id": "some_id", "firstName": "John", "lastName": "Doe"}]
    return []


def get_admitted_not_in_inpatients():
    return list_admitted_patients_not_in_inpatients()
