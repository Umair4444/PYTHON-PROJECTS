import streamlit as st
from gtts import gTTS
import os

def main():

# Streamlit UI
    st.title("🗣️ Text-to-Speech App")

    # Text Input
    text_input = st.text_area("Enter text to convert to speech:")

    # Language selection
    language = st.selectbox("Select Language:", ["en", "es", "fr", "de", "hi","ur"])

    # Button to generate speech
    if st.button("Convert to Speech"):
        if text_input.strip():
            # Generate speech
            tts = gTTS(text=text_input, lang=language)
            speech_file = "speech.mp3"
            tts.save(speech_file)

            # Play audio in Streamlit
            st.audio(speech_file, format="audio/mp3")
            
            st.success("✅ Speech generated successfully!")
        else:
            st.warning("⚠️ Please enter text before clicking 'Convert to Speech'.")



if __name__ == "__main__":
    main()
