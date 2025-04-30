import streamlit as st
import os
import requests

# Retrieve Groq API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define the model to use
MODEL_ID = "llama2-70b"

def get_diagnosis(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": (
                "You are a mechanical engineering assistant specializing in diagnosing machine failures. "
                "When given a description of a mechanical issue, provide:\n"
                "- Possible Cause\n"
                "- Recommended Fix\n"
                "- Tools Needed\n"
                "Ensure the response is concise and informative."
            )},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="Failure Diagnosis Bot", layout="centered")
st.title("🛠️ Failure Diagnosis Bot")
st.write("Describe the mechanical issue you're experiencing:")

user_input = st.text_area("Your Input", height=150)

if st.button("Diagnose"):
    if not GROQ_API_KEY:
        st.error("API key not set. Please set your GROQ_API_KEY as an environment variable or in secrets.")
    elif user_input.strip() == "":
        st.warning("Please enter a description of the issue.")
    else:
        with st.spinner("Analyzing..."):
            diagnosis = get_diagnosis(user_input)
        st.success("Diagnosis:")
        st.markdown(diagnosis)
