import streamlit as st
import random

def main():
    WORDS = ["python", "streamlit", "hangman", "developer", "interface", "frontend"]

    if "word" not in st.session_state:
        st.session_state.word = random.choice(WORDS)
        st.session_state.guessed = []
        st.session_state.attempts = 0
        st.session_state.max_attempts = 6
        st.session_state.game_over = False
        st.session_state.feedback = ""
        st.session_state.latest_guess = ""

    def display_word():
        return " ".join([letter if letter in st.session_state.guessed else "_" for letter in st.session_state.word])

    def process_guess(guess):
        guess = guess.lower()

        if not guess or not guess.isalpha() or len(guess) != 1:
            st.session_state.feedback = "❗ Please enter a single alphabet letter."
            return
        if guess in st.session_state.guessed:
            st.session_state.feedback = f"🔁 You've already guessed '{guess.upper()}'!"
            return

        st.session_state.guessed.append(guess)
        st.session_state.latest_guess = guess

        if guess in st.session_state.word:
            st.session_state.feedback = f"✅ '{guess.upper()}' is correct!"
        else:
            st.session_state.attempts += 1
            st.session_state.feedback = f"❌ '{guess.upper()}' is not in the word."

        if all(letter in st.session_state.guessed for letter in st.session_state.word):
            st.session_state.game_over = True
            st.balloons()
        elif st.session_state.attempts >= st.session_state.max_attempts:
            st.session_state.game_over = True

    st.title("🎯 Hangman Game")
    st.subheader("Guess the word:")
    st.markdown(f"### {display_word()}")
    st.write("Guessed Letters: ", ", ".join(st.session_state.guessed))

    if not st.session_state.game_over:
        # Display a text input for the guess
        user_guess = st.text_input("Enter a letter:", max_chars=1)

        if st.button("✅ Enter Guess"):
            process_guess(user_guess)
            # Clear the input after processing the guess
            st.session_state["guess_input"] = ""  # This won't cause an error now

        if st.session_state.feedback:
            st.info(st.session_state.feedback)

        st.write(f"❌ Wrong Attempts: {st.session_state.attempts}/{st.session_state.max_attempts}")
    else:
        if all(letter in st.session_state.guessed for letter in st.session_state.word):
            st.success(f"🎉 You won! The word was '{st.session_state.word}'")
        else:
            st.error(f"💀 Game Over! The word was '{st.session_state.word}'")
        st.markdown(f"### Final Word: {display_word()}")
        st.info("Thanks for playing!")

    if st.button("🔁 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.warning('Game is reset!')

if __name__ == "__main__":
    main()