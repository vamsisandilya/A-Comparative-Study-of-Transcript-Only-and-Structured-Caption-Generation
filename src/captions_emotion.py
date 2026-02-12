# captions.py (replace ONLY analyze_tone with this version)
import json
from openai import OpenAI

client = OpenAI()

ALLOWED_EMOTIONS = [
    "joy",
    "sadness",
    "anger",
    "fear_anxiety",
    "disgust",
    "surprise",
    "shame",
    "guilt",
    "embarrassment",
    "pride",
    "love_affection",
    "gratitude",
    "frustration",
    "stress_overwhelm",
    "confusion",
    "hope_optimism",
    "loneliness",
    "insecurity",
    "neutral",
]

def analyze_tone(transcript: str) -> dict:
    """
    Level 1: Text-only emotion + sarcasm + intent analysis.
    Outputs stable labels from ALLOWED_EMOTIONS, plus intensity and confidence.
    """
    transcript = (transcript or "").strip()
    if not transcript:
        return {
            "primary_emotion": "neutral",
            "secondary_emotions": [],
            "intensity": 0,
            "sarcasm_likelihood": "unknown",
            "confidence": 0.0,
            "intent": "unknown",
            "themes": [],
            "evidence": ""
        }

    emotion_list_str = ", ".join(ALLOWED_EMOTIONS)

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "developer",
                "content": (
                    "You are a careful analyst of conversational text. "
                    "Infer emotional tone and sarcasm conservatively. "
                    "You MUST output ONLY valid JSON with the exact schema and constraints. "
                    "If unsure, choose primary_emotion='neutral', sarcasm_likelihood='low' or 'unknown', "
                    "and set confidence low."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Analyze the transcript and return JSON with EXACTLY this schema:\n"
                    "{\n"
                    '  "primary_emotion": one_of_allowed_emotions,\n'
                    '  "secondary_emotions": [up_to_3_allowed_emotions_distinct_from_primary],\n'
                    '  "intensity": integer_0_to_3,\n'
                    '  "sarcasm_likelihood": "low"|"medium"|"high"|"unknown",\n'
                    '  "confidence": number_0_to_1,\n'
                    '  "intent": short_string,\n'
                    '  "themes": [up_to_5_short_strings],\n'
                    '  "evidence": short_quote_or_paraphrase_from_transcript\n'
                    "}\n\n"
                    f"Allowed emotions (choose ONLY from this list): {emotion_list_str}\n\n"
                    "Rules:\n"
                    "- primary_emotion MUST be exactly one item from the allowed list.\n"
                    "- secondary_emotions MUST be 0–3 items, from the allowed list, no duplicates, and not equal to primary.\n"
                    "- intensity: 0=none/flat, 1=mild, 2=moderate, 3=strong.\n"
                    "- sarcasm_likelihood should be 'unknown' if there isn't clear textual evidence.\n"
                    "- confidence should reflect how certain you are based on the words alone.\n"
                    "- Return JSON ONLY (no markdown, no extra text).\n\n"
                    "Transcript:\n"
                    f"{transcript}"
                ),
            },
        ],
    )

    raw = (resp.output_text or "").strip()

    # Parse JSON robustly
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("Not a JSON object")

        # Validate & sanitize to keep app stable
        primary = data.get("primary_emotion", "neutral")
        if primary not in ALLOWED_EMOTIONS:
            primary = "neutral"

        secondary = data.get("secondary_emotions", [])
        if not isinstance(secondary, list):
            secondary = []
        secondary = [e for e in secondary if e in ALLOWED_EMOTIONS and e != primary]
        # remove duplicates while preserving order
        seen = set()
        secondary_clean = []
        for e in secondary:
            if e not in seen:
                seen.add(e)
                secondary_clean.append(e)
        secondary = secondary_clean[:3]

        intensity = data.get("intensity", 0)
        try:
            intensity = int(intensity)
        except Exception:
            intensity = 0
        intensity = max(0, min(3, intensity))

        sarcasm = data.get("sarcasm_likelihood", "unknown")
        if sarcasm not in ["low", "medium", "high", "unknown"]:
            sarcasm = "unknown"

        confidence = data.get("confidence", 0.0)
        try:
            confidence = float(confidence)
        except Exception:
            confidence = 0.0
        confidence = max(0.0, min(1.0, confidence))

        intent = data.get("intent", "unknown")
        if not isinstance(intent, str):
            intent = "unknown"

        themes = data.get("themes", [])
        if not isinstance(themes, list):
            themes = []
        themes = [str(t).strip()[:40] for t in themes if str(t).strip()]
        themes = themes[:5]

        evidence = data.get("evidence", "")
        if not isinstance(evidence, str):
            evidence = ""
        evidence = evidence.strip()[:200]

        return {
            "primary_emotion": primary,
            "secondary_emotions": secondary,
            "intensity": intensity,
            "sarcasm_likelihood": sarcasm,
            "confidence": confidence,
            "intent": intent.strip()[:80],
            "themes": themes,
            "evidence": evidence,
        }

    except Exception:
        # Safe fallback if JSON fails
        return {
            "primary_emotion": "neutral",
            "secondary_emotions": [],
            "intensity": 1,
            "sarcasm_likelihood": "unknown",
            "confidence": 0.2,
            "intent": "unknown",
            "themes": [],
            "evidence": raw[:200],
        }
def generate_captions(transcript: str) -> list[str]:
    transcript = (transcript or "").strip()
    if not transcript:
        return ["(No transcript found)", "(Try a clearer clip)"]

    tone = analyze_tone(transcript)

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "developer",
                "content": (
                    "You write concise, authentic Instagram-style captions from conversation transcripts. "
                    "Match emotional subtext (including sarcasm if present). "
                    "Avoid generic motivational language."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Return EXACTLY 2 captions.\n"
                    "Caption 1: reflective (1–3 sentences)\n"
                    "Caption 2: short/punchy (1 sentence)\n\n"
                    f"TONE_ANALYSIS:\n{tone}\n\n"
                    f"TRANSCRIPT:\n{transcript}"
                ),
            },
        ],
    )

    text = (resp.output_text or "").strip()

    cap1 = cap2 = None
    for line in text.splitlines():
        if line.lower().startswith("caption 1:"):
            cap1 = line.split(":", 1)[1].strip()
        elif line.lower().startswith("caption 2:"):
            cap2 = line.split(":", 1)[1].strip()

    if not cap1 or not cap2:
        parts = [p for p in text.splitlines() if p.strip()]
        cap1 = parts[0]
        cap2 = parts[1] if len(parts) > 1 else "A small moment, a big takeaway."

    return [cap1, cap2]
