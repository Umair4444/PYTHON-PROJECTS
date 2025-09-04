<!-- SPEAKING FUNCTION -->

# Initialize
```python

import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 180)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()
```