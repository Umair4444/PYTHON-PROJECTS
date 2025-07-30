import gradio as gr
import os
import uuid
from dotenv import load_dotenv

from brain_of_doctor.groq_ai_model import analyse_image_with_query, encode_image
from voice_of_patient.main import transcribe_with_groq, text_to_speech, translate_to_urdu
from voice_of_doctor.main import text_to_speech_with_elevenlabs

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY is not set in the environment.")

# Refined prompt
system_prompt = (
    "You have to act as a professional doctor. I know you are not, but this is for learning purposes. "
    "With what I see, I think you have... Do you find anything medically wrong in this image? "
    "If you suggest a differential, recommend simple remedies. "
    "No numbers or special characters. Response should be one long paragraph, maximum two sentences. "
    "Always answer like a real doctor to a real patient. "
    "Avoid phrases like 'In the image I see'. Do not respond as an AI or in markdown."
)

def process_inputs(audio_filepath, image_filepath, patient_text=None, translate=False):
    # Step 1: Handle Text or Audio Input
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

    # Step 2: Image + Query
    if image_filepath:
        doctor_response = analyse_image_with_query(
            query=system_prompt + " " + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # Step 3: Generate Voice
    audio_output_path = f"output_{uuid.uuid4().hex[:6]}_doctor_response.mp3"
    text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=audio_output_path)

    # Step 4: Urdu Translation (if checked)
    urdu_response = translate_to_urdu(doctor_response) if translate else ""

    return (
        speech_to_text_output,
        doctor_response,
        urdu_response,
        audio_output_path,
        audio_output_path  # used for download link
    )

# Replay function
def replay_audio(audio_path):
    return audio_path

# Interface
with gr.Blocks(title="🩺AI Doctor with Vision, Voice, and Urdu") as demo:
    gr.Markdown("# 🩺 AI Doctor with Vision and Voice + Urdu")

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Patient Voice")
        image_input = gr.Image(type="filepath", label="🖼️ Upload Medical Image")
        patient_text_input = gr.Textbox(label="✍️ Patient Text (Optional)", placeholder="Or type your symptoms here...")

    translate_checkbox = gr.Checkbox(label="🌐 Translate Doctor's Response to Urdu", value=True)
    submit_btn = gr.Button("💡 Analyze Symptoms")

    speech_output = gr.Textbox(label="🗣️ Transcribed or Typed Symptoms")
    doctor_text = gr.Textbox(label="👨‍⚕️ Doctor's English Response")
    doctor_text_urdu = gr.Textbox(label="🩺 Doctor's Urdu Response")

    audio_output = gr.Audio(label="🔊 Doctor's Voice", interactive=False)
    download_btn = gr.File(label="📥 Download Doctor Audio")

    replay_btn = gr.Button("🔁 Replay Voice")

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input, patient_text_input, translate_checkbox],
        outputs=[speech_output, doctor_text, doctor_text_urdu, audio_output, download_btn]
    )

    replay_btn.click(fn=replay_audio, inputs=[audio_output], outputs=[audio_output])

demo.launch(debug=True)
