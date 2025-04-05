import streamlit as st
import random

if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, 5)
if "guesses" not in st.session_state:
    st.session_state.guesses = []

st.write("Guess the number between 1 and 100")

guess = st.number_input("Enter your guess", min_value=1, max_value=100, key="guess", step=1)

if st.button("Submit"):
    st.session_state.guesses.append(guess)
    if guess == st.session_state.target_number:
        st.success(f"Congratulations! You guessed the number in {len(st.session_state.guesses)} attempts")
        st.write(f"Your guesses: {st.session_state.guesses}")
        st.balloons()
        st.session_state.target_number = random.randint(1, 5)
        st.session_state.guesses = []
    elif guess < st.session_state.target_number:
        st.write("Try a higher number")
    else:
        st.write("Try a lower number")

if st.button("Play Again"):
    st.session_state.target_number = random.randint(1, 5)
    st.session_state.guesses = []
