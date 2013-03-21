import simplejson as json


def lower_keys(item):
    if isinstance(item, list):
        return [lower_keys(val) for val in item]
    if isinstance(item, dict):
        return dict((key.lower(), lower_keys(val)) for key, val in item.iteritems())
    return item


def find_key(key, item):
    for k, v in item.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find_key(key, v):
                if isinstance(v, dict):
                    for k, v in item.iteritems():
                        if k == key:
                            yield v
        elif isinstance(v, list):
            for d in v:
                for result in find_key(key, d):
                    yield result

