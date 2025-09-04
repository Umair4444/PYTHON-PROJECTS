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
agent = Agent(
  name="Optimum Answer Agent",
    instructions=
        "You are an intelligent and helpful AI assistant. "
        "For any question or task, provide the most optimal, accurate, and efficient response possible. "
        "Use expert-level knowledge, clear reasoning, and concise explanations.",
    model = model
)

def ask_the_agent(prompt: str) -> str:
    result = Runner.run_sync(agent, input=prompt, run_config=config)
    return result.final_output

