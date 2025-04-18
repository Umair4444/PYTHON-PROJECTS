import streamlit as st

def calculator():
    st.title("🧮 Mathematical Calculator")
    st.write("Solve math problems instantly!")

    # Input Fields
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("Enter first number:", value=0)
    with col2:
        num2 = st.number_input("Enter second number:", value=0)

    # Operation Selection
    operation = st.selectbox("Choose Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (x)", "Division (/)"])

    # Calculation Logic
    if st.button("Calculate"):
        try:
            if operation == "Addition (+)":
                result = num1 + num2
                symbol = "+"
            elif operation == "Subtraction (-)":
                result = num1 - num2
                symbol = "-"
            elif operation == "Multiplication (x)":
                result = num1 * num2
                symbol = "×"
            elif operation == "Division (/)":
                if num2 == 0:
                    st.error("❌ Error: Division by zero is not possible!")
                    return
                result = num1 / num2
                symbol = "÷"
            else:
                st.error("Invalid operation selected")
                return

            # Display Result
            st.success(f"✅ **Result:** {num1} {symbol} {num2} = {result}")

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Run the calculator
if __name__ == "__main__":
    calculator()
