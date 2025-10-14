# audio_to_text_engine.py
import speech_recognition as sr

def speak() -> str:
    """Records voice input and converts to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, could not understand your voice.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Could not request results; {e}")
        return ""
