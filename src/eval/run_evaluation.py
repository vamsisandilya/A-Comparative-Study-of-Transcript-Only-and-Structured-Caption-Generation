import os
from src.stt import transcribe_audio

AUDIO_FOLDER = "data/eval_audio"
OUTPUT_FOLDER = "data/eval_outputs"
TRANSCRIPT_FOLDER = os.path.join(OUTPUT_FOLDER, "transcripts")
AUDIO_EXTS = (".wav", ".mp3", ".m4a")


def get_audio_files():
    if not os.path.isdir(AUDIO_FOLDER):
        raise FileNotFoundError(f"Missing input folder: {AUDIO_FOLDER}")
    return sorted(
        f for f in os.listdir(AUDIO_FOLDER)
        if f.lower().endswith(AUDIO_EXTS)
    )


def save_transcript(stem: str, text: str):
    os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
    path = os.path.join(TRANSCRIPT_FOLDER, f"{stem}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # minimal, necessary
    files = get_audio_files()
    if not files:
        print("No audio files found.")
        return
    first_file = files[0]
    audio_path = os.path.join(AUDIO_FOLDER, first_file)
    print(f"Transcribing {first_file}...")
    transcript = transcribe_audio(audio_path)

    stem = os.path.splitext(first_file)[0]
    save_transcript(stem, transcript)

    print("Transcript saved.")


if __name__ == "__main__":
    main()