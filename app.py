import streamlit as st
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import os
from pydub import AudioSegment
import tempfile

# 🔊 Offline fallback with pyttsx3 + pydub
def save_offline_tts(text, audio_file):
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    engine = pyttsx3.init()
    engine.save_to_file(text, temp_wav.name)
    engine.runAndWait()
    engine.stop()

    # Convert WAV to MP3 for Streamlit
    sound = AudioSegment.from_wav(temp_wav.name)
    sound.export(audio_file, format="mp3")
    temp_wav.close()


# Initialize translator and recognizer
translator = Translator()
recognizer = sr.Recognizer()

# Initialize session state for input text
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# App title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌐 Language Translator with Speech Input & Audio Output</h1>", unsafe_allow_html=True)

# Sidebar language selection
st.sidebar.header("Language Settings")
src_lang = st.sidebar.selectbox("Select source language:", ["auto"] + sorted(LANGUAGES.keys()))
dest_lang = st.sidebar.selectbox("Select target language:", sorted(LANGUAGES.keys()), index=21)

# Text input area (linked to session_state)
st.session_state.input_text = st.text_area("Enter text or use the microphone input", st.session_state.input_text)

# 🎙 Microphone input section
if st.button("🎙 Record Audio"):
    try:
        with sr.Microphone() as source:
            st.info("Recording... Please speak now")
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source, timeout=5)
            recognized_text = recognizer.recognize_google(audio_data)
            st.success("✅ Speech recognized!")
            st.session_state.input_text = recognized_text  # Save in session state
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
    except Exception as e:
        st.error(f"Error: {e}")

# 🔄 Translation logic
if st.button("🔄 Translate"):
    if st.session_state.input_text.strip():
        try:
            result = translator.translate(st.session_state.input_text, src=src_lang, dest=dest_lang)
            detected_language = LANGUAGES.get(result.src, "Unknown").title()
            target_language = LANGUAGES.get(dest_lang, dest_lang).title()
            
            st.success("✅ Translation Successful!")
            st.write(f"**Detected Source Language:** {detected_language}")
            st.write(f"**Target Language:** {target_language}")
            st.text_area("Translated Text", result.text)

            # 🔊 Audio output section (indented inside try:)
            audio_file = "translated_output.mp3"

            # List of languages supported by gTTS (you can expand if needed)
            gtts_supported_langs = [
                "en", "es", "fr", "de", "hi", "it", "pt", "ru", "zh-cn", "ja", "ko", "te", "ta"
            ]

            if dest_lang in gtts_supported_langs:
                try:
                    tts = gTTS(text=result.text, lang=dest_lang, slow=False)
                    tts.save(audio_file)
                    st.audio(audio_file, format="audio/mp3")
                    st.download_button("📥 Download Audio", data=open(audio_file, "rb"),
                                       file_name="translated_output.mp3", mime="audio/mp3")
                except Exception as e:
                    st.warning(f"⚠️ gTTS failed: {e}, falling back to offline TTS...")
                    engine = pyttsx3.init()
                    engine.save_to_file(result.text, audio_file)
                    engine.runAndWait()
                    st.audio(audio_file, format="audio/mp3")
                    st.download_button("📥 Download Audio", data=open(audio_file, "rb"),
                                       file_name="translated_output.mp3", mime="audio/mp3")
            else:
                st.info(f"ℹ️ gTTS does not support `{dest_lang}`, using offline voice...")
                engine = pyttsx3.init()
                engine.save_to_file(result.text, audio_file)
                engine.runAndWait()
                st.audio(audio_file, format="audio/mp3")
                st.download_button("📥 Download Audio", data=open(audio_file, "rb"),
                                   file_name="translated_output.mp3", mime="audio/mp3")

        except Exception as e:   # <-- matches the try: at top of translate block
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter or record some text to translate")



