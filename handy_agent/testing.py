import speech_recognition as sr
import pyttsx3
import requests
import json
import re
import os
import subprocess
import webbrowser
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play


# Initialize
engine = pyttsx3.init()
engine.setProperty("rate", 180)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def speak():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        audio = recognizer.listen(source)

        
        return audio

    
    print("Assistant:", audio)
    engine.say(audio)
    engine.runAndWait()

speak()

# def listen():
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         print("🎤 Listening...")
#         audio = recognizer.listen(source)
#     try:
#         print("🔍 Recognizing...")
#         aud = audio.get_wav_data()
#         audio_segment = AudioSegment.from_wav(BytesIO(aud))
#         audio_segment.export('file_path.mp3', format="mp3", bitrate="128k")

#         # query = recognizer.recognize_google(audio)
#         with open("file_path.mp3", "rb") as audio_file:
#             read = audio_file.readlines()
#     except:
#         return None
    
# listen()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        print("🔍 Recognizing...")
        aud = audio.get_wav_data()
        audio_segment = AudioSegment.from_wav(BytesIO(aud))
        audio_segment.export('file_path.mp3', format="mp3", bitrate="128k")
        with open("file_path.mp3","rb+") as file:
            recognizer.record('new.mp3')
            query = recognizer.recognize_bing(file)
            print("You said:", query)
            return query       
    except:
        return None
    
listen()

def callback(recognizer, audio):
    try:
        command = recognizer(audio)
        if command.lower() == "stop":
            engine.stop()
            print("Speech stopped by user")
    except:
        pass

stop_listening = recognizer.listen_in_background(microphone, callback)

def speak(text, allow_interruption=False):
    if allow_interruption:
        stop_listening(wait_for_stop=False)
        stop_listening_new = recognizer.listen_in_background(microphone, callback)
    engine.say(text)
    engine.runAndWait()
    if allow_interruption:
        stop_listening_new(wait_for_stop=False)

# speak('hi')


