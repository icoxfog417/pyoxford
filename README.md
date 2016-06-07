# pyoxford
Simple Python Client for [Microsoft Cognitive Services](https://www.microsoft.com/cognitive-services).

## Installation

```
pip install pyoxford
```

And you have to prepare Cognitive Service account to use each services.


## Speech APIs

```python
import pyoxford

text = "welcome to microsoft oxford speech api"
api = pyoxford.speech("your_client_id", "your_client_secret")

# text to speech (.wav file)
binary = api.text_to_speech(text)
with open("voice.wav", "wb") as f:
    f.write(binary)

# speech to text
recognized = api.speech_to_text("voice.wav")

if text == recognized:
    print("success!!")
```

see also official document.

* [text to speech](https://www.projectoxford.ai/doc/speech/REST/Output)
* [speech to text](https://www.projectoxford.ai/doc/speech/REST/Recognition)

## Vision APIs

### Analyze

```python
import pyoxford

api = pyoxford.vision("your_primary_key")
result = api.analyze("https://oxfordportal.blob.core.windows.net/vision/Analysis/4.jpg")

for c in result.categories:
    print(c.name)

```

see also official document.

* [Analyze an image](https://www.projectoxford.ai/doc/vision/visual-features)
* [Computer Vision API #Analyze an image](https://dev.projectoxford.ai/docs/services/54ef139a49c3f70a50e79b7d/operations/550a323849c3f70b34ba2f8d)

### OCR

```python
import pyoxford

api = pyoxford.vision("your_primary_key")
result = api.ocr("https://oxfordportal.blob.core.windows.net/vision/OpticalCharacterRecognition/1.jpg")

doc = result.to_document()
for par in doc:
    print("\n".join(par))
```

see also official document.

* [Optical Character Recognition](https://www.projectoxford.ai/doc/vision/OCR)
* [Computer Vision API #OCR](https://dev.projectoxford.ai/docs/services/54ef139a49c3f70a50e79b7d/operations/5527970549c3f723cc5363e4)

## Translator API

[Translator API](https://datamarket.azure.com/dataset/bing/microsofttranslator) is not project oxford's api, but it is very useful to use with speech api and so on.
To use this API, you have to do step1 & step2 of [Get started](http://www.microsoft.com/en-us/translator/getstarted.aspx).

```python
import pyoxford

api = pyoxford.translator("your_client_id", "your_client_secret")
result = api.translate("My name is John.", "ja")

if "私の名前はジョンです。" == result:
    print("Well translated!!")
```
