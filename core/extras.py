import json
def validate_fields(obj):
    if obj:
        error = {}
        for key in obj:
            if key is 'id' or key is 'creation_date':
                pass
            else:
                if obj[key] is None or obj[key] is "":
                    error.update({key: key.capitalize() + ' should not be empty!'})
                else:
                    pass

    if not error:
        return True
    else:
        raise Exception(json.dumps(error))
