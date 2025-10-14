# main.py
from audio_to_text_engine import speak
from my_triage_agent import ask_the_agent
from agent_voice_output import speak_text

print("🎤 Voice Triage Agent Started. Say 'bye' to exit.")

while True:
    # 1️⃣ Get user input via voice
    user_input = speak()
    if not user_input:
        continue  # retry if nothing heard

    print(f"🗣 You: {user_input}")

    # 2️⃣ Break loop if user says bye
    if user_input.lower() in ["bye", "exit", "quit"]:
        speak_text("Goodbye!")
        print("👋 Exiting. Goodbye!")
        break

    # 3️⃣ Get agent response
    agent_response = ask_the_agent(user_input)
    print(f"🤖 Agent: {agent_response}")

    # 4️⃣ Speak the agent response
    speak_text(agent_response)
