# agent_voice_output.py
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

def speak_text(text: str):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()
