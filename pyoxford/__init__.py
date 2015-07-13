import yaml


def speech_api(path_or_client_id="", client_secret=""):
    from pyoxford.speech import SpeechAPI
    api = None
    if path_or_client_id and client_secret:
        api = SpeechAPI(path_or_client_id, client_secret)
    else:
        with open(path_or_client_id, "rb") as f:
            settings = yaml.load(f)
            c_id = settings["speech"]["primary"]
            secret = settings["speech"]["secondary"]
            api = SpeechAPI(c_id, secret)

    return api
