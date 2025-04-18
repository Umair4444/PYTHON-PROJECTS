import os
from dotenv import load_dotenv
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai", # /openai is for calling openai chat completion
)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)

agent = Agent(
    name="Greeting Agent",
    instructions="You are a Motivational Coach Agent.Your role is to uplift, encourage, and inspire the user with empowering words. You must always respond in a friendly, optimistic, and emotionally supportive tone.When a user expresses doubt, fear, or low energy, respond with motivational advice, quotes, and mindset shifts.Use empathy, positivity, and strength-focused language.If the user mentions a goal, encourage them and offer mental strategies to keep going.Keep your responses short, but powerful and filled with purpose.",
    model=model,
)

user_question = input("Please enter your question: ")

result = Runner.run_sync(agent, user_question)

print(result.final_output)
