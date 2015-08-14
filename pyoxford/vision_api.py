from enum import Enum
import json
from collections import namedtuple
import urllib.parse
import requests


class VisualFeatures(Enum):
    ImageType = "ImageType"
    Color = "Color"
    Faces = "Faces"
    Adult = "Adult"
    Categories = "Categories"
    All = "All"


class Vision():
    ANALYZE_URL = "https://api.projectoxford.ai/vision/v1/analyses"

    def __init__(self, ocp_apim_key):
        self.ocp_apim_key = ocp_apim_key

    def analyze(self, image_url_or_binary, visual_features=VisualFeatures.All):
        """
        analyze the image. see also below link.
        https://dev.projectoxford.ai/docs/services/54ef139a49c3f70a50e79b7d/operations/550a323849c3f70b34ba2f8d
        :param visual_features:
        :return:
        """

        headers = {
            "Ocp-Apim-Subscription-Key": self.ocp_apim_key
        }
        params = {
            "visualFeatures": visual_features.value
        }
        data = {}

        if isinstance(image_url_or_binary, str):
            headers["Content-type"] = "application/json"
            data = json.dumps({"Url": image_url_or_binary})
        else:
            headers["Content-type"] = "application/octet-stream"
            data = image_url_or_binary

        url = self.ANALYZE_URL + "?" + urllib.parse.urlencode(params)
        response = requests.post(url, headers=headers, data=data)

        resp = {}
        if response.ok:
            resp = response.json()
            analyzed = AnalyzeResult(resp)
        else:
            response.raise_for_status()

        return analyzed


class AnalyzeResult():
    _category_fields = ["name", "score"]
    _adult_fields = ["isAdultContent", "isRacyContent", "adultScore", "racyScore"]
    _metadata_fields = ["width", "height", "format"]
    _face_fields = ["age", "gender", "faceRectangle"]
    _color_fields = ["dominantColorForeground", "dominantColorBackground", "dominantColors", "accentColor", "isBWImg"]
    _image_type_fields = ["clipArtType", "lineDrawingType"]

    Category = namedtuple("Category", _category_fields)
    Adult = namedtuple("Adult", _adult_fields)
    Metadata = namedtuple("Metadata", _metadata_fields)
    Face = namedtuple("Face", _face_fields)
    Color = namedtuple("Color", _color_fields)
    ImageType = namedtuple("ImageType", _image_type_fields)

    def __init__(self, analyzed):
        self.request_id = -1
        self.categories = []
        self.adult = None
        self.metadata = None
        self.faces = []
        self.color = None
        self.image_type = None

        if "requestId" in analyzed:
            self.request_id = analyzed["requestId"]

        self._load_categories(analyzed)
        self._load_adult(analyzed)
        self._load_metadata(analyzed)
        self._load_faces(analyzed)
        self._load_color(analyzed)
        self._load_image_type(analyzed)

    def _load_categories(self, analyzed):
        if "categories" in analyzed:
            self.categories = [self.__make_obj(self.Category, self._category_fields, c) for c in analyzed["categories"]]

    def _load_adult(self, analyzed):
        if "adult" in analyzed:
            self.adult = self.__make_obj(self.Adult, self._adult_fields, analyzed["adult"])

    def _load_metadata(self, analyzed):
        if "metadata" in analyzed:
            self.metadata = self.__make_obj(self.Metadata, self._metadata_fields, analyzed["metadata"])

    def _load_faces(self, analyzed):
        if "faces" in analyzed:
            self.faces = [self.__make_obj(self.Face, self._face_fields, f) for f in analyzed["faces"]]

    def _load_color(self, analyzed):
        if "color" in analyzed:
            self.color = self.__make_obj(self.Color, self._color_fields, analyzed["color"])

    def _load_image_type(self, analyzed):
        if "imageType" in analyzed:
            self.image_type = self.__make_obj(self.ImageType, self._image_type_fields, analyzed["imageType"])

    def __make_obj(self, class_type, fields, dict_data):
        return class_type._make(self.__dict_to_list(dict_data, fields))

    def __dict_to_list(self, dict_data, fields):
        result = []
        for f in fields:
            if f in dict_data:
                result.append(dict_data[f])
            else:
                result.append(None)
        return result
