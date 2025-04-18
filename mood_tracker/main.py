import streamlit as st
import pandas as pd
import datetime
import os


# File to store mood data
data_file = "mood_data.csv"

# Load existing data or create a new one
def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    else:
        return pd.DataFrame(columns=["Date", "Mood", "Notes"])

# Save mood data
def save_data(df):
    df.to_csv(data_file, index=False)

# Mood tracker UI
st.title("🌈 Mood Tracker App")

# Mood input
mood_options = ["😀 Happy", "😊 Content", "😐 Neutral", "😔 Sad", "😡 Angry"]
selected_mood = st.selectbox("How are you feeling today?", mood_options)
notes = st.text_area("Notes (optional)")

# date format 
today_date = datetime.date.today().strftime("%d-%m-%Y")

data = load_data()

if st.button("Save Entry"):
    new_entry = pd.DataFrame({"Date": [today_date], "Mood": [selected_mood], "Notes": [notes]})
    data = pd.concat([data, new_entry], ignore_index=True)
    save_data(data)
    st.success("Mood entry saved!")

# Display mood history
st.subheader("📅 Mood History")
st.dataframe(data.sort_values(by="Date", ascending=False))

# Mood trend visualization
st.subheader("📊 Mood Trends")
if not data.empty:
    mood_counts = data["Mood"].value_counts()
    st.bar_chart(mood_counts)
