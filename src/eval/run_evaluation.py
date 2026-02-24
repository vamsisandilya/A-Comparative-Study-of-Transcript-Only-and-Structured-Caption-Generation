import os
from src.stt import transcribe_audio
from src.captions_base import generate_captions as generate_baseline


AUDIO_FOLDER = "data/eval_audio"
OUTPUT_FOLDER = "data/eval_outputs"
TRANSCRIPT_FOLDER = os.path.join(OUTPUT_FOLDER, "transcripts")
AUDIO_EXTS = (".wav", ".mp3", ".m4a")
BASELINE_FOLDER = os.path.join(OUTPUT_FOLDER, "baseline")


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
        f.write(text.rstrip() + "\n")


def load_transcript(stem: str) -> str:
    path = os.path.join(TRANSCRIPT_FOLDER, f"{stem}.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def save_text(folder: str, stem: str, text: str):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{stem}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")


def format_captions(captions) -> str:
    # captions might be list[str] or str
    if isinstance(captions, list):
        captions = [str(x).replace("**", "").strip() for x in captions if str(x).strip()]
        if len(captions) >= 2:
            return f"Caption 1: {captions[0]}\nCaption 2: {captions[1]}\n"
        if len(captions) == 1:
            return f"Caption 1: {captions[0]}\n"
        return ""
    return str(captions).replace("**", "").strip() + "\n"


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)  
    files = get_audio_files()
    if not files:
        print("No audio files found.")
        return

    for audio_file in files:
        audio_path = os.path.join(AUDIO_FOLDER, audio_file)
        stem = os.path.splitext(audio_file)[0]
        transcript_path = os.path.join(TRANSCRIPT_FOLDER, f"{stem}.txt")
        if os.path.exists(transcript_path):
            print(f"Skipping {audio_file} (transcript already exists)")
            continue
        print(f"Transcribing {audio_file}...")
        transcript = transcribe_audio(audio_path)
        save_transcript(stem, transcript)
        print(f"Transcript saved for {audio_file}")

    for audio_file in files:
        stem = os.path.splitext(audio_file)[0]
        transcript = load_transcript(stem)

        baseline_out_path = os.path.join(BASELINE_FOLDER, f"{stem}.txt")
        if os.path.exists(baseline_out_path):
            print(f"Skipping baseline captions for {audio_file} (already exists)")
            continue

        print(f"Generating baseline captions for {audio_file}...")
        baseline_captions = generate_baseline(transcript)
        baseline_text = format_captions(baseline_captions)
        save_text(BASELINE_FOLDER, stem, baseline_text)
        print(f"Baseline captions saved for {audio_file}")


if __name__ == "__main__":
    main()
