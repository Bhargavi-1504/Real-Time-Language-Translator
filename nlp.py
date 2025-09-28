import streamlit as st
from googletrans import Translator, LANGUAGES

# Initialize Translator
translator = Translator()

# Initialize session state for history (persists during the session)
if "history" not in st.session_state:
    st.session_state.history = []

# App Header
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🌐 Language Translator App with History</h1>",
    unsafe_allow_html=True,
)


# Sidebar for Language Settings
st.sidebar.header("Language Settings")
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
            detected_lang = LANGUAGES.get(result.src, "Unknown")
            st.success("Translated Text:")
            st.write(result.text)

            # Show detected language if auto-detect used
            if src_lang == "auto":
                st.info(f"Detected Source Language: **{detected_lang.title()}**")

            # Save to history
            st.session_state.history.append({
                "Input Text": input_text,
                "Source Language": detected_lang if src_lang == "auto" else LANGUAGES.get(src_lang, src_lang).title(),
                "Target Language": LANGUAGES.get(dest_lang, dest_lang).title(),
                "Translated Text": result.text
            })

        except Exception as e:
            st.error(f"An error occurred during translation: {e}")
    else:
        st.warning("Please enter some text to translate.")

# Display Translation History
if st.session_state.history:
    st.markdown("### 🕘 Translation History")
    st.dataframe(st.session_state.history)


