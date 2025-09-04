# import speech_recognition as sr

# recognizer = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Say something...")
#     audio = recognizer.listen(source)

# try:
#     text = recognizer.recognize_google(audio)
#     print("You said:", text)
# except sr.UnknownValueError:
#     print("Could not understand audio")
# except sr.RequestError as e:
#     print(f"Could not request results; {e}")


# import whisper

# model = whisper.load_model("base")  # or "small", "medium", "large"

# # Load and transcribe an audio file
# result = model.transcribe("your_audio.wav")

# print("Transcribed Text:")
# print(result["text"])


# import whisper
# import sounddevice as sd
# from scipy.io.wavfile import write
# import numpy as np

# # === Settings ===
# fs = 44100  # Sample rate
# duration = 5  # Duration in seconds
# output_file = "your_audio.wav"

# # === Record Audio ===
# print("🎙️ Speak now...")
# recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
# sd.wait()
# write(output_file, fs, recording)
# print("✅ Audio saved as", output_file)

# # === Load Whisper Model ===
# model = whisper.load_model(name='large')  # You can use "small", "medium", "large" for better accuracy

# # === Transcribe ===
# result = model.transcribe(output_file)
# print("\n📝 Transcribed Text:")
# print(result["text"])

import whisper

model = whisper.load_model("small")  # or "small", "medium", "large"

# Load and transcribe an audio file
result = model.transcribe("your_audio.wav")

print("Transcribed Text:")
print(result["text"])
