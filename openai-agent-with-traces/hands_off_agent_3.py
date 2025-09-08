from agents import Agent, Runner, trace, handoff
from agents.extensions import handoff_filters
import rich
from connection.myagent import config
import asyncio
from dotenv import load_dotenv

load_dotenv()

botany_agent = Agent(
    name="Botany Agent",
    instructions=
    """
    You are a Botany Agent. 
    Your job is to answer any questions related to plants, trees, flowers, photosynthesis, plant biology, 
    and ecosystems that involve plants. 
    Always provide clear, concise, and factual explanations.
    """,
)

zoology_agent = Agent(
    name="Zoology Agent",
    instructions=
    """
    You are a Zoology Agent. 
    You specialize in animals, their biology, habitats, behavior, and classifications. 
    Always answer with accurate zoological knowledge in a simple and professional tone.
    """,
)

science_agent = Agent(
    name="Science Agent",
    instructions=
    """
    You are a Science Agent.
    Handle queries related to general science, physics, chemistry, biology, astronomy, 
    or scientific facts. 
    If the query is specific to plants, hand it off to the Botany Agent. 
    If the query is about animals, hand it off to the Zoology Agent.
    """,
    # handoffs=[botany_agent, zoology_agent],
    handoffs=[handoff(botany_agent,input_filter=handoff_filters.remove_all_tools),
    zoology_agent],
    handoff_description=
    """
    Forward plant-related questions to the Botany Agent and 
    animal-related questions to the Zoology Agent.
    Handle all other science queries yourself.
    """
)

math_agent = Agent(
    name="Math Agent",
    instructions=
    """
    You are a Math Agent.
    Solve problems and answer queries related to mathematics: 
    arithmetic, algebra, geometry, calculus, statistics, and applied math. 
    Always explain step by step when solving problems.
    """,
    handoff_description=
    """
    Responsible for handling all math-related queries.
    """
)

general_agent = Agent(
    name="General Agent",
    instructions=
    """
    You are a General Agent.
    You handle everyday general knowledge queries, history, geography, 
    famous personalities, current events, and basic Q&A. 
    Always respond in a clear and professional manner.
    """
)

triage_Agent = Agent(
    name="Triage Agent",
    instructions=
    """
    You are a helpful triage assistant in a multi-domain question-answering system.
    
    Rules:
    - Identify the nature of the user's query.
    - If it's about mathematics → route to Math Agent.
    - If it's about science → route to Science Agent.
    - If it's a general question → route to General Agent.
    - If no match applies or the query is irrelevant → respond with "SORRY".
    """,
    handoffs=[science_agent, math_agent,
    handoff(
            general_agent,
            tool_name_override="shifting_to_general_agent",
            tool_description_override="Use this tool to handle general queries",
            # input_filter=handoff_filters.remove_all_tools, # (only last) removing all tool calls from the history 

        ),
        ],
    handoff_description=
    """
    Route the query to the correct agent:
    - Math Agent → for math-related queries
    - Science Agent → for science-related queries
    - General Agent → for general queries
    If no suitable agent is available, respond with "SORRY".
    """
)

async def main():
    with trace('hand_offs_3'):
        result = await Runner.run(
            triage_Agent,
            # 'Who is the founder of facebook',
            'What is scientic name of rose',
            run_config=config
        )

        rich.print(result.final_output)
        rich.print("Last Agent ==> ", result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())
