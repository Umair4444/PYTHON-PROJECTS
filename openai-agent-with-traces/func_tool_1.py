from datetime import date, timedelta
from agents import Agent, Runner, trace, function_tool
from connection.myagent import config
import asyncio
import requests
import rich
import json

# ---------------- TOOLS ---------------- #

@function_tool
def search_flight(origin: str = "", destination: str = "", date_: str = date.today().isoformat()):
    """
    Search available flights based on route and date.
    If origin or destination is empty, return all flights for the date.
    """
    flights = [
        {"airline": "Qatar Airways", "price": 450, "duration": 6, "departure": "10:00", "arrival": "16:00"},
        {"airline": "Emirates", "price": 400, "duration": 7, "departure": "12:00", "arrival": "19:00"},
        {"airline": "Turkish Airlines", "price": 380, "duration": 8, "departure": "09:00", "arrival": "17:00"},
    ]

    if not origin or not destination:
        return {
            "note": "Origin or destination not provided, showing all available flights.",
            "date": date_,
            "flights": flights
        }

    # Here you could filter by origin/destination if you had actual data
    return {
        "origin": origin,
        "destination": destination,
        "date": date_,
        "flights": flights
    }

@function_tool
def get_cheapest_flight(flights):
    """Get the cheapest flight from a list (handles JSON string or list)."""
    if isinstance(flights, str):
        flights = json.loads(flights)
    cheapest = min(flights, key=lambda f: f["price"])
    return {"cheapest": cheapest}

@function_tool
def get_fastest_flight(flights):
    """Get the fastest flight from a list (handles JSON string or list)."""
    if isinstance(flights, str):
        flights = json.loads(flights)
    fastest = min(flights, key=lambda f: f["duration"])
    return {"fastest": fastest}

@function_tool
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
    name="travel_agent",
    instructions="""
    You are a helpful travel assistant.
    - If the user does not specify a date, assume today's date automatically.
    - If the user does not specify origin or destination, call 'search_flight' with empty strings for them.
    - Use 'search_flight' first to get flights.
    - Then use 'get_cheapest_flight' or 'get_fastest_flight' depending on user query.
    - Always pass a valid list of flights to 'get_cheapest_flight'/'get_fastest_flight'.
    - if query is not about cheap or fastest flight show all flights available.
    - Use 'get_weather' if asked about weather.
    """,
    tools=[search_flight, get_cheapest_flight, get_fastest_flight, get_weather],
)

# ---------------- RUNNER ---------------- #

async def main():
    with trace("function_tool"):
        result = await Runner.run(
            triage_agent,
            # "Find me the cheapest flight tomorrow",
            # "Find me the cheapest flight to london",
            "Find me the fastest flight to london",
            # "Find me all flight from london to kuwait",
            # "all flight from london to kuwait",
            run_config=config,
        )
        rich.print("[RESULT]:", result.final_output)
        print("Last Agent =>", result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())
