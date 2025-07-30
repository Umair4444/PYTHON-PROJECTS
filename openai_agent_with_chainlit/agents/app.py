from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig, AsyncOpenAI, function_tool
from dotenv import load_dotenv
import os

load_dotenv()

# Load Gemini API key from environment
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Setup Gemini client using OpenAI-compatible API
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Use Gemini 2.0 Flash model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure agent runner
config = RunConfig(
    model=model,
    tracing_disabled=True
)

# Define a tool to fetch weather
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

# Sub-agent: Weather
weather_news_agent = Agent(
    name='Weather News Agent',
    instructions="You are a weather news agent. Only answer weather-related questions.",
    handoff_description="Handles weather-related topics.",
    tools=[get_weather],
    # model=model  # Optional but allows fallback
)

# Sub-agent: Crime
crime_news_agent = Agent(
    name='Crime News Agent',
    instructions="You are a crime news agent. Only answer crime-related questions.",
    handoff_description="Handles crime-related news.",
    # model=model  # Needed to respond if routed
)

# Chief Editor Agent
chief_editor_agent = Agent(
    name="Editor Agent",
instructions="""You are a professional news editor. You can answer all types of general knowledge questions. 
                Only delegate to sub-agents if the query is clearly about weather or crime.""",    
model=model,
    tools=[
        weather_news_agent.as_tool(
            tool_name='weather_news_agent_tool',
            tool_description='Handles weather-related topics.'
        ),
        crime_news_agent.as_tool(
            tool_name='crime_news_agent_tool',
            tool_description='Handles crime-related topics.'
        )
    ]
)

# Run agent with a general query
response = Runner.run_sync(
    chief_editor_agent,
    input='Who is the founder of Pakistan?',
    run_config=config
)

# Print output
print(response.final_output)
