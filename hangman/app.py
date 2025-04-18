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
        # st.session_state.latest_guess = ""
    print(st.session_state.word)

    # display_words will make letter appear 
    def display_word():
        return " ".join([letter if letter in st.session_state.guessed else "_" for letter in st.session_state.word])

    st.title("🎯 Hangman Game")
    st.subheader("Guess the word:")
    st.markdown(f"# {display_word()}") # "#" will make text large and small
    st.write("Guessed Letters: ", ", ".join(st.session_state.guessed))

    if not st.session_state.game_over:
        with st.form("guess_form", clear_on_submit=True): # clear = True will make form reset to empty strings
            guess = st.text_input("Enter a letter:", max_chars=1,placeholder="Enter the letter here!")
            submit = st.form_submit_button("Submit Guess")

        if submit:
            guess = guess.lower()
            if not guess or not guess.isalpha(): # Checks if the input is empty or not a letter
                st.warning("❗ Please enter a valid single letter.") # displaying a warning if invalid.
            elif guess in st.session_state.guessed:
                st.warning(f"🔁 You've already guessed '{guess.upper()}'!")
            else:
                st.session_state.guessed.append(guess)
                # st.session_state.latest_guess = guess

                if guess in st.session_state.word:
                    st.session_state.feedback = f"✅ '{guess.upper()}' is correct!"
                    st.info(st.session_state.feedback)

                else:
                    st.session_state.attempts += 1
                    st.session_state.feedback = f"❌ '{guess.upper()}' is not in the word."
                    st.info(st.session_state.feedback)


            # Win/Loss logic
            if all(letter in st.session_state.guessed for letter in st.session_state.word):
                st.success(f"🎉 You won! The word was '{st.session_state.word}'")
                st.balloons()
                st.session_state.game_over = True
            elif st.session_state.attempts >= st.session_state.max_attempts:
                st.error(f"💀 Game Over! The word was '{st.session_state.word}'")
                st.session_state.game_over = True

        # # Show result of latest guess
        # if st.session_state.feedback:
        #     st.info(st.session_state.feedback)
        #     # print(st.session_state.feedback)

        st.write(f"❌ Wrong Attempts: {st.session_state.attempts}/{st.session_state.max_attempts}")

    else:
        st.markdown(f"### Final Word: {display_word()}")
        st.info("Thanks for playing!")

    if st.button("🔁 Play Again"):
        st.session_state.word = random.choice(WORDS)
        st.session_state.guessed = []
        st.session_state.attempts = 0
        st.session_state.game_over = False
        # st.session_state.latest_guess = ""
        st.session_state.feedback = ""

if __name__ == "__main__":
    main()
