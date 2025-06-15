import random
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool, set_tracing_disabled
import os
from dotenv import load_dotenv
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
import subprocess
import platform
from pydub import AudioSegment
import requests

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
# api_key = os.getenv("OPENWEATHER_API_KEY")

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

@function_tool
def get_static_weather(city: str) -> str:
    """Get the weather for a given city but my weather should be updated and accurate based on live data."""
    print(f"[debug] get_weather called with city: {city}")
    choices = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {city} is {random.choice(choices)}."

@function_tool
def get_live_weather(city: str) -> str:
    """Get live weather data for a city using OpenWeatherMap."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response.get("weather"):
        desc = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        return f"The weather in {city} is {desc} with a temperature of {temp}°C."
    else:
        return f"Couldn't get weather for {city}. Please check the city name."

spanish_agent = Agent(
    name="Spanish",
    handoff_description="A spanish speaking agent.",
    instructions="You're speaking to a human, so be polite and concise. Speak in Spanish.",
    model=model,
)

agent = Agent(
    name="Assistant",
    instructions="You're speaking to a human, so be polite and concise. If the user speaks in Spanish, handoff to the spanish agent.",
    model=model,
    handoffs=[spanish_agent],
    tools=[get_live_weather],
)

response = Runner.run_sync(
    agent,
    input = 'How is the weather in sydney today?',
    run_config = config
    )
print(response.final_output)


# audio have to run manually
def text_to_speech_with_gtts_manually_play(input_text,output_filepath):
    language="en"

    audioobj = gTTS(
        text=input_text,
        slow=False,
        lang=language
    )
    audioobj.save(output_filepath)

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

# audio have to run manually
def text_to_speech_with_elevenlabs_manually_play(input_text,output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
            text= input_text,
            voice_id= "9BWtsMINqrJLrRacOk9x",
            output_format= "mp3_22050_32",
            model_id= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)


if __name__ == "__main__":
    # text_to_speech_with_elevenlabs_manually_play(input_text=response.final_output,output_filepath='elevenlabs_response.mp3')

    text_to_speech_with_gtts_manually_play(input_text=response.final_output,output_filepath='gtts_response.mp3')