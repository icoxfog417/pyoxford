import os
import unittest
import tests.envs as envs
import pyoxford


class TestSpeech(unittest.TestCase):

    def test_speech(self):
        wavfile = os.path.join(os.path.dirname(__file__), "./data/test_speech.wav")
        text = "welcome to microsoft oxford speech api"
        api = pyoxford.speech(envs.FILE_PATH)

        binary = api.text_to_speech(text)
        with open(wavfile, "wb") as f:
            f.write(binary)

        if os.path.isfile(wavfile):
            recognized = api.speech_to_text(wavfile)
            self.assertEqual(text, recognized)
