# portaudio and ffmpeg and pyaudio
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in environment variables.")

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY=GROQ_API_KEY):

    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    return transcription.text

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred while recording: {e}")

if __name__ == '__main__':
    try:
        stt_model = "whisper-large-v3"
        audio_filepath = "patient_voice_test_for_patient.mp3"      
          
        # Step 1: Record the audio
        record_audio(file_path=audio_filepath)

        # Step 2: Transcribe using Groq
        # transcription = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
        transcription = transcribe_with_groq(stt_model=stt_model, audio_filepath=audio_filepath, GROQ_API_KEY=GROQ_API_KEY)

        # Step 3: Output transcription
        print("\n📝 Transcription:")
        print(transcription)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
