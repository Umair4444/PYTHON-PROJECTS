import streamlit as st
import random
import time
import requests

st.title("Money Making Machine")

def generate_money():
    return random.randint(1,10000)

# Create a section for generating money
st.subheader("Instant Cash Generator")
if st.button("Generate Money"):  # When user clicks the button
    st.write("Counting your money...")  # Show loading message
    time.sleep(1)  # Wait for 3 seconds
    amount = generate_money()  # Get random amount
    st.success(f"You made Pkr{amount}!")  # Show success message with amount

    # my api route https://python-projects-two.vercel.app/
    # my api key to access apikey = 1234
    # https://python-projects-two.vercel.app/side_hustles?apikey=1234

def side_hustles():
    try:
        # Try to get data from local server or deployed server
        response = requests.get(
            "https://python-projects-two.vercel.app/side_hustles?apikey=1234"
        )
        if response.status_code == 200:  
            hustles = response.json()  
            print(hustles["side_hustles"])
            return hustles["side_hustles"] 
        else:
            return "Freelancing"  

    except:
        return "Something went wrong!"  

# Create a section for side hustle ideas
st.subheader("Side Hustle Ideas")
if st.button("Generate Hustle"): 
    idea = side_hustles()  
    st.success(idea)  


# Function to get money-related quotes from server
def money_quote():
    try:
        response = requests.get(
            "https://python-projects-two.vercel.app/money_quotes?apikey=1234"
        )
        if response.status_code == 200: 
            quotes = response.json()  
            return quotes["money_quotes"]  
        else:
            return "Money is the root of all evil!"  
    except:
        return "Something went wrong!"  


# Create a section for motivation quotes
st.subheader("Money-Making Motivation")
if st.button("Get Inspired"): 
    quote = money_quote()  
    st.info(quote)  