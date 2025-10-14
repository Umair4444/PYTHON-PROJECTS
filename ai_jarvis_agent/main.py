import asyncio
from my_triage_agent import ask_the_agent
from input_to_voice import text_to_speech_with_gtts
from voice_to_input import record_and_save_text

async def main():
    user_input = record_and_save_text()
    if user_input:
        print(f"🧠 Processing your command: {user_input}")
        response = await ask_the_agent(prompt=user_input)   # ✅ await here
        print(f"🧠 Agent Response: {response}")
        text_to_speech_with_gtts(response, "agent_response.mp3")
    else:
        print("❌ No valid input detected.")

if __name__ == "__main__":
    asyncio.run(main())
