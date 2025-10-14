import pyttsx3
from queue import Queue
from threading import Thread
import time

# Initialize TTS engine once globally
engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

# Queue for all texts to speak
speech_queue = Queue()

def speak_text(text: str):
    """Add text to the speech queue."""
    if text.strip():
        speech_queue.put(text)