

from elevenlabs import ElevenLabs
import os


ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

# get all voice models
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
# List available voices
voices = client.voices.get_all()
for voice in voices.voices:
    print(f"{voice.name} - {voice.voice_id}")


def get_supported_output_formats():
    """
    Returns a list of supported output_format values for ElevenLabs TTS.
    """
    return [
        "mp3_22050_32",
        "mp3_44100_64",
        "mp3_44100_96",
        "mp3_44100_128",
        "pcm_16000",
        "pcm_22050",
        "pcm_24000",
        "ulaw_8000"
    ]

def is_valid_output_format(format_to_check: str) -> bool:
    """
    Checks whether a given output_format is supported.
    """
    return format_to_check in get_supported_output_formats()

# Usage
formats = get_supported_output_formats()
print("✅ Supported Output Formats:")
for fmt in formats:
    print(f" - {fmt}")

# Validate a format
format_to_test = "mp3_44100_96"
if is_valid_output_format(format_to_test):
    print(f"\n✅ '{format_to_test}' is a valid output format.")
else:
    print(f"\n❌ '{format_to_test}' is NOT a valid output format.")
