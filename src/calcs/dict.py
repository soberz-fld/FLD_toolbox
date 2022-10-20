import json

def format_byte_to_dict(bytelist: bytes) -> dict:
    #TODO: Check if bytes can be translated to dict
    string = bytelist.decode('utf8').replace("'", '"')
    jsoned = json.loads(string)
    return jsoned