import asyncio
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os

# Disable tracing
set_tracing_disabled(disabled=True)

# Load environment variables
load_dotenv()

# Get API Key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Model ID for Gemini 2.0 Flash (LiteLLM-compatible)
MODEL = "gemini/gemini-2.0-flash"

# Define a simple function tool
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

# Initialize the LiteLLM model
model = LitellmModel(model=MODEL, api_key=gemini_api_key)

# Create the agent with haiku instructions
agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model=model,
    tools=[get_weather],
)

# Run the agent synchronously
response = Runner.run_sync(agent, input='weather in Karachi')
print(response.final_output)