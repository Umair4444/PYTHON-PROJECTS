from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
from dotenv import load_dotenv
import requests
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

# Define a route for /weather?city=CityName
@function_tool
def get_weather(city: str):
    """Give dwtail weather on the city
    
    Args : get city name from the prompt
    """
    # Create the URL for the public weather service
    url = f"https://wttr.in/{city}?format=j1"

    # Send an HTTP GET request to wttr.in
    response = requests.get(url)
    data = response.json()  # Parse JSON response

    # Get current weather information
    current = data["current_condition"][0]

    # Return weather details as JSON
    return {
        "city": city,
        "temperature_C": current["temp_C"],
        "weather": current["weatherDesc"][0]["value"],
        "humidity": current["humidity"],
        "wind_speed_kmph": current["windspeedKmph"]
    }


# Realstate Agent
writer = Agent(
    name = 'Manager',
    instructions= 
    """You are a helpful assisstant and respond to queries in a romantic manner.""",
    model = model,
    tools=[get_weather]
)

response = Runner.run_sync(
    writer,
    input = 'What is the current weather in Islamabad?',
    run_config = config
    )
print(response.final_output)
