from agents import Agent, Runner, trace, function_tool
from connection.myagent import config
import asyncio
import requests
import rich

# ---------------- TOOLS ---------------- #

@function_tool(name_override="ADDITION TOOL",description_override="IT DOES ADDITION CALCULATION")
def add_tool(num1:int , num2:int):
    """Your job is to add two number"""
    num1 = int(num1)
    num2 = int(num2)
    return f" the sum of {num1} and {num2} is {num1 + num2}"

@function_tool
def minus_tool(num1:int , num2:int):
    """Your job is to minus two number"""
    num1 = int(num1)
    num2 = int(num2)
    return f" the subtraction of {num1} and {num2} is {num1 - num2}"

@function_tool(is_enabled=False)
def get_weather(city: str):
    """Get current weather in the given city."""
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    data = response.json()
    current = data["current_condition"][0]
    return {
        "city": city,
        "temperature_C": current["temp_C"],
        "weather": current["weatherDesc"][0]["value"]
    }

# ---------------- AGENT ---------------- #

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
                You are a helpful math assistant.
                - You must always pass integers (not strings) to the tools.
                - Example: {"num1": 2, "num2": 4} not {"num1": "2", "num2": "4"}.
                - If you repsonse always start with Hurray I can do it and your answer is ==>
                - If you cannot respond say Go somewhere else stupid it is not my job to answer your silly questions! 🤬
                """,
    tools=[get_weather,add_tool,minus_tool],
)

# ---------------- RUNNER ---------------- #

async def main():
    with trace("function_tool_Override"):
        result = await Runner.run(
            triage_agent,
            "What is 2 plus 4",
            run_config=config,
        )
        rich.print("[RESULT]:", result.final_output)
        rich.print("Last Agent =>", result.last_agent.name)
        rich.print("New Items =>", result.new_items)

if __name__ == "__main__":
    asyncio.run(main())
