from agents.news_agent import main
import chainlit as cl
import asyncio

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        'content' : 'How to catch a thief without getting hurt'
    ).srnd()

@cl.on_message
async def on_message(message:cl.Message):
    msg = message.content
    response = asyncio.run(main(msg))
    await cl.Message(
        'content' : f"{response}"
    ).send()