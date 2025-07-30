from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig, AsyncOpenAI, function_tool
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()

# Fetch Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Gemini client (OpenAI-compatible)
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model wrapper
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  # or "gemini-2.0-pro"
    openai_client=external_client
)

# Runner configuration
config = RunConfig(
    model=model,
    tracing_disabled=True
)

# Sample weather tool
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is currently sunny with clear skies."

# Crime News Agent
crime_news_agent = Agent(
    name='Crime News Agent',
    instructions="You are a professional crime reporter. Answer questions about police, murder, investigation, and criminal topics with clarity and detail.",
    handoff_description="Handles crime-related questions and criminal news.",
    model=model
)

# Weather News Agent
weather_news_agent = Agent(
    name='Weather News Agent',
    instructions="""
        You are a weather news specialist. You provide:
        - Current forecasts using tools
        - Commentary and summaries about historical weather events (like hurricanes, floods, etc.)
        Respond in a calm and professional tone. """,
    handoff_description="Handles weather news and local forecasts.",
    tools=[get_weather],
    model=model
)

# Chief Editor Agent
chief_editor_agent = Agent(
    name="Chief Editor Agent",
    instructions="""
You are the Chief Editor of a news organization.

- If the question includes words like "weather", "forecast", or city names, use the Weather News Agent.
- If the question involves police, murder, crime, investigation, or legal actions, use the Crime News Agent.
- For anything else, you must respond directly — as a professional, confident news anchor. 
    Never say you're unsure — instead, offer a neutral, informative statement on the topic.""",
    model=model,
    handoffs=[crime_news_agent, weather_news_agent]
)

# Async main function
async def main():
    response = await Runner.run(
        chief_editor_agent,
        # input='how to surrender to police',
        # input='toma and jerry',
        input='hurricanee in karachi history',
        run_config=config,
    )

    print("\n📰 Final Output:\n", response.final_output)


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
