def speech(path_or_client_id="", client_secret=""):
    from pyoxford.speech_api import Speech
    api = None
    if path_or_client_id and client_secret:
        api = Speech(path_or_client_id, client_secret)
    else:
        key = _read_key(path_or_client_id, "speech")
        api = Speech(key.primary, key.secondary)

    return api

def vision(path_or_key=""):
    from pyoxford.vision_api import Vision
    api = None
    if path_or_key.find(".yaml") > 0:
        key = _read_key(path_or_key, "vision")
        api = Vision(key.primary)
    else:
        api = Vision(path_or_key)

    return api

def _read_key(path, service_name):
    import yaml
    from collections import namedtuple
    ApiKey = namedtuple("ApiKey", ["primary", "secondary"])
    key = ApiKey("", "")
    with open(path, "rb") as f:
        settings = yaml.load(f)
        p = settings[service_name]["primary"]
        s = settings[service_name]["secondary"]
        key = ApiKey(p, s)

    return key
