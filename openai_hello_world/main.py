from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    # model_provider=external_client,
    tracing_disabled=True
)

# Realstate Agent
writer = Agent(
    name = 'Realstate Agent',
    instructions= 
    """You are a Realstate agent. Give advice on buy, sell, rent and property advice.""",
    model = model
)

response = Runner.run_sync(
    writer,
    input = 'give me 10 bullet points on how to buy a property',
    run_config = config
    )
print(response.final_output)

