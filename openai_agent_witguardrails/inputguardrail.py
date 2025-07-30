import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    RunContextWrapper,
    TResponseInputItem,
    OpenAIChatCompletionsModel,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    GuardrailFunctionOutput,
    input_guardrail,
    output_guardrail,
    )

from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
print("🔐 GEMINI_API_KEY:", gemini_api_key)


#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    # model="gemini-2.0-flash", # not gonna work
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    # model_provider=external_client,
    tracing_disabled=True
)

class MathHomeWorkOutput(BaseModel):
    is_math_homework : bool
    reasoning : str
    answer : str

guardrail_agent = Agent(
    name = "Guardrail Agent",
    instructions="Check if user is asking you to do Math homework do",
    output_type=MathHomeWorkOutput,
    model=model
)

@input_guardrail
async def math_guardril(ctx:RunContextWrapper[None], agent:Agent, input:str | list[TResponseInputItem])->GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_agent,
        input,
        context=ctx.context,
        run_config=config
        )
    
    print("🔍 Guardrail result:", result.final_output)


    return GuardrailFunctionOutput(
            output_info = result.final_output,
            tripwire_triggered=result.final_output.is_math_homework
        )


manager = Agent(
    name = "Professor Agent",
    instructions= "You are the orchestrator and manages all the work and decide whether to call tool or handsoff to other agent",
    input_guardrails=[math_guardril],
    model=model
)

async def myfunc():
    try:
        response =await Runner.run(
            manager,
            # input="How to make coffee in 3 lines only and no useless information",
            input="Solve: (2x + 5)^2 = 49",
            run_config=config
        )
        print("Guardrail didn't trip - this is unexpected")

        print(response.final_output)
    except InputGuardrailTripwireTriggered:
        print('Input Guardrail trigerred')
        
asyncio.run(myfunc())



