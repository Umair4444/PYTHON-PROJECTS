## langchain langchain-google-genai

from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

MODEL = 'gemini-1.5-flash'

model = ChatGoogleGenerativeAI(
    model = MODEL,
    api_key = gemini_api_key
)

response = model.invoke('Name the largest planet and 2 lines about it')

print(response.content)