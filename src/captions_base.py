from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

def generate_captions(transcript: str) -> list[str]:
    """
    Baseline (Condition A): Transcript-only caption generation.
    Returns exactly 2 captions.
    """
    transcript = (transcript or "").strip()
    if not transcript:
        return ["(No transcript found)", "(Try a clearer clip)"]

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "developer",
                "content": (
                    "You write concise, authentic Instagram-style captions from conversation transcripts. "
                    "Avoid generic motivational language. Keep it natural and human."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Return EXACTLY 2 captions.\n"
                    "Caption 1: reflective (1–3 sentences)\n"
                    "Caption 2: short/punchy (1 sentence)\n\n"
                    f"TRANSCRIPT:\n{transcript}"
                ),
            },
        ],
    )

    text = (resp.output_text or "").strip()

    # Try to parse labeled output first
    cap1 = cap2 = None
    for line in text.splitlines():
        if line.lower().startswith("caption 1:"):
            cap1 = line.split(":", 1)[1].strip()
        elif line.lower().startswith("caption 2:"):
            cap2 = line.split(":", 1)[1].strip()

    # Fallback if model didn't follow labels
    if not cap1 or not cap2:
        parts = [p.strip() for p in text.splitlines() if p.strip()]
        cap1 = parts[0] if parts else "One small moment from today."
        cap2 = parts[1] if len(parts) > 1 else "Just sharing a thought."

    return [cap1, cap2]
