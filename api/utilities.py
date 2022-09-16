import json

def handle_requests_response(res):

    jsonRes = {}
    
    if not res:    
        raise Exception("No response received")
    try:
        jsonRes = res.json()
    except json.JSONDecodeError:
        print("Response could not be serialized. Check if record exists.")

    if 'errors' in jsonRes:
        raise Exception(jsonRes['errors'])


    return jsonRes
