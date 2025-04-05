import streamlit as st
import random

# Constants
PROMPT = "What do you want?"
JOKE = [
    "A guy in a plane stood up & shouted: 'HIJACK!' All passengers got scared. From the other end of the plane, a guy shouted back: 'HI JOHN'.",
    "I wanted to tell you a construction joke, but I cannot. Because it is still a work in progress!",
    "If a paper comes very tough in an exam, just close your eyes for a moment, take a deep breath, and say loudly, 'This is a very interesting subject; I want to study it again.'"
]
SORRY = "Sorry I only tell jokes"

# App UI
st.set_page_config(page_title="Joke Bot 🤖", page_icon="😂")
st.title("🤖 Joke Bot")

# User selects from dropdown
user_choice = st.selectbox(PROMPT, ["Joke", "Weather", "News", "Motivation"])

# Response
if user_choice == "Joke":
    # Pick a random joke from the list
      # Button to load another joke
    if st.button("Generate Joke"):
        joke = random.choice(JOKE)
        st.session_state.joke = random.choice(JOKE)
        st.success(joke)

else:
    st.warning(SORRY)
