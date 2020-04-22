import json
def validate_fields(obj):
    if obj:
        error = {}
        for key in obj:
            if key is 'id':
                pass
            else:
                error.update({key: key + ' should not be empty'})

    raise Exception(json.dumps(error))
