import streamlit as st
from googletrans import Translator, LANGUAGES
import pandas as pd

# Initialize Translator
translator = Translator()

# Initialize Session State for History
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar Branding
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/910/910421.png", width=100)
st.sidebar.title("🌟 Language Translator")
st.sidebar.markdown("Made with ❤️ by [Your Name]")

# Language Settings in Sidebar
st.sidebar.header("🌐 Language Settings")
src_lang = st.sidebar.selectbox(
    "Select Source Language:",
    ["auto"] + sorted(LANGUAGES.keys())
)
dest_lang = st.sidebar.selectbox(
    "Select Target Language:",
    sorted(LANGUAGES.keys()),
    index=21  # Default English
)

# App Header
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🚀 Fancy Language Translator App</h1>",
    unsafe_allow_html=True,
)

# Input Section
st.subheader("✍️ Enter the Text to Translate")
input_text = st.text_area("Input Text Here:")

# Translate Button with Columns
col1, col2 = st.columns(2)
with col1:
    translate_btn = st.button("🔄 Translate")
with col2:
    clear_btn = st.button("🗑️ Clear History")

# Translation Logic
if translate_btn:
    if input_text.strip():
        try:
            result = translator.translate(input_text, src=src_lang, dest=dest_lang)
            detected_lang = LANGUAGES.get(result.src, "Unknown")
            
            # Display Result
            st.success("✅ Translation Successful!")
            st.write(f"**Translated Text:** {result.text}")
            if src_lang == "auto":
                st.info(f"Detected Language: **{detected_lang.title()}**")

            # Save History
            st.session_state.history.append({
                "Input Text": input_text,
                "Source Language": detected_lang if src_lang == "auto" else LANGUAGES.get(src_lang, src_lang).title(),
                "Target Language": LANGUAGES.get(dest_lang, dest_lang).title(),
                "Translated Text": result.text
            })
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter some text.")

# Clear History Button
if clear_btn:
    st.session_state.history.clear()
    st.info("🗑️ History Cleared.")

# Translation History Table
if st.session_state.history:
    st.markdown("### 📜 Translation History")
    st.dataframe(pd.DataFrame(st.session_state.history))

    # CSV Download
    csv_data = pd.DataFrame(st.session_state.history).to_csv(index=False)
    st.download_button("📥 Download History as CSV", data=csv_data, file_name="translation_history.csv", mime="text/csv")

