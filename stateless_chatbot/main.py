import chainlit as cl

@cl.on_chat_start
async def start():
    response = f"Hi Welcome! to my first chat app."
    await cl.Message(content=response).send()

@cl.on_message
async def main(message : cl.Message):

    print("message",message) # gives memory address
    print("cl.Message",cl.Message) # gives class address
    response = f"You said {message.content} by {message.author}"

    await cl.Message(content=response , author="Devil").send()