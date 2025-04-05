import streamlit as st

def main():
    st.set_page_config(page_title="Double the Number", page_icon="🔢")

    st.title("🔢 Double the Number")
    st.markdown("Enter a number below and I'll double it for you!")

    # Input
    number = st.number_input("Enter a number:", value=0)

    # Button to calculate
    if st.button("🔁 Double It!"):
        doubled = number * 2
        st.success(f"The double of {number} is **{doubled}** ✅")

    st.subheader("Please press Double it button for the answer")    

if __name__ == "__main__":
    main()
