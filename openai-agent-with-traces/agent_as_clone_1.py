from agents import Agent,Runner,function_tool,trace
from connection.myagent import config

@function_tool
def get_location():
    return 'I am in karachi'

agent = Agent(
    name = 'Parent Agent',
    instructions = 
                """
                    You are a helpful assistant. 
                """
)

poet_agent = agent.clone(
    name = 'Poet Agent',
    instructions="""
                    You always respond in a poetic way (Allama Iqbal)
                 """,
    # tools = [get_location]
)

mad_agent = agent.clone(
    name = 'Mad Agent',
    instructions="""
                    You always respond in a abusive way
                 """,
    # tools = [get_location]
)

joker_agent = agent.clone(
    name = 'Joker Agent',
    instructions="""
                    You always respond in the most funny way 
                 """,
    # tools = [get_location]
)

main_agent = Agent(
    name = 'Main Agent',
    instructions = 
                """
                    You are a helpful assistant. 
                    If the query is about location, call the 'get_location' tool. 
                    if someone ask about poems and stanza handoffs to Poet Agent.
                    if someone ask about jokes handoffs to Joker Agent.
                    if someone ask abusive question handoffs to Mad Agent.
                    otherwise respond directly
                """,
    tools=[get_location],
    handoffs=[poet_agent,mad_agent,joker_agent]
)

with trace('Clone Agent'):
    try:
        result = Runner.run_sync(main_agent, 
                                # 'Who is the founder of facebook ',
                                # 'What is my location',
                                # 'what is the sum of 2 and 6 ',
                                # 'suggest me poem',
                                # "my friend is stupid how to tell him",
                                # 'are you stupid',
                                # 'how to absue others who are cheater',
                                # 'hi stupid how are you doing',
                                'tell me a joke about husband and wife',
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


