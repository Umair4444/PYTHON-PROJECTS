import streamlit as st

def main():
    st.title("🐵 Mad Libs Generator!")
    st.subheader("Fill in the blanks to create a hilarious story 🤪")

    # User Inputs
    place = st.text_input("Enter a place:")
    adjective = st.text_input("Enter an adjective:")
    animal = st.text_input("Enter an animal:")
    verb = st.text_input("Enter a verb (base form):")
    noun = st.text_input("Enter a noun:")

    # Generate Story
    if st.button("Generate Story"):
        if place and adjective and animal and verb and noun:
            story = f"""
            Today I went to the **{place}** and saw a **{adjective}** **{animal}**
            trying to **{verb}** a **{noun}**.  
            It was the best day ever!
            """
            st.markdown("### Your Mad Libs Story:")
            st.markdown(story)
        else:
            st.warning("Please fill in all the fields to create your story.")

if __name__ == "__main__":
    main()



