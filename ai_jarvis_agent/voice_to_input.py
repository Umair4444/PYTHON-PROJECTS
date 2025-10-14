import speech_recognition as sr

def record_and_save_text(filename="user_input.txt"):
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Access the default microphone
    with sr.Microphone() as source:
        print("🎤 Calibrating for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        # Configure silence detection
        recognizer.pause_threshold = 5            # seconds of silence to stop listening
        # recognizer.energy_threshold = 300         # lower if silence not detected
        recognizer.dynamic_energy_threshold = False

        print("🎧 Start speaking... (Recording will stop after 5s of silence)")

        try:
            # Listen indefinitely until silence or phrase_time_limit reached
            audio = recognizer.listen(source, phrase_time_limit=120)
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected. Exiting...")
            return

    print("✅ Recording stopped.")

    try:
        # Convert speech to text
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}")

        # Save recognized text to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"💾 Saved to {filename}")
        return text

    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as e:
        print(f"🚫 Speech recognition service error: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    return ""

if __name__ == "__main__":
    record_and_save_text()
