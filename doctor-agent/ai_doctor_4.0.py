import gradio as gr
import os
import uuid
import threading
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

from brain_of_doctor.groq_ai_model import analyse_image_with_query, encode_image
from voice_of_patient.main import transcribe_with_groq, text_to_speech, translate_to_urdu
from voice_of_doctor.main import text_to_speech_with_elevenlabs

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY is not set.")

# Directory to save audio responses
AUDIO_OUTPUT_DIR = "./outputs"
AUDIO_LIFETIME_SECONDS = 600  # 10 minutes
# AUDIO_SUFFIX_1 = "_doctor_response.mp3"
AUDIO_SUFFIX= "_doctor_response.wav"

# Create output directory if it doesn't exist
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

# System prompt to guide the vision model
system_prompt =    """
                    Start with a warm greeting using the patient's name if mentioned, or offer a general empathetic greeting.
                    If the patient describes their injury or symptoms, acknowledge and comment on their statement to show understanding and empathy.
                    You have to act as a professional doctor. I know you are not, but this is for educational and learning purposes only.
                    With what I see, I think you have... Do you find anything medically wrong in this image?
                    If you suggest a differential diagnosis, also recommend simple and accessible remedies.
                    Do not include any numbers, bullet points, or special characters.
                    Respond in one concise paragraph, no more than two sentences.
                    Do not introduce yourself as an AI or format your response in markdown.
                    Avoid phrases like 'In the image I see' — instead, speak naturally like a real doctor would.
                    End with reassurance: say 'Don’t worry, everything will be alright. You are a strong person, and I know it.
                    """
    

# Function to clean up old audio files every minute
def cleanup_old_audio_files():
    while True:
        now = datetime.now()
        for file in os.listdir(AUDIO_OUTPUT_DIR):
            if file.endswith(AUDIO_SUFFIX):
                file_path = os.path.join(AUDIO_OUTPUT_DIR, file)
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if now - file_time > timedelta(seconds=AUDIO_LIFETIME_SECONDS):
                    try:
                        os.remove(file_path)
                        print(f"[CLEANUP] Deleted old audio file: {file}")
                    except Exception as e:
                        print(f"[CLEANUP ERROR] Could not delete {file}: {e}")
        time.sleep(60)  # Run every 60 seconds

# Start background thread for cleanup
cleanup_thread = threading.Thread(target=cleanup_old_audio_files, daemon=True)
cleanup_thread.start()

# Main processing function for Gradio
def process_inputs(audio_filepath, image_filepath, patient_text=None, translate=False):
    # Step 1: Handle text input or transcribe audio
    if patient_text and patient_text.strip():
        speech_to_text_output = patient_text.strip()
    elif audio_filepath:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=groq_api_key,
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    else:
        return "No input", "Please provide either voice or typed symptoms.", "", None, None

    # Step 2: Analyze image + query model
    if image_filepath:
        doctor_response = analyse_image_with_query(
            query=system_prompt + " " + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # Step 3: Generate audio file from response
    audio_output_path = os.path.join(
        AUDIO_OUTPUT_DIR, f"{uuid.uuid4().hex[:6]}_doctor_response.mp3"
    )
    text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=audio_output_path)

    # Step 4: Translate to Urdu if checkbox is enabled
    urdu_response = translate_to_urdu(doctor_response) if translate else ""

    # Step 5: Return results to UI (5 outputs)
    return (
        speech_to_text_output,
        doctor_response,
        urdu_response,
        audio_output_path,
        audio_output_path # Clean download name
    )

# Replays the same audio
def replay_audio(audio_path):
    return audio_path

# Gradio UI
with gr.Blocks(title="AI Doctor with Vision and Voice + Urdu") as demo:
    gr.Markdown("# 🩺 AI Doctor with Vision and Voice + Urdu Translation")

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Patient Voice")
        image_input = gr.Image(type="filepath", label="🖼️ Upload Medical Image")
        patient_text_input = gr.Textbox(label="✍️ Patient Text (Optional)", placeholder="Or type your symptoms here...")

    translate_checkbox = gr.Checkbox(label="🌐 Translate Doctor's Response to Urdu", value=True)
    submit_btn = gr.Button("💡 Analyze Symptoms")

    # Output fields
    speech_output = gr.Textbox(label="🗣️ Transcribed or Typed Symptoms")
    doctor_text = gr.Textbox(label="👨‍⚕️ Doctor's English Response")
    doctor_text_urdu = gr.Textbox(label="🩺 Doctor's Urdu Response")
    audio_output = gr.Audio(label="🔊 Doctor's Voice", interactive=False)
    download_btn = gr.File(label="📥 Download Doctor Audio")
    replay_btn = gr.Button("🔁 Replay Voice")

    # Bind buttons
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input, patient_text_input, translate_checkbox],
        outputs=[speech_output, doctor_text, doctor_text_urdu, audio_output, download_btn]
    )

    replay_btn.click(fn=replay_audio, inputs=[audio_output], outputs=[audio_output])

# Launch the app
demo.launch(debug=True)
