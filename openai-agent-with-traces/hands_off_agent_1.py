from agents import Agent, Runner, trace
from connection.myagent import config
import asyncio

waiter_Agent = Agent(
    name="Waiter Agent",
    instructions=
    """
    You are a waiter agent and provide a list of pizzas to the customer.
    Always Provide the customer with the list of available pizzas and their prices:
        ## Your pizza list:
        1. Margherita - $12
        2. Pepperoni - $15  
        3. Vegetarian - $14
    """
)

welcome_Agent = Agent(
    name="Welcome Agent",
    instructions=
        """
        You are a Welcome agent in a Pizza Restuarant you task is to greet user and always handoffs to waiter agent
        1. Welcome user politely.
        2. Ask them to have a seat.
        3. Always Handoffs to the waiter agent to show the the menu
        """ ,
        handoffs=[waiter_Agent],
        handoff_description="transfer to waiter agent to takes order from guest"
        )

general_Agent = Agent(
    name="General Agent",
    instructions=
        """
       You are a agent that always respond to user query and answer them in a professional manner.
        """ ,
        )


triage_Agent = Agent(
    name="Triage Agent",
    instructions="""
                You are a helpful assistant.
                Your task is to help the user with their queries 
                and always hand them off to the appropriate delegate agent.
                """,
    handoffs=[welcome_Agent,general_Agent],
    handoff_description="""First, ensure the guest is greeted by the welcome agent. Then, hand them off to the waiter agent to take their order.
                            and if it is general query answer them directly.
                        """
                        )


async def main():
    with trace('hands_off_1'):
        result = await Runner.run(triage_Agent, 
                                'Who is the founder of facebook',
                                # 'Hi i am Umair and i am hungry ',
                                # 'Hi i am Umair and i am not hungry ',
                                # 'Hi i am Umair and how to make a pizza ',
                                # 'I want to eat pizza',
                                run_config=config
        )

        print(result.final_output)
        print("Last Agent ==> ",result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())