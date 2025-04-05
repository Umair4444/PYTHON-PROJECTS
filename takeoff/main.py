import streamlit as st
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Rocket Launch App", page_icon="🚀")

st.title("🚀 Rocket Takeoff App")

# Input takeoff time
takeoff_delay = st.slider("Set countdown (in seconds)", min_value=5, max_value=60, value=10)
rocket_name = st.text_input("Enter Rocket Name", "FalconX")

if st.button("Initiate Countdown"):
    st.write(f"🛰️ Rocket **{rocket_name}** is preparing for launch...")
    countdown_placeholder = st.empty()

    # without st,empty it print every countdown in new line
    # for i in range(takeoff_delay, 0, -1):
    #     st.markdown(f"### ⏳ T-minus {i} seconds")
    #     time.sleep(1)

    # st.empty make print update in asinlge line overriding the previous count
    for i in range(takeoff_delay, 0, -1):
        countdown_placeholder.warning(f"### ⏳ T-minus {i} seconds")
        time.sleep(1)
        countdown_placeholder.success(f"## 🚀 Liftoff! The {rocket_name} has launched!")    

    st.balloons()
    
