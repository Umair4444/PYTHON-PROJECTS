from gtts import gTTS
import subprocess
import platform
from pydub import AudioSegment

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

if __name__ == "__main__":
    text_to_speech_with_gtts("Hello, this is autoplay testing","output_gtts.mp3")
