from agents import Agent, Runner, trace,handoff
import rich
from connection.myagent import config
import asyncio
from dotenv import load_dotenv

load_dotenv()

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
       You are a agent that always respond to user general query and answer them in a professional manner.
        """)


triage_Agent = Agent(
    name="Triage Agent",
  instructions=
                """
                    You are a helpful assistant in a restaurant system.
                    
                    Rules:
                    1. If the user's query is about food, menu, orders, pizza, or anything related to eating → 
                    hand off to the Welcome Agent.
                    2. If the query is about general knowledge, facts, or unrelated to food →
                    hand off to the General Agent.
                    3. If neither applies, or if the appropriate agent is unavailable →
                    say exactly: "SORRY".
                    
                    You never answer the query yourself — only decide and hand off.
                """,

    # handoffs=[general_Agent,welcome_Agent],
    handoffs=[handoff(general_Agent,tool_name_override="sending to Gen Agent",tool_description_override="Answer General query")],
    # handoffs=[handoff(general_Agent,tool_name_override="sending to Gen Agent",tool_description_override="Answer General query"),welcome_Agent],
    # handoffs=[handoff(general_Agent,tool_name_override="sending to Gen Agent",tool_description_override="Answer General query"),handoff(waiter_Agent,tool_name_override="send to waiteer")],
    # handoffs=[handoff(waiter_Agent, tool_description_override="Transfer to waiter...")],
    handoff_description =
                        """
                            Route the query to the correct agent: Welcome Agent for food,
                            General Agent for general queries.
                            If no handoff is valid or irrelevant, respond with "SORRY".
                        """
                            )

async def main():
    with trace('handoffs_override'):
        result = await Runner.run(triage_Agent, 
                                # 'Who is the founder of facebook',
                                'Who is the founder of google',
                                # 'Hi i am Umair and i am hungry ',
                                # 'Hi i am Umair and i am not hungry ',
                                # 'Hi i am Umair and how to make a pizza ',
                                # 'I want to eat pizza',
                                run_config=config
        )

        rich.print(result.final_output)
        rich.print("Last Agent ==> ",result.last_agent.name)
        rich.print("NewItems Agent ==> ",result.new_items)

if __name__ == "__main__":
    asyncio.run(main())