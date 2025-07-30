import gradio as gr
import os
import uuid
import threading
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import custom modules (ensure these are available)
from brain_of_doctor.groq_ai_model import analyse_image_with_query, encode_image
from voice_of_patient.main import transcribe_with_groq, translate_to_urdu
from voice_of_doctor.main import text_to_speech_with_elevenlabs, text_to_speech_with_gtts_manually_play

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY is not set.")

# Constants
OUTPUT_DIR = "./outputs"
AUDIO_LIFETIME_SECONDS = 10 * 60  # 10 minutes
os.makedirs(OUTPUT_DIR, exist_ok=True)

# System prompt
system_prompt = """
Start with a warm greeting using the patient's name if mentioned, or offer a general empathetic greeting.
If the patient describes their injury or symptoms, acknowledge and comment on their statement to show understanding and empathy.
You have to act as a professional doctor. I know you are not, but this is for educational and learning purposes only.
With what I see, I think you have... Do you find anything medically wrong in this image?
If you suggest a differential diagnosis, also recommend simple and accessible remedies.
Do not include any numbers, bullet points, or special characters.
Respond in one concise paragraph, no more than two sentences.
Do not introduce yourself as an AI or format your response in markdown.
Avoid phrases like 'In the image I see' — instead, speak naturally like a real doctor would.
Please don’t worry — we’re monitoring everything closely, and you’re responding well. With time and care, things will improve. I have full confidence in you.
"""

# Cleanup thread
def cleanup_old_audio_files():
    while True:
        now = datetime.now()
        for folder in os.listdir(OUTPUT_DIR):
            folder_path = os.path.join(OUTPUT_DIR, folder)
            if os.path.isdir(folder_path):
                modified_time = datetime.fromtimestamp(os.path.getmtime(folder_path))
                if now - modified_time > timedelta(seconds=AUDIO_LIFETIME_SECONDS):
                    try:
                        import shutil
                        shutil.rmtree(folder_path)
                        print(f"[CLEANUP] Deleted old session: {folder_path}")
                    except Exception as e:
                        print(f"[CLEANUP ERROR] Could not delete {folder_path}: {e}")
        time.sleep(60)

threading.Thread(target=cleanup_old_audio_files, daemon=True).start()

def create_session_output_dir(base_dir=OUTPUT_DIR):
    session_id = uuid.uuid4().hex[:8]
    session_path = os.path.join(base_dir, session_id)
    os.makedirs(session_path, exist_ok=True)
    return session_path

# Main processing
def process_inputs(audio_filepath, image_filepath, patient_text=None, audio_choice="Both"):
    session_dir = create_session_output_dir()

    if patient_text and patient_text.strip():
        speech_text = patient_text.strip()
    elif audio_filepath:
        speech_text = transcribe_with_groq(
            GROQ_API_KEY=groq_api_key,
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    else:
        return "No input provided", "", "", None, None, None

    with open(os.path.join(session_dir, "transcription.txt"), "w", encoding="utf-8") as f:
        f.write(speech_text)

    if image_filepath:
        doctor_response = analyse_image_with_query(
            query=system_prompt + " " + speech_text,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for analysis."

    with open(os.path.join(session_dir, "doctor_response.txt"), "w", encoding="utf-8") as f:
        f.write(doctor_response)

    urdu_response = ""
    english_audio_path = None
    urdu_audio_path = None

    if audio_choice in ["English Only", "Both"]:
        english_audio_path = os.path.join(session_dir, "doctor_en.mp3")
        text_to_speech_with_elevenlabs(doctor_response, english_audio_path)

    if audio_choice in ["Urdu Only", "Both"]:
        urdu_response = translate_to_urdu(doctor_response)
        urdu_audio_path = os.path.join(session_dir, "doctor_urdu.mp3")
        with open(os.path.join(session_dir, "urdu_translation.txt"), "w", encoding="utf-8") as f:
            f.write(urdu_response)
        text_to_speech_with_gtts_manually_play(urdu_response, urdu_audio_path, lang="ur")

    # Choose file to expose for download
    download_file = urdu_audio_path or english_audio_path

    return speech_text, doctor_response, urdu_response, english_audio_path, urdu_audio_path, download_file

def replay_audio(audio_path):
    return audio_path if audio_path and os.path.exists(audio_path) else None

# Gradio UI
def launch_gradio():
    with gr.Blocks(title="AI Doctor with Vision and Voice + Urdu") as demo:
        gr.Markdown("# 🩺 AI Doctor with Vision and Voice + Urdu Translation")

        with gr.Row():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎧 Patient Voice")
            image_input = gr.Image(type="filepath", label="🖼️ Upload Medical Image")
            patient_text_input = gr.Textbox(label="✍️ Patient Text (Optional)", placeholder="Or type your symptoms here...")

        audio_lang_choice = gr.Radio(
            choices=["English Only", "Urdu Only", "Both"],
            value="Both",
            label="🎵 Choose Doctor Audio Language"
        )

        submit_btn = gr.Button("💡 Analyze Symptoms")

        # Outputs
        speech_output = gr.Textbox(label="🗣️ Transcribed or Typed Symptoms")
        doctor_text = gr.Textbox(label="👨‍⚕️ Doctor's English Response")
        doctor_text_urdu = gr.Textbox(label="🩺 Doctor's Urdu Response")
        audio_output_english = gr.Audio(label="🔊 Doctor's Voice in English", interactive=False)
        audio_output_urdu = gr.Audio(label="🔊 Doctor's Voice in Urdu", interactive=False)
        download_btn = gr.File(label="📁 Download Doctor Audio")
        replay_btn = gr.Button("🔁 Replay Voice")

        # Bind submit
        submit_btn.click(
            fn=process_inputs,
            inputs=[audio_input, image_input, patient_text_input, audio_lang_choice],
            outputs=[
                speech_output, doctor_text, doctor_text_urdu,
                audio_output_english, audio_output_urdu, download_btn
            ]
        )

        # Replay Urdu and English
        replay_btn.click(fn=replay_audio, inputs=[audio_output_english], outputs=[audio_output_english])
        replay_btn.click(fn=replay_audio, inputs=[audio_output_urdu], outputs=[audio_output_urdu])

    demo.launch(debug=True, share=True)

# Entry point
if __name__ == '__main__':
    launch_gradio()
