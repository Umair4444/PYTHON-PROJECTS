# portaudio and ffmpeg and pyaudio
from datetime import datetime
import logging
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

# Load environment variables from .env
load_dotenv()


import time
import shutil
# clean up function to delete files and folder after 5 minutes 
def cleanup_old_patient_dirs(base_dir="./patient", lifetime_seconds=600):
    now = time.time()

    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        if os.path.isdir(folder_path):
            folder_mtime = os.path.getmtime(folder_path)
            folder_age = now - folder_mtime

            if folder_age > lifetime_seconds:
                try:
                    shutil.rmtree(folder_path)
                    logging.info(f"🗑️ Deleted old folder: {folder_path}")
                except Exception as e:
                    logging.error(f"❌ Failed to delete {folder_path}: {e}")


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

def translate_to_urdu(text):
    try:
        translated = GoogleTranslator(source='auto', target='ur').translate(text)
        print(f"📝 Translated Text: {translated}")
        with open("output.txt", "a+", encoding="utf-8") as f:
            f.write(f"📝 Translated Text: {translated}\n")

        return translated
    except Exception as e:
        print(f"❌ Translation Error: {e}")
        return None
    
def text_to_speech(text, lang="ur", output_file="translated_audio.mp3"):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    logging.info(f"Translated audio saved as: {output_file}")
    audio = AudioSegment.from_mp3(output_file)
    play(audio)    

def create_patient_directory(base_dir="./patient", patient_id="default"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    patient_dir = os.path.join(base_dir, f"{patient_id}_{timestamp}")
    os.makedirs(patient_dir, exist_ok=True)
    return patient_dir

if __name__ == '__main__':
    try:
        # Directory to save audio responses, text response in english and translation in urdu 
        # and audio in urdu in one directory of the patient
        # Step 0: Define model and create patient folder
        stt_model = "whisper-large-v3"
        patient_id = "patient001"  # Replace with actual patient name or ID dynamically
        patient_dir = create_patient_directory(patient_id=patient_id)

        audio_filepath = os.path.join(patient_dir, "voice_input.mp3")
        transcription_path = os.path.join(patient_dir, "transcription.txt")
        translation_path = os.path.join(patient_dir, "translation_urdu.txt")
        tts_output_path = os.path.join(patient_dir, "translation_audio.mp3")

        # Step 1: Record audio
        record_audio(file_path=audio_filepath)

        # Step 2: Transcribe using Groq
        transcription = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)

        # Step 3: Save transcription
        print("\n📝 Transcription:", transcription)
        with open(transcription_path, "w", encoding="utf-8") as f:
            f.write(transcription)

        # Step 4: Translate to Urdu
        translated_text = translate_to_urdu(transcription)
        print(f"\n🌍 Translated ({translated_text}):")
        if translated_text:
            with open(translation_path, "w", encoding="utf-8") as f:
                f.write(translated_text)

        # Step 5: Speak translated text and save audio
        if translated_text:
            text_to_speech(translated_text, output_file=tts_output_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # try:
    
    #     stt_model = "whisper-large-v3"
    #     audio_filepath = "patient_voice_test_for_patient.mp3"      
          
    #     # Step 1: Record the audio
    #     record_audio(file_path=audio_filepath)

    #     # Step 2: Transcribe using Groq 
    #     # transcription = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
    #     transcription = transcribe_with_groq(stt_model=stt_model, audio_filepath=audio_filepath, GROQ_API_KEY=GROQ_API_KEY)

    #     # Step 3: Output transcription
    #     print("\n📝 Transcription:",(transcription))

    #     # Translate the text
    #     translated_text = translate_to_urdu(transcription)
    #     print(f"\n🌍 Translated ({translated_text}):")

    #     # Speak the translated text
    #     if translated_text:
    #         text_to_speech(translated_text)

    # except Exception as e:
    #     print(f"An error occurred: {str(e)}")
