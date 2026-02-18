import json
from captions_base import generate_captions as generate_captions_baseline
from captions_emotion import analyze_tone, generate_captions_structured

if __name__ == "__main__":
    sample = "I thought I’d be fine with it, but honestly it still stings a little. Maybe I just need more time."

    tone = analyze_tone(sample)
    print("TONE JSON:\n", json.dumps(tone, indent=2, ensure_ascii=False))

    print("\nBASELINE:\n", generate_captions_baseline(sample))
    print("\nSTRUCTURED:\n", generate_captions_structured(sample))
