
def validate_fields(fields):

    validated_output = {}

    for key, value in fields.items():

        if value is None:
            validated_output[key] = "Not Found"

        elif isinstance(value, list) and len(value) == 0:
            validated_output[key] = "Not Found"

        else:
            validated_output[key] = value

    return validated_output
