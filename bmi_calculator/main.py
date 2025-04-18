import streamlit as st

st.title("BMI Calculator 💪")

# Input fields
st.subheader("Enter your details:")
weight = st.number_input("Weight (in kg)", min_value=1.0, step=0.5)
height = st.number_input("Height (in cm)", min_value=50.0, step=1.0)

# Function to calculate BMI
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

# Interpret BMI
def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "🔵"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight", "🟢"
    elif 25 <= bmi < 29.9:
        return "Overweight", "🟠"
    else:
        return "Obesity", "🔴"

# Button to trigger BMI calculation
if st.button("Calculate BMI"):
    if weight and height:
        bmi = calculate_bmi(weight, height)
        status, emoji = interpret_bmi(bmi)
        st.success(f"Your BMI is: **{bmi}**")
        st.info(f"Category: **{status}** {emoji}")
    else:
        st.warning("Please enter both weight and height.")

