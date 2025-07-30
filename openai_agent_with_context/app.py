from dataclasses import dataclass
from agents import (
    Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,
    RunConfig, function_tool, set_tracing_disabled, ItemHelpers,
    RunContextWrapper
)
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import asyncio

# Disable tracing and load API key
set_tracing_disabled(True)
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Connect Gemini via OpenAI-compatible API
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(model=model, tracing_disabled=True)

# 🧑 Context passed to agent
@dataclass
class UserInfo:
    name: str
    uid: int | str

# ✅ Tool input using Pydantic
class GreetingInput(BaseModel):
    greeting: str
    tone: str  # e.g., "formal" or "casual"

# 🛠️ Tool that takes a BaseModel input
@function_tool
async def greet_user(context: RunContextWrapper[UserInfo], input: GreetingInput) -> str:
    """
    Greets the user with their name using the specified tone.
    Args:
        input: GreetingInput object containing message and tone
    """
    name = context.context.name
    if input.tone.lower() == "formal":
        return f"Good day, {name}. {input.greeting}"
    elif input.tone.lower() == "casual":
        return f"Hey {name}! {input.greeting} 😄"
    else:
        return f"Hello {name}, {input.greeting}"

# 🧠 Main function to run the agent
async def main():
    user_info = UserInfo(name="Umair", uid="007")

    agent = Agent[UserInfo](
        name="Assistant",
        tools=[greet_user],
        model=model,
        instructions=(
            "Always greet the user using the greet_user tool. "
            "Welcome them to Panaversity. "
            "Add a welcome joke based on the tone: formal or casual."
        )
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Greet me in a formal tone and welcome me to the platform",
        context=user_info
    )

    print(result.final_output)

asyncio.run(main())

