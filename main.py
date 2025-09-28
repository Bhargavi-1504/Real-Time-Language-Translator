import streamlit as st
from googletrans import Translator, LANGUAGES

# Initialize Translator
translator = Translator()

# Streamlit App
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🌐 Language Translator App</h1>",
    unsafe_allow_html=True,
)

st.markdown("This app allows you to translate text between different languages using Google Translate.")

# Sidebar for Language Settings
st.sidebar.header("Language Settings")
# Source Language Selection (added 'auto' for auto-detection)
src_lang = st.sidebar.selectbox(
    "Select source language:",
    ["auto"] + sorted(LANGUAGES.keys()),
    index=0
)

dest_lang = st.sidebar.selectbox(
    "Select target language:",
    sorted(LANGUAGES.keys()),
    index=21  # default 'en'
)

# Text Input
input_text = st.text_area("Enter text to translate:")

# Translate Button
if st.button("Translate"):
    if input_text.strip():
        try:
            result = translator.translate(input_text, src=src_lang, dest=dest_lang)
            if src_lang == "auto":
                detected_lang = LANGUAGES.get(result.src, "Unknown")
                st.info(f"Detected Source Language: **{detected_lang.title()}**")
            st.success("Translated Text:")
            st.write(result.text)
        except Exception as e:
            st.error(f"An error occurred during translation: {e}")
    else:
        st.warning("Please enter some text to translate.")

# Footer
st.markdown(
    "<hr><center>Powered by Google Translate via `googletrans`</center>",
    unsafe_allow_html=True,
)
