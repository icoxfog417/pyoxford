# -*- coding: utf-8 -*-
import unittest
import tests.envs as envs
import pyoxford


class TestTranslator(unittest.TestCase):

    def test_detect(self):
        api = pyoxford.translator(envs.FILE_PATH)
        result = api.detect("I'm testing translator api.")
        self.assertEqual("en", result)

    def test_translate(self):
        api = pyoxford.translator(envs.FILE_PATH)
        result = api.translate("My name is John.", "ja")
        self.assertTrue("私の名前はジョンです。", result)
