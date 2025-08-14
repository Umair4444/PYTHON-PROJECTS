from dataclasses import dataclass
from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered,Runner,function_tool,trace,input_guardrail,RunContextWrapper
from pydantic import BaseModel
from connection.myagent import config

# Define exactly what final_output contains
@dataclass
class CryptoFinalOutput:
    answer : str
    is_not_crypto: bool
    # add more fields if your agent returns them

# Define the Runner.run return type
@dataclass
class CryptoRunResult:
    final_output: CryptoFinalOutput

crypto_guard_agent = Agent(
    name= 'Crypto Exchange Guard Agent',
    instructions=
                """
                You are a Crypto Expert guard and your duty is to make sure block other queries other than crypto related topics.
                """,
                output_type=CryptoFinalOutput
                    )

@input_guardrail
async def crypto_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str
) -> GuardrailFunctionOutput:
    # Tell Python exactly what type result is
    result: CryptoRunResult = await Runner.run(
        crypto_guard_agent,
        input,
        context=ctx.context,
        run_config=config
    )

    print("🔍 Guardrail result:", result.final_output)
    print("🔍 Context result:", ctx)
    print("🔍 Agent result:", agent)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_not_crypto
    )

@function_tool
def get_location():
    return 'I am in karachi'
    

triage_agent = Agent(
    name = 'Main Agent',
    instructions =   
                    """
        You are the orchestrator and manages all the work and decide whether to call tool or handsoff to other agent or answer directly
                    """,
        #             """
        #             You must use get location tool
        # You are the orchestrator and manages all the work and decide whether to call tool or handsoff to other agent or answer directly
        #             """,
    input_guardrails=[crypto_guardrail],
    tools=[get_location]
)

with trace('Input Guardrail Agent 2'):
    try:
        result = Runner.run_sync(triage_agent, 
                                # 'Who is the founder of facebook ',
                                'What is my location ',
                                # 'what is the sum of 2 and 6 ',
                                # 'How is BTC doing',
                                # 'when was btc launched',
                                # 'how to take trade in 3 lines',
                                run_config=config
        )

        print("Main Agent Final Output",result.final_output)
        print("Last Agent",result.last_agent.name)
    except ValueError:
        print("ERROR", ValueError)
    except ConnectionError:
        print("No Connection")
    except TimeoutError:
        print("Timeout Connection")
    except KeyError:
        print("KeyError")
    except InputGuardrailTripwireTriggered:
        print('🤖 Input Guardrail trigerred')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print('Finished Execution')