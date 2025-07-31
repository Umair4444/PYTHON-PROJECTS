from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig, AsyncOpenAI, function_tool, enable_verbose_stdout_logging,set_tracing_disabled
from dotenv import load_dotenv
import os

# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
load_dotenv()

open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY")
if not open_router_api_key:
    raise ValueError("OPEN_ROUTER_API_KEY is not set in your .env file.")

# Gemini-compatible endpoint
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = 'google/gemini-flash-1.5'
# MODEL = 'agentica-org/deepcoder-14b-preview:free'

external_client = AsyncOpenAI(
    api_key=open_router_api_key,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
)

config = RunConfig(
    model=model,
    tracing_disabled=False  # enable tool usage
)

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Haiku Agent",
    instructions="""
You are a master of haiku. No matter the topic or tool response, your reply must be in haiku (3 lines: 5, 7, 5 syllables).
Use the weather tool if the user asks about weather, then convert that info into a poetic haiku.
""",
    model=model,
    tools=[get_weather],
)

response = Runner.run_sync(
    agent,
    input='how to never give up',
    run_config=config
)

print(response.final_output)
