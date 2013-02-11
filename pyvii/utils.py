import simplejson as json


def lower_keys(item):
    if isinstance(item, list):
        return [lower_keys(val) for val in item]
    if isinstance(item, dict):
        return dict((key.lower(), lower_keys(val)) for key, val in item.iteritems())
    return item


def find_key(key, value):
    for k, v in value.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find_key(key, v):
                if isinstance(v, dict):
                    for k, v in value.iteritems():
                        if k == key:
                            yield v
        elif isinstance(v, list):
            for d in v:
                for result in find_key(key, d):
                    yield result


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
