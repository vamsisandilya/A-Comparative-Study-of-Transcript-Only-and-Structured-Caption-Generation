import streamlit as st


st.set_page_config(page_title="Conversation to Caption"", layout="centered")

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
            captions = generate_captions(transcript)

        st.subheader("Transcript")
        st.text_area("Transcript", transcript, height=200)

        st.subheader("Suggested Captions")
        for i, cap in enumerate(captions, start=1):
            st.markdown(f"**Caption {i}:** {cap}")

