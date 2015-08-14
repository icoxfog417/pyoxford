# pyoxford
Python Client for Microsoft [Project Oxford](https://www.projectoxford.ai/).

## Installation

```
pip install pyoxford
```

And you have to prepare Microsoft Azure account to use each services.

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
* [Computer Vision API](https://dev.projectoxford.ai/docs/services/54ef139a49c3f70a50e79b7d/operations/550a323849c3f70b34ba2f8d)
