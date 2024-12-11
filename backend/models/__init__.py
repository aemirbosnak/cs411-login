from bson import ObjectId

def convert_objectid_to_string(document):
    if '_id' in document:
        document['_id'] = str(document['_id'])
    if 'patientId' in document and isinstance(document['patientId'], ObjectId):
        document['patientId'] = str(document['patientId'])
    return document
