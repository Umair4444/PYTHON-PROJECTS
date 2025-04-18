import streamlit as st
from data import quiz_data


# Configure Streamlit page
st.set_page_config(page_title="📝 Quiz App", layout="wide")
st.title("📝 Fun Quiz App")
st.write("Test your knowledge with this interactive quiz!")


# Store user answers in session state
if "responses" not in st.session_state:
    st.session_state.responses = {}

# Display questions
for idx, q in enumerate(quiz_data):
    st.subheader(f"Q{idx+1}: {q['question']}")
    selected_option = st.radio(
        f"Choose an answer for Q{idx+1}:",
        q["options"],
        key=f"question_{idx}"
    )
    st.session_state.responses[idx] = selected_option

# Submit button
if st.button("Submit Quiz"):
    score = 0
    st.subheader("📊 Quiz Results")
    for idx, q in enumerate(quiz_data):
        user_answer = st.session_state.responses[idx]
        correct_answer = q["answer"]
        if user_answer == correct_answer:
            score += 1
            st.success(f"✅ Q{idx+1}: Correct! ({correct_answer})")
        else:
            st.error(f"❌ Q{idx+1}: Incorrect! The correct answer is {correct_answer}")

    st.write(f"🎯 **Your Score: {score}/{len(quiz_data)}**")
