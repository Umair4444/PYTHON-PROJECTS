import os
# import chainlit as cl
import google.generativeai as ai
from dotenv import load_dotenv

# This is a stateless chatbot in terminal

load_dotenv()

ai.configure(api_key=os.environ["GEMINI_API_KEY"])

# model = ai.GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")
model = ai.GenerativeModel(model_name="gemini-2.0-flash")


while True:
    user_input = input("\nEnter your question (or type 'q' to quit): ").strip()

    if user_input.lower() in ["q", "quit"]:
        print("Thanks for chatting! Goodbye!")
        break

    try:
        response = model.generate_content(user_input)
        print("\nResponse:", response.text)
    except Exception as e:
        print("API call failed:", e)

