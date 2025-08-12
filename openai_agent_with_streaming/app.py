import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig,ItemHelpers,function_tool
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
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

async def main():

    @function_tool
    def weather(city):
        return f"the weather of {city} is sunny"

    # Realstate Agent
    writer = Agent(
        name = 'Realstate Agent',
        instructions= 
        """You are a Realstate agent. Give advice on buy, sell, rent and property advice.""",
        model = model,
        tools=[weather]
    )


    response = Runner.run_streamed(
        writer,
        input = 'give me 2 bullet points on how to buy a property only and weather in karachi',
        run_config = config)
    
    print("=== Run starting ===")
    async for event in response.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        #     print(event.data.delta, end="", flush=True)
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
                print('----')
            else:
                pass  # Ignore other event types

asyncio.run(main())