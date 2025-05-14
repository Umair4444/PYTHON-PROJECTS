import os
import chainlit as cl
import google.generativeai as ai
from dotenv import load_dotenv

# This is a stateless chatbot on chainlit

load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_apikey = os.environ["GEMINI_API_KEY"]

ai.configure(api_key=gemini_apikey)

model = ai.GenerativeModel(model_name="gemini-2.0-flash") 

@cl.on_chat_start
async def handle_start_chat():
    await cl.Message(content="Hi! How can I help?").send()

@cl.on_message
async def handle_message(message:cl.Message):
    question = message.content # prompt to the user

 
    response_text = response.text if hasattr(response, "text") else ""

    await cl.Message(content=response_text).send()





