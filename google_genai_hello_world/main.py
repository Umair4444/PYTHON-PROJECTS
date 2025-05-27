import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() 

# Make sure your .env or system environment has GEMINI_API_KEY set
gemini_api_key = os.getenv("GEMINI_API_KEY")  # Use quotes

# Optional: Raise error if not set
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content('Name the highest mountain in the world.')

print(response.text)
