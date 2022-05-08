import json
import jsonschema


def validateJson(request):
    # schema of the expected json object
    schema = {
        "type": "object",
        "properties": {
            "accounts": {"type": "array"},
            "transactions": {"type": "array"}
        },
        "required": ["accounts", "transactions"]
    }

    # first, ensure that the request is a valid JSON object
    try:
        jsonObj = json.loads(request)
    except ValueError:
        return False

    # next, ensure that the request matches the schema format
    try:
        jsonschema.validate(instance=jsonObj, schema=schema)
    except jsonschema.exceptions.ValidationError:
        return False

    # in no exceptions occurred, the JSON is valid and matches schema
    return jsonObj
