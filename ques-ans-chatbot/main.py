import os
import chainlit as cl
import google.generativeai as ai
from dotenv import load_dotenv

# This is stateful chatbot on chainlit
load_dotenv()

gemini_apikey = os.environ["GEMINI_API_KEY"]
ai.configure(api_key=gemini_apikey)

generate_config = ai.GenerationConfig(
    temperature=0.9,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    max_output_tokens=256  # Increased for better responses
)

model = ai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Use the latest version
    generation_config=generate_config
)

# Initialize chat session globally
chat_session = model.start_chat(history=[])

@cl.on_chat_start
async def handle_start_chat():
    """Reset chat session when a new session starts"""
    global chat_session
    chat_session = model.start_chat(history=[])
    await cl.Message(content="Hi! How can I help?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    """Handles user messages and maintains chat history"""

    global chat_session
    question = message.content

    # Generate response with chat history as context
    response = chat_session.send_message(question)

    # Extract response text
    response_text = response.text if hasattr(response, "text") else ""

    # Send response back to user
    await cl.Message(content=response_text).send()
