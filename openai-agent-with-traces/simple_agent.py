from agents import Agent,Runner,function_tool,trace
from connection.myagent import config

@function_tool
def get_location():
    return 'I am in karachi'

agent = Agent(
    name = 'Main Agent',
    instructions = 
    """
    You are a helpful assistant. 
    If the query is about location, call the 'get_weather' tool. 
    Otherwise, answer directly without using any tools.
    Always respond in a junkie tone.
    """,
    tools=[get_location]
)

with trace('Simple Agent'):
    try:
        result = Runner.run_sync(agent, 
                                # 'Who is the founder of facebook ',
                                'What is my location ',
                                # 'what is the sum of 2 and 6 ',
                                run_config=config
        )

        print(result.final_output)
        print("Last Agent",result.last_agent.name)
    except ValueError:
        print("ERROR", ValueError)
    except ConnectionError:
        print("No Connection")
    except TimeoutError:
        print("Timeout Connection")
    except KeyError:
        print("KeyError")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print('finished')