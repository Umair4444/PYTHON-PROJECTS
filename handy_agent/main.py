import speech_recognition as sr
import pyttsx3
import pyautogui
import os
from handy_agent import ask_the_agent
from datetime import datetime

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text: str):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("audio", audio)
            command = recognizer.recognize_google(audio).lower()
            print("command", command)
            return command
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
        except sr.RequestError as e:
            print(f"🚫 API error: {e}")
        except sr.WaitTimeoutError:
            print("⏱️ Timed out waiting for speech.")
        except Exception as e:
            print(f"⚠️ Other error: {e}")
        return ""

        
def execute_command(command: str) -> str:
    if "open notepad" in command:
        os.system("start notepad")
        return "Opening Notepad."
    elif "screenshot" in command:
        pyautogui.screenshot("screenshot.png")
        return "Screenshot saved as screenshot.png."
    elif "close notepad" in command:
        os.system("taskkill /im notepad.exe /f")
        return "Closed Notepad."
    elif "open chrome" in command:
        os.system("start chrome")
        return "Opening Chrome browser."
    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down the computer."
    elif "type hello" in command:
        pyautogui.write("Hello!")
        return "Typed Hello!"
    elif "what time is it" in command:
        now = datetime.now().strftime("%I:%M %p")
        return f"It is {now}."

    elif "what day is it" in command:
        day = datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {day}."
    else:
        result = ask_the_agent(command)
        return speak(result)

def run_voice_agent():
    speak("How can I help you?")
    command = listen()
    print(">>>",command)
    if command:
        response = execute_command(command)
        speak(response)
    else:
        speak("Sorry, I didn't hear anything.")

def wake_word_listener():
    speak("Voice assistant is running. Say 'Jarvis' to activate.")
    while True:
        print("Waiting for wake word...")
        phrase = listen()
        if "Jarvis" in phrase.lower():
            speak("Yes?")
            run_voice_agent()
        elif phrase:
            print("Heard something, but not the wake word.")
        else:
            print("No speech detected.")

if __name__ == "__main__":
    wake_word_listener()
