import streamlit as st
import tempfile
from stt import transcribe_audio
from captions_base import generate_captions as generate_baseline
from captions_emotion import generate_captions as generate_emotion

st.set_page_config(page_title="Conversation to Caption", layout="centered")

st.title("Conversation → Instagram Post Prototype")

st.write(
    "Upload a short conversational audio clip to generate "
    "Instagram-style captions using two approaches:"
)

st.markdown(
    "- **Baseline:** Transcript-only generation  \n"
    "- **Structured Emotion-Guided:** Uses inferred emotional metadata"
)

uploaded_file = st.file_uploader(
    "Upload an audio file (wav, mp3, m4a)",
    type=["wav", "mp3", "m4a"]
)

if uploaded_file is not None:
    st.audio(uploaded_file)

    if st.button("Process Audio"):
        with st.spinner("Transcribing and generating captions..."):
            # Save temp audio file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                temp_audio_path = tmp.name

            # Speech to text
            transcript = transcribe_audio(temp_audio_path)

            # Caption generation
            baseline_captions = generate_baseline(transcript)
            emotion_captions = generate_emotion(transcript)

        st.subheader("Transcript")
        st.text_area("Transcript", transcript, height=200)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Suggested Captions")
            for i, cap in enumerate(baseline_captions, start=1):
                st.markdown(f"**Caption {i}:** {cap}")

        with col2:
            st.subheader("Structured Emotion-Guided")
            for i, cap in enumerate(emotion_captions, start=1):
                st.markdown(f"**Caption {i}:** {cap}")