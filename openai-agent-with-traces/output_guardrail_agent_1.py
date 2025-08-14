from agents import(
     Agent, GuardrailFunctionOutput, output_guardrail,OutputGuardrailTripwireTriggered,Runner,function_tool,trace,RunContextWrapper)
from pydantic import BaseModel
from connection.myagent import config


class WordOutput(BaseModel):
    answer : str
    is_not_allowed : bool

@function_tool
def get_location():
    return 'I am in karachi'

safe_speech_agent = Agent(
    name= 'Safe Speech Agent',
    instructions=
                """
                You are an guardrail agent and your duty is to make sure block these words:
                [
                    # GAMBLING_KEYWORDS
                    "bet", "bets", "betting", "casino", "poker", "blackjack", "roulette",
                    "baccarat", "slots", "slot machine", "jackpot", "wager", "bookmaker",
                    "sportsbook", "odds", "spread", "pari-mutuel", "bet slip", "chip",
                    "gamble", "gambling", "lottery", "raffle", "scratch card", "dice game",
                    "card game", "sports betting", "handicap", "ante", "pot", "draw poker",
                    "texas hold'em", "craps", "keno",
                    
                    # Illegal / unlicensed
                    "illegal games", "underground casino", "backroom poker", "unlicensed betting",
                    "offshore betting", "match fixing", "point shaving", "illegal lottery",
                    "unregulated gaming", "illegal slot machine", "street dice", "numbers game",
                    "illegal sportsbook", "black market betting",
                    
                    # Slang & betting terms
                    "parlay", "moneyline", "prop bet", "teaser", "over/under", "spread betting",
                    "live odds", "in-play betting", "bankroll", "stake", "high roller",
                    "house edge", "whale", "marker"
                ]

                """,
                output_type=WordOutput
                    )

@output_guardrail
async def safe_speech(ctx:RunContextWrapper[None],agent:Agent,output:WordOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(
        safe_speech_agent,
        output,
        context=ctx.context,
        run_config=config
    )
    print("🔍 Guardrail result:", result.final_output)
    print("🔍 Context result:", ctx)
    print("🔍 Agent result:", agent)

    return GuardrailFunctionOutput(
            output_info =result.final_output,
            tripwire_triggered=result.final_output.is_not_allowed
        )
    

triage_agent = Agent(
    name = 'Main Agent',
    instructions =   
                    """
        You are the orchestrator and manages all the work and decide whether to call tool or handsoff to other agent or answer directly
                    """,
    output_guardrails=[safe_speech],
    tools=[get_location]
)

with trace('Input Guardrail Agent 1'):
    try:
        result = Runner.run_sync(triage_agent, 
                                # 'Who is the founder of facebook ',
                                # 'What is my location ',
                                'how to play poker',
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
    except OutputGuardrailTripwireTriggered:
        print('Output Guardrail trigerred')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print('Finished Execution')