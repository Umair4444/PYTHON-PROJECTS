import asyncio
import re
import os
import pyttsx3
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from agent_web_tool import execute_command  # 👉 Your custom tool for system actions

# ✅ Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY is not set in your .env file")

# 🤖 Configure Gemini API as OpenAI compatible
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    tracing_disabled=True
)

# 🧠 Define the Agent
agent = Agent(
    name="Optimum Answer Agent",
    instructions=(
        "You are a smart triage assistant. "
        "If the user asks you to open or launch something like Notepad, Calculator, or Browser, "
        "use the available tools to do it. "
        "If no tool can handle the command, politely say so. "
        "If the user asks a question, provide a clear and accurate answer."
    ),
    tools=[execute_command]
)

# 🧠 Function to talk to the Agent
async def ask_the_agent(prompt: str) -> str:
    result = await Runner.run(agent, input=prompt, run_config=config)
    # 🧹 Clean the output text
    clean_text = re.sub(r'[*_`#]', '', result.final_output)
    return clean_text

# 🗣️ Text-to-Speech function
def voice_output(final_output: str):
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    engine.setProperty("volume", 1.0)
    engine.say(final_output)
    engine.runAndWait()

# 🚀 Run the agent
if __name__ == "__main__":
    # user_input = "open notepad"  # Try also: "Who is the founder of Google?"
    user_input = "Who is the founder of Google?"  # Try also: "Who is the founder of Google?"
    response = asyncio.run(ask_the_agent(prompt=user_input))
    print(f"🧠 Agent Response: {response}")
    voice_output(response)
