import logging
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

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
    
text = "dont do"
translated_text = translate_to_urdu(text)

if translated_text:
    text_to_speech(translated_text)
