import streamlit as st

def convert_units(value, unit_from, unit_to):
    conversions = {
        # Distance conversions
        "meter_kilometer": 0.001,
        "kilometer_meter": 1000,
        "mile_kilometer": 1.60934,
        "kilometer_mile": 0.621371,
        "meter_meter": 1,
        "kilometer_kilometer": 1,
        "mile_mile": 1,
        
        # Weight conversions
        "gram_kilogram": 0.001,
        "kilogram_gram": 1000,
        "pound_kilogram": 0.453592,
        "kilogram_pound": 2.20462,
        "gram_gram": 1,
        "kilogram_kilogram": 1,
        "pound_pound": 1,
        
        # Temperature conversions
        "celsius_fahrenheit": lambda c: (c * 9/5) + 32,
        "fahrenheit_celsius": lambda f: (f - 32) * 5/9,
        "celsius_kelvin": lambda c: c + 273.15,
        "kelvin_celsius": lambda k: k - 273.15,
        "celsius_celsius": lambda c: c,
        "fahrenheit_fahrenheit": lambda f: f,
        "kelvin_kelvin": lambda k: k
    }
  
    key = f"{unit_from}_{unit_to}"

    if key in conversions:
        conversion = conversions[key]
        if callable(conversion):  # for temperature formulas
            return conversion(value)
        else:
            return value * conversion
    else:
        return "Conversion not Supported"

st.title("Unit Converter")

conversion_type = st.selectbox("Select conversion type:", ["Distance", "Weight", "Temperature"])

options = {
    "Distance": ["meter", "kilometer", "mile"],
    "Weight": ["gram", "kilogram", "pound"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"]
}

value = st.number_input("Enter the Value to Convert",step=1, min_value=1,placeholder="Enter the Number")

unit_from = st.selectbox("Convert from:", options[conversion_type])
unit_to = st.selectbox("Convert to:", options[conversion_type])

if st.button("Convert"):
    result = convert_units(value, unit_from, unit_to)
    st.write(f"Converted Value: {result}")
