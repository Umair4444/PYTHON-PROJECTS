import streamlit as st
import random
import string

def generate_password(length, use_digits, use_special):

    characters = string.ascii_letters

    if use_digits:
        characters += string.digits #add numbers

    if use_special:
        characters += string.punctuation #add specials

    return "".join(random.choice(characters) for _ in range(length))

st.title("Password Generator")

length = st.slider("Select Password Length", min_value=6, max_value=32,value=12)

use_digits = st.checkbox("Include Digits")
use_specials = st.checkbox("Include Special Characters")

if st.button ("Generate Password"):
    password = generate_password(length,use_digits,use_specials)
    st.write (f"Generate Password: {password}")