from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
from connection.myagent import config
import asyncio
import rich

class UserInfo(BaseModel):
    user_id: int | str
    name: str

user = UserInfo(user_id= "007", name="Umair")

@function_tool
def get_user_info(wrapper: RunContextWrapper[UserInfo]):
    rich.print(wrapper.context.name)
    return f'The user info is {wrapper.context.name}'

personal_agent = Agent(
    name = "Context Management",
    instructions="You are a helpful assistant, always call the tool to get user's information",
    tools=[get_user_info]
)
async def main():
    result = await Runner.run(
        personal_agent, 
        'What is the name', 
        # 'What is my id',
        run_config=config,
        context = user #Local context
        )
    rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())