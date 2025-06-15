import gradio as gr
import os
from dotenv import load_dotenv

from brain_of_doctor.groq_ai_model import analyse_image_with_query, encode_image
from voice_of_patient.main import transcribe_with_groq
from voice_of_doctor.main import text_to_speech_with_elevenlabs

load_dotenv()

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath, patient_text=None):
    # Prefer typed text if available
    if patient_text and patient_text.strip():
        speech_to_text_output = patient_text.strip()
    else:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

    if image_filepath:
        doctor_response = analyse_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    audio_output_path = "final.mp3"
    text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=audio_output_path)

    return speech_to_text_output, doctor_response, audio_output_path

# Replay function just returns the same audio path
def replay_audio(audio_path):
    return audio_path

# Interface using Blocks
with gr.Blocks(title="AI Doctor with Vision and Voice") as demo:
    gr.Markdown("# 🩺 AI Doctor with Vision and Voice")

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Patient Voice")
        image_input = gr.Image(type="filepath", label="🖼️ Upload Medical Image")
        patient_text_input = gr.Textbox(label="✍️ Patient Text (Optional)", placeholder="Or type your symptoms here...")

    submit_btn = gr.Button("💡 Analyze")
    
    speech_output = gr.Textbox(label="🗣️ Transcribed Text")
    doctor_text = gr.Textbox(label="👨‍⚕️ Doctor's Response")

    audio_output = gr.Audio(label="🔊 Doctor's Voice Response", interactive=False)
    replay_btn = gr.Button("🔁 Replay Doctor Voice")

    submit_btn.click(fn=process_inputs,
                     inputs=[audio_input, image_input, patient_text_input],
                     outputs=[speech_output, doctor_text, audio_output])

    replay_btn.click(fn=replay_audio,
                     inputs=[audio_output],
                     outputs=[audio_output])

demo.launch(debug=True)
