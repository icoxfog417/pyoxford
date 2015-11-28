import urllib.parse
from xml.etree import ElementTree
import requests


class Translator(object):
    AUTH_URL = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
    API_ROOT = "http://api.microsofttranslator.com/v2/Http.svc"
    TRANSLATE_URL = "http://api.microsofttranslator.com/v2/Http.svc/Translates"

    def __init__(self, client_id, client_secret):
        self.__token = ""
        self.authorize(client_id, client_secret)

    def authorize(self, client_id, client_secret):
        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }

        params = urllib.parse.urlencode({
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "http://api.microsofttranslator.com"
        })

        resp = requests.post(self.AUTH_URL, data=params, headers=headers)
        if resp.ok:
            _body = resp.json()
            self.__token = _body["access_token"]
        else:
            resp.raise_for_status()

    def detect(self, text):
        params = {
            "text": text
        }
        url = self.API_ROOT + "/Detect?" + urllib.parse.urlencode(params)
        resp = requests.get(url, headers=self.__make_header())
        result = {}
        if resp.ok:
            root = ElementTree.fromstring(resp.content)
            result = root.text
        else:
            resp.raise_for_status()
        return result

    def translate(self, text, lang_to, lang_from=""):
        # language codes
        # https://msdn.microsoft.com/en-us/library/hh456380.aspx
        params = {
            "text": text,
            "to": lang_to
        }

        if lang_from:
            params["from"] = lang_from

        url = self.API_ROOT + "/Translate?" + urllib.parse.urlencode(params)
        resp = requests.get(url, headers=self.__make_header())
        result = {}
        if resp.ok:
            root = ElementTree.fromstring(resp.content)
            result = root.text
        else:
            resp.raise_for_status()
        return result

    def __make_header(self):
        return {
            "Authorization": "Bearer {0}".format(self.__token)
        }
