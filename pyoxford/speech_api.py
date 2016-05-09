import uuid
import requests
import platform

try:
    from urllib.parse import urlencode 
except ImportError:
    from urllib import urlencode

class Speech():
    HOST = "https://speech.platform.bing.com"
    USER_AGENT = "pyoxford.SpeechAPI"
    UNIQUE_ID = str(uuid.uuid4()).replace("-", "")

    def __init__(self, client_id, client_secret):
        self.instance_id = self.__generate_id()
        self.__token = ""
        self.authorize(client_id, client_secret)

    def authorize(self, client_id, client_secret):
        url = "https://oxford-speech.cloudapp.net//token/issueToken"

        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }

        params = urlencode(
            {"grant_type": "client_credentials",
             "client_id": client_id,
             "client_secret": client_secret,
             "scope": self.HOST}
        )

        response = requests.post(url, data=params, headers=headers)
        if response.ok:
            _body = response.json()
            self.__token = _body["access_token"]
        else:
            response.raise_for_status()

    def text_to_speech(self, text, lang="en-US", female=True):
        template = """
        <speak version='1.0' xml:lang='{0}'>
            <voice xml:lang='{0}' xml:gender='{1}' name='{2}'>
                {3}
            </voice>
        </speak>
        """

        url = self.HOST + "/synthesize"
        headers = {
            "Content-type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
            "Authorization": "Bearer " + self.__token,
            "X-Search-AppId": self.UNIQUE_ID,
            "X-Search-ClientID": self.instance_id,
            "User-Agent": self.USER_AGENT
        }
        name = self.get_name(lang, female)
        data = template.format(lang, "Female" if female else "Male", name, text)

        response = requests.post(url, data=data, headers=headers)

        if response.ok:
            return response.content
        else:
            raise response.raise_for_status()

    def speech_to_text(self, binary_or_path, lang="en-US", samplerate=8000, scenarios="ulm"):
        data = binary_or_path
        if isinstance(binary_or_path, str):
            with open(binary_or_path, "rb") as f:
                data = f.read()

        params = {
            "version": "3.0",
            "appID": "D4D52672-91D7-4C74-8AD8-42B1D98141A5",
            "instanceid": self.instance_id,
            "requestid": self.__generate_id(),
            "format": "json",
            "locale": lang,
            "device.os": platform.system() + " " + platform.release(),
            "scenarios": scenarios,
        }

        url = self.HOST + "/recognize/query?" + urlencode(params)
        headers = {"Content-type": "audio/wav; samplerate={0}".format(samplerate),
                   "Authorization": "Bearer " + self.__token,
                   "X-Search-AppId": self.UNIQUE_ID,
                   "X-Search-ClientID": self.instance_id,
                   "User-Agent": self.USER_AGENT}

        response = requests.post(url, data=data, headers=headers)

        if response.ok:
            result = response.json()["results"][0]
            return result["lexical"]
        else:
            raise response.raise_for_status()


    @classmethod
    def get_name(cls, lang, female):
        template = "Microsoft Server Speech Text to Speech Voice ({0}, {1})"
        person = ""

        if lang == "de-DE":
            person = "Hedda" if female else "Stefan, Apollo"
        elif lang == "en-AU":
            person = "Catherine"
        elif lang == "en-CA":
            person = "Linda"
        elif lang == "en-GB":
            person = "Susan, Apollo" if female else "George, Apollo"
        elif lang == "en-IN":
            person = "Ravi, Apollo"
        elif lang == "en-US":
            person = "ZiraRUS" if female else "BenjaminRUS"
        elif lang == "es-ES":
            person = "Laura, Apollo" if female else "Pablo, Apollo"
        elif lang == "es-MX":
            person = "Raul, Apollo"
        elif lang == "fr-CA":
            person = "Caroline"
        elif lang == "fr-FR":
            person = "Julie, Apollo" if female else "Paul, Apollo"
        elif lang == "it-IT":
            person = "Cosimo, Apollo"
        elif lang == "ja-JP":
            person = "Ayumi, Apollo" if female else "Ichiro, Apollo"
        elif lang == "pt-BR":
            person = "Daniel, Apollo"
        elif lang == "ru-RU":
            person = "Irina, Apollo" if female else "Pavel, Apollo"
        elif lang == "zh-CN":
            person = "Yaoyao, Apollo" if female else "Kangkang, Apollo"
        elif lang == "zh-HK":
            person = "Tracy, Apollo" if female else "Danny, Apollo"
        elif lang == "zh-TW":
            person = "Yating, Apollo" if female else "Zhiwei, Apollo"

        name = template.format(lang, person)
        return name

    @classmethod
    def __generate_id(cls):
        return str(uuid.uuid4()).replace("-", "")
