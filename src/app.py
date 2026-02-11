import streamlit as st

st.set_page_config(page_title="Conversation to Instagram Post")

st.title("Conversation → Instagram Post Prototype")

st.write(
    "Upload a short audio clip. This prototype will later convert speech to text "
    "and suggest Instagram-style post captions."
)

uploaded_file = st.file_uploader(
    "Upload an audio file (wav, mp3, m4a)",
    type=["wav", "mp3", "m4a"]
)

if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")
    st.write("Next step: speech-to-text and caption generation.")
