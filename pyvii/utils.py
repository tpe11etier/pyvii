import simplejson as json


def suds_to_json(suds_object):
    # Work in progress and may ditch it.
    json_dict = {}
    suds_object = suds_object
    for suds_object in suds_object:
        if isinstance(suds_object, tuple):
            key, value = suds_object
            if value and isinstance(key, str):
                for inner_key in value:
                    if isinstance(inner_key, tuple):
                        inner_key, inner_value = inner_key
                        json_dict[key] = inner_value
                    else:
                        json_dict[key] = value
    return json.dumps(json_dict, indent=4)
