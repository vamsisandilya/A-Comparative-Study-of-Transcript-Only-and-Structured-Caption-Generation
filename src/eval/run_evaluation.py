import os

AUDIO_FOLDER = "data/eval_audio"
OUTPUT_FOLDER = "data/eval_outputs"
AUDIO_EXTS = (".wav", ".mp3", ".m4a")

def get_audio_files():
    if not os.path.isdir(AUDIO_FOLDER):
        raise FileNotFoundError(f"Missing input folder: {AUDIO_FOLDER}")
    return sorted(
        f for f in os.listdir(AUDIO_FOLDER)
        if f.lower().endswith(AUDIO_EXTS)
    )

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # minimal, necessary
    files = get_audio_files()
    print(f"Found {len(files)} audio files")

if __name__ == "__main__":
    main()