import os
import unittest
import tests.envs as envs
import pyoxford


class TestVision(unittest.TestCase):

    def test_vision_analysis_by_image_url(self):
        api = pyoxford.vision(envs.FILE_PATH)
        result = api.analyze("https://oxfordportal.blob.core.windows.net/vision/Analysis/4.jpg")
        self.assertTrue(result.request_id)
        self.assertTrue(result.adult.isRacyContent)
        for c in result.categories:
            print(c.name)

    def test_vision_analysis_by_image(self):
        api = pyoxford.vision(envs.FILE_PATH)
        path = os.path.join(os.path.dirname(__file__), "./data/test_image.jpg")
        with open(path, "rb") as f:
            image = f.read()
            result = api.analyze(image)
            self.assertTrue(result.request_id)
            self.assertEqual("jpeg", result.metadata.format.lower())

    def test_vision_ocr(self):
        api = pyoxford.vision(envs.FILE_PATH)
        result = api.ocr("https://oxfordportal.blob.core.windows.net/vision/OpticalCharacterRecognition/1.jpg")
        self.assertTrue(result.language)
        self.assertTrue(len(result.regions) > 0)
        d = result.to_document()
        for p in d:
            print("\n".join(p))
