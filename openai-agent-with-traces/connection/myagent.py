from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set. Please ensure it is defined in your .env file.")
if not mistral_api_key:
    raise ValueError("MISTRAL_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    # api_key=gemini_api_key,
    api_key=groq_api_key,
    # api_key=mistral_api_key,
    # base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    base_url="https://api.groq.com/openai/v1",
    # base_url="https://api.mistral.ai/v1/"
)

model = OpenAIChatCompletionsModel(
    # model = "gemini-2.5-pro",
    # model="gemini-1.5-flash",
    # model="gemini-2.5-flash", # gemini
    # model="llama-3.1-8b-instant", # groq
    model="meta-llama/llama-4-scout-17b-16e-instruct", # groq
    # model="mistral-medium-2508", # mistral
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,    
    # tracing_disabled=True
)