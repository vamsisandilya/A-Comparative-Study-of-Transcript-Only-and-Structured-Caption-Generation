import os
import csv
import random
from src.stt import transcribe_audio
from src.captions_base import generate_captions as generate_baseline
from src.captions_emotion import generate_captions_structured

AUDIO_FOLDER = "data/eval_audio"
OUTPUT_FOLDER = "data/eval_outputs"
TRANSCRIPT_FOLDER = os.path.join(OUTPUT_FOLDER, "transcripts")
AUDIO_EXTS = (".wav", ".mp3", ".m4a")
BASELINE_FOLDER = os.path.join(OUTPUT_FOLDER, "baseline")
STRUCTURED_FOLDER = os.path.join(OUTPUT_FOLDER, "structured")
PACKETS_FOLDER = os.path.join(OUTPUT_FOLDER, "packets")
MAPPING_FILE = os.path.join(OUTPUT_FOLDER, "xy_mapping.csv")

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


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


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

    for audio_file in files:
        stem = os.path.splitext(audio_file)[0]
        transcript = load_transcript(stem)

        structured_out_path = os.path.join(STRUCTURED_FOLDER, f"{stem}.txt")
        if os.path.exists(structured_out_path):
            print(f"Skipping structured captions for {audio_file} (already exists)")
            continue

        print(f"Generating structured captions for {audio_file}...")
        structured_captions = generate_captions_structured(transcript)
        structured_text = format_captions(structured_captions)
        save_text(STRUCTURED_FOLDER, stem, structured_text)
        print(f"Structured captions saved for {audio_file}")

    os.makedirs(PACKETS_FOLDER, exist_ok=True)

    if not os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["clip", "X_condition", "Y_condition"])

    for audio_file in files:
        stem = os.path.splitext(audio_file)[0]

        transcript_path = os.path.join(TRANSCRIPT_FOLDER, f"{stem}.txt")
        baseline_path = os.path.join(BASELINE_FOLDER, f"{stem}.txt")
        structured_path = os.path.join(STRUCTURED_FOLDER, f"{stem}.txt")

        if not (os.path.exists(transcript_path) and os.path.exists(baseline_path) and os.path.exists(structured_path)):
            print(f"Skipping packet for {audio_file} (missing outputs)")
            continue

        packet_stem = f"{stem}_packet"
        packet_path = os.path.join(PACKETS_FOLDER, f"{packet_stem}.txt")
        if os.path.exists(packet_path):
            print(f"Skipping packet for {audio_file} (packet already exists)")
            continue

        transcript = load_text(transcript_path)
        baseline_txt = load_text(baseline_path)
        structured_txt = load_text(structured_path)


        if random.random() < 0.5:
            x_label, y_label = "baseline", "structured"
            x_txt, y_txt = baseline_txt, structured_txt
        else:
            x_label, y_label = "structured", "baseline"
            x_txt, y_txt = structured_txt, baseline_txt

        packet_contents = (
            f"CLIP: {stem}\n\n"
            "TRANSCRIPT:\n"
            f"{transcript}\n\n"
            "SET X:\n"
            f"{x_txt}\n\n"
            "SET Y:\n"
            f"{y_txt}\n"
        )

        save_text(PACKETS_FOLDER, packet_stem, packet_contents)

        with open(MAPPING_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([stem, x_label, y_label])

        print(f"Evaluator packet saved for {audio_file}")    

if __name__ == "__main__":
    main()
