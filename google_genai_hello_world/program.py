import google.generativeai as genai
import os
from dotenv import load_dotenv
import PIL.Image

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=gemini_api_key)

gen_config = {
    'temperature': 0.5,
    'max_output_tokens': 200
}


model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              generation_config=gen_config)

img = PIL.Image.open('image1.jpg')

prompt = 'what is in the image write 5 points'
response = model.generate_content([prompt,img])

print(response.text)
