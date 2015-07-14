# pyoxford
Python Client for Microsoft [Project Oxford](https://www.projectoxford.ai/).

## Speech APIs

```python
import pyoxford

text = "welcome to microsoft oxford speech api"
api = pyoxford.speech_api("your_client_id", "your_client_secret")

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
