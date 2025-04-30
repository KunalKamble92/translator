import streamlit as st
import requests

# ---- Page Config ----
st.set_page_config(page_title="Cloud Translator", layout="centered")
API_TOKEN = "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"  
headers = {"Authorization": f"Bearer {API_TOKEN}"}
# ---- API URL Template ----
API_URL = "https://api-inference.huggingface.co/models/{}"
language_models = {
    "English to French": "Helsinki-NLP/opus-mt-en-fr",
    "English to German": "Helsinki-NLP/opus-mt-en-de",
    "English to Hindi": "Helsinki-NLP/opus-mt-en-hi",
    "French to English": "Helsinki-NLP/opus-mt-fr-en",
    "German to English": "Helsinki-NLP/opus-mt-de-en",
    "Hindi to English": "Helsinki-NLP/opus-mt-hi-en",
}

# ---- App UI ----
st.title("🌐 Cloud-based Language Translator")

selected_pair = st.selectbox("Select Translation Direction", list(language_models.keys()))
input_text = st.text_area("Enter text to translate", height=150)

# ---- Translation Request Function ----
def query(payload, model):
    try:
        response = requests.post(API_URL.format(model), headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Unauthorized: Check your Hugging Face token.")
        elif response.status_code == 503:
            st.error("Model is loading on Hugging Face. Please wait a moment and try again.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
        return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

# ---- Run Translation ----
if st.button("Translate"):
    if input_text.strip():
        with st.spinner("Translating..."):
            output = query({"inputs": input_text}, language_models[selected_pair])
            if output and isinstance(output, list) and "translation_text" in output[0]:
                translated = output[0]["translation_text"]
                st.text_area("Translated Text", translated, height=150)
            elif output:
                st.error("Unexpected response format.")
    else:
        st.warning("Please enter text to translate.")