import os
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
import subprocess
import platform
from pydub import AudioSegment

# audio have to run manually
def text_to_speech_with_gtts_manually_play(input_text,output_filepath):
    language="en"

    audioobj = gTTS(
        text=input_text,
        slow=False,
        lang=language
    )
    audioobj.save(output_filepath)

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

# audio have to run manually
def text_to_speech_with_elevenlabs_manually_play(input_text,output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
            text= input_text,
            voice_id= "9BWtsMINqrJLrRacOk9x",
            output_format= "mp3_22050_32",
            model_id= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)


# autoplay audio
def text_to_speech_with_gtts(input_text,output_filepath):
    language="en"

    audioobj = gTTS(
                text=input_text,
                lang=language,
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
        voice_id= "9BWtsMINqrJLrRacOk9x",
        output_format= "mp3_22050_32",
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


if __name__ == '__main__':
    try:      
        input_text="Hi this is Ai with Umair!, autoplay testing!"
        # text_to_speech_with_gtts()
        text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")
        # text_to_speech_with_elevenlabs()
        # text_to_speech_with_elevenlabs(input_text=input_text, output_filepath="elevenlabs_testing_autoplay.mp3")

        input_text="Hi this is A-I with Umair! without autoplay"
        # text_to_speech_with_gtts_manually_play()
        # text_to_speech_with_gtts_manually_play(input_text=input_text, output_filepath="gtts_testing.mp3")
        # text_to_speech_with_elevenlabs_manually_play() 
        # text_to_speech_with_elevenlabs_manually_play(input_text=input_text, output_filepath="elevenlabs_testing.mp3")

    except Exception as e:
        print(f"An error occurred: {str(e)}")