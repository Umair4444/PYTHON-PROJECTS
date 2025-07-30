from datetime import datetime, timedelta
import os
import threading
import time
import uuid
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
import subprocess
import platform
from pydub import AudioSegment

#  Directory to save audio responses
AUDIO_OUTPUT_DIR_GTTS = "./gttsTesting"
AUDIO_OUTPUT_DIR_ELEVEN_LABS = "./elevenLabsTesting"
AUDIO_LIFETIME_SECONDS = 600  # 10 minutes
AUDIO_SUFFIX= "_doctor_response.wav"

# Create output directory if it doesn't exist
os.makedirs(AUDIO_OUTPUT_DIR_GTTS, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_DIR_ELEVEN_LABS, exist_ok=True)

audio_output_path_gtts_manually = os.path.join(
    AUDIO_OUTPUT_DIR_GTTS, f"gtts_testing{uuid.uuid4().hex[:6]}.mp3"
    )
audio_output_path_gtts_autoplay = os.path.join(
    AUDIO_OUTPUT_DIR_GTTS, f"gtts_testing_autoplay{uuid.uuid4().hex[:6]}.mp3"
    )
audio_output_path_elevenLabs_manually = os.path.join(
    AUDIO_OUTPUT_DIR_ELEVEN_LABS, f"gtts_elevenLabs{uuid.uuid4().hex[:6]}.mp3"
    )
audio_output_path_elevenLabs_autoplay = os.path.join(
    AUDIO_OUTPUT_DIR_ELEVEN_LABS, f"gtts_elevenLabs_autoplay{uuid.uuid4().hex[:6]}.mp3"
    )

# Function to clean up old audio files every minute
def cleanup_old_audio_files():
    while True:
        now = datetime.now()
        for directory in [AUDIO_OUTPUT_DIR_GTTS, AUDIO_OUTPUT_DIR_ELEVEN_LABS]:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if now - modified_time > timedelta(seconds=AUDIO_LIFETIME_SECONDS):
                        try:
                            os.remove(filepath)
                            print(f"[CLEANUP] Deleted: {filepath}")
                        except Exception as e:
                            print(f"[CLEANUP ERROR] Could not delete {filepath}: {e}")
        time.sleep(60)  # Run every 60 seconds

# audio have to run manually
def text_to_speech_with_gtts_manually_play(input_text,output_filepath,lang="en"):

    audioobj = gTTS(
        text=input_text,
        slow=False,
        lang=lang
    )
    audioobj.save(output_filepath)

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

# audio have to run manually
def text_to_speech_with_elevenlabs_manually_play(input_text,output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
            text= input_text,
            # voice_id= "9BWtsMINqrJLrRacOk9x", # model_id= "eleven_turbo_v2"
            voice_id= "ZQe5CZNOzWyzPSCn5a3c",
            output_format= "mp3_22050_32",
            model_id= "eleven_turbo_v2"
            # model_id="eleven_multilingu/al_v2"

    )
    elevenlabs.save(audio, output_filepath)


# autoplay audio
def text_to_speech_with_gtts(input_text,output_filepath,lang="en"):

    audioobj = gTTS(
                text=input_text,
                lang=lang,
                slow=False
    )
    audioobj.save(output_filepath)
    
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Convert MP3 to WAV
            wav_path = output_filepath.replace(".mp3", ".wav")
            AudioSegment.from_mp3(output_filepath).export(wav_path, format="wav")
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# autoplay audio
def text_to_speech_with_elevenlabs(input_text,output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.text_to_speech.convert(
        text= input_text,
        voice_id= "9BWtsMINqrJLrRacOk9x", # model_id= "eleven_turbo_v2"
        # voice_id= "ZQe5CZNOzWyzPSCn5a3c",
        output_format= "mp3_22050_32",
        # model_id="eleven_multilingual_v2"
        model_id= "eleven_turbo_v2"

    )
    elevenlabs.save(audio, output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Convert MP3 to WAV
            wav_path = output_filepath.replace(".mp3", ".wav")
            AudioSegment.from_mp3(output_filepath).export(wav_path, format="wav")
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# Start the cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_audio_files, daemon=True)
cleanup_thread.start()


if __name__ == '__main__':
    try:      
        input_text="Hi this is Ai with Umair!, autoplay testing!"
        # text_to_speech_with_gtts()
        text_to_speech_with_gtts(input_text=input_text, output_filepath=audio_output_path_gtts_autoplay)
        # text_to_speech_with_elevenlabs()
        # text_to_speech_with_elevenlabs(input_text=input_text, output_filepath=audio_output_path_elevenLabs_autoplay)
        # text_to_speech_with_elevenlabs("नमस्ते! आज का मौसम सुहाना है।", "output_hindi.mp3")
        # text_to_speech_with_elevenlabs("App kaisa hoon main theek hooon", "output_romanurdu.mp3")
        # text_to_speech_with_elevenlabs("کیا حال ہے؟ میں امید کرتا ہوں کہ آپ خیریت سے ہیں۔", "output_urdu.mp3")

        input_text="Hi this is A-I with Umair! without autoplay"
        text_to_speech_with_gtts_manually_play()
        # text_to_speech_with_gtts_manually_play(input_text=input_text, output_filepath=audio_output_path_gtts_manually)
        # text_to_speech_with_elevenlabs_manually_play() 
        # text_to_speech_with_elevenlabs_manually_play(input_text=input_text, output_filepath=audio_output_path_elevenLabs_manually)

    except Exception as e:
        print(f"An error occurred: {str(e)}")