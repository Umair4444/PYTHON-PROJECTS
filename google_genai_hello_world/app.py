import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=gemini_api_key)

gen_config = {
    'temperature': 0.5,
    'max_output_tokens': 10
}

model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              generation_config=gen_config)

response = model.generate_content('Name the highest mountain in the world with 2 lines.')

print(response.text)
