import json
from typing import Any, Dict, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv

from captions_base import generate_captions


load_dotenv()
client = OpenAI()

DEFAULT_TEMPERATURE = 0.2

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

ALLOWED_INTENTS: List[str] = [
    "sharing_experience",
    "self_reflection",
    "motivational_statement",
    "storytelling",
    "venting",
    "celebration",
    "advice",
    "observation",
    "request_help",
    "humor_playful",
]

ALLOWED_SARCASM: List[str] = ["low", "medium", "high", "unknown"]

TONE_JSON_SCHEMA: Dict[str, Any] = {
    "name": "tone_analysis",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "primary_emotion": {"type": "string"},
            "secondary_emotions": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 3,
            },
            "intensity": {"type": "integer", "minimum": 0, "maximum": 3},
            "sarcasm_likelihood": {"type": "string", "enum": ALLOWED_SARCASM},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "intent": {"type": "string"},
            "themes": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
            "evidence": {"type": "string"},
        },
        "required": [
            "primary_emotion",
            "secondary_emotions",
            "intensity",
            "sarcasm_likelihood",
            "confidence",
            "intent",
            "themes",
            "evidence",
        ],
    },
}

def _safe_empty_tone() -> Dict[str, Any]:
    return {
        "primary_emotion": "neutral",
        "secondary_emotions": [],
        "intensity": 0,
        "sarcasm_likelihood": "unknown",
        "confidence": 0.0,
        "intent": "observation",
        "themes": [],
        "evidence": "",
    }


def _sanitize_tone(data: Any) -> Dict[str, Any]:
    """
    Validate + sanitize to keep the app stable and outputs comparable.
    """
    if not isinstance(data, dict):
        return _safe_empty_tone()

    primary = data.get("primary_emotion", "neutral")
    if primary not in ALLOWED_EMOTIONS:
        primary = "neutral"

    secondary = data.get("secondary_emotions", [])
    if not isinstance(secondary, list):
        secondary = []
    secondary = [
        e for e in secondary
        if e in ALLOWED_EMOTIONS and e != primary and e != "neutral"
    ]

    # Deduplicate, preserve order, max 3
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
    if sarcasm not in ALLOWED_SARCASM:
        sarcasm = "unknown"

    confidence = data.get("confidence", 0.0)
    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))

    intent = data.get("intent", "observation")
    if not isinstance(intent, str):
        intent = "observation"
    intent = intent.strip()
    if intent not in ALLOWED_INTENTS:
        # Conservative fallback if model invents something
        intent = "observation"

    themes = data.get("themes", [])
    if not isinstance(themes, list):
        themes = []
    # Short noun phrases only; clamp length
    cleaned_themes = []
    for t in themes:
        s = str(t).strip()
        if not s:
            continue
        # Keep it compact for stability
        cleaned_themes.append(s[:40])
    themes = cleaned_themes[:5]

    evidence = data.get("evidence", "")
    if not isinstance(evidence, str):
        evidence = ""
    evidence = evidence.strip()[:200]

    # Tiny heuristic: if sarcasm is "high" and intensity is 0, bump to 1
    if sarcasm == "high" and intensity == 0:
        intensity = 1

    return {
        "primary_emotion": primary,
        "secondary_emotions": secondary,
        "intensity": intensity,
        "sarcasm_likelihood": sarcasm,
        "confidence": confidence,
        "intent": intent[:80],
        "themes": themes,
        "evidence": evidence,
    }


def _tone_block(tone: Dict[str, Any]) -> str:
    secondary = ", ".join(tone.get("secondary_emotions", [])) or "none"
    themes = ", ".join(tone.get("themes", [])) or "none"
    evidence = tone.get("evidence", "").replace("\n", " ").strip()
    return (
        f"primary_emotion: {tone.get('primary_emotion', 'neutral')}\n"
        f"secondary_emotions: {secondary}\n"
        f"intensity: {tone.get('intensity', 0)}\n"
        f"sarcasm_likelihood: {tone.get('sarcasm_likelihood', 'unknown')}\n"
        f"confidence: {tone.get('confidence', 0.0)}\n"
        f"intent: {tone.get('intent', 'observation')}\n"
        f"themes: {themes}\n"
        f"evidence: \"{evidence}\"\n"
    )


def _responses_create_with_optional_json_schema(model: str, input_messages: List[Dict[str, str]], temperature: float = 0.2,) -> Tuple[str, bool]:
    """
    Tries to enforce JSON schema output if your SDK supports it.
    Falls back to normal text if not supported.

    Returns (output_text, used_schema_bool)
    """
    try:
        resp = client.responses.create(
            model=model,
            temperature=DEFAULT_TEMPERATURE,
            input=input_messages,
            text={
                "format": {
                    "type": "json_schema",
                    "json_schema": TONE_JSON_SCHEMA,
                }
            },
        )
        return (resp.output_text or "").strip(), True
    except TypeError:
        # SDK doesn't support text.format (older/newer shape)
        resp = client.responses.create(model=model, temperature=temperature, input=input_messages)
        return (resp.output_text or "").strip(), False
    except Exception:
        # Any other failure: fallback call without schema
        resp = client.responses.create(model=model, temperature=temperature, input=input_messages)
        return (resp.output_text or "").strip(), False


def analyze_tone(transcript: str) -> dict:
    """
    Text-only structured conversational signal extraction.
    Emotion + intensity + sarcasm + intent + themes + evidence + confidence.

    Outputs stable labels from ALLOWED_EMOTIONS / ALLOWED_INTENTS.
    """
    transcript = (transcript or "").strip()
    if not transcript:
        return _safe_empty_tone()

    emotion_list_str = ", ".join(ALLOWED_EMOTIONS)
    intent_list_str = ", ".join(ALLOWED_INTENTS)

    developer_msg = (
        "You are a structured conversational signal extractor (Level 1, text-only). "
        "Be conservative: do NOT over-infer emotion. "
        "If evidence is weak or mixed, choose primary_emotion='neutral' and keep intensity low (0 or 1). "
        "Sarcasm should be 'unknown' unless there are clear textual cues (obvious irony/contradiction). "
        "Output MUST be valid JSON only and match the required schema exactly."
    )

    user_msg = (
        "Return JSON with EXACTLY this schema:\n"
        "{\n"
        '  "primary_emotion": one_of_allowed_emotions,\n'
        '  "secondary_emotions": [0_to_3_allowed_emotions_distinct_from_primary],\n'
        '  "intensity": 0|1|2|3,\n'
        '  "sarcasm_likelihood": "low"|"medium"|"high"|"unknown",\n'
        '  "confidence": number_0_to_1,\n'
        '  "intent": one_of_allowed_intents,\n'
        '  "themes": [0_to_5_short_noun_phrases],\n'
        '  "evidence": exact_quote_from_transcript\n'
        "}\n\n"
        f"Allowed emotions: {emotion_list_str}\n"
        f"Allowed intents: {intent_list_str}\n\n"
        "Rules:\n"
        "- primary_emotion MUST be exactly one item from Allowed emotions.\n"
        "- secondary_emotions: 0–3 items, from Allowed emotions, no duplicates, not equal to primary.\n"
        "- intensity: 0=flat, 1=mild, 2=moderate, 3=strong.\n"
        "- sarcasm_likelihood: use 'unknown' unless clear sarcasm/irony is present.\n"
        "- themes: short noun phrases only (1–4 words each). No sentences.\n"
        "- evidence MUST be an exact quote copied from the transcript (max 1 sentence, <=200 chars).\n"
        "- confidence reflects certainty from text only.\n"
        "- Return JSON ONLY.\n\n"
        "Transcript:\n"
        f"{transcript}"
    )

    raw, _used_schema = _responses_create_with_optional_json_schema(
        model="gpt-4o-mini",
        temperature=DEFAULT_TEMPERATURE,
        input_messages=[
            {"role": "developer", "content": developer_msg},
            {"role": "user", "content": user_msg},
        ],
    )

    # Parse JSON robustly
    try:
        data = json.loads(raw)
        return _sanitize_tone(data)
    except Exception:
        # Safe fallback if JSON fails
        fallback = _safe_empty_tone()
        fallback["confidence"] = 0.2
        fallback["evidence"] = raw[:200]
        return fallback


def generate_captions_structured(transcript: str) -> list[str]:
    """
    Condition A: Baseline transcript-only caption generation.
    Returns EXACTLY 2 captions.
    """
    transcript = (transcript or "").strip()
    if not transcript:
        return ["(No transcript found)", "(Try a clearer clip)"]
    tone = analyze_tone(transcript)
    tone_block = _tone_block(tone)
    resp = client.responses.create(
        model="gpt-4o-mini",
        temperature=DEFAULT_TEMPERATURE,
        input=[
            {
                "role": "developer",
                "content": (
                    "You write concise, authentic Instagram-style captions from conversation transcripts. "
                    "Use the structured tone block as an intermediate representation to guide tone and subtext. "
                    "Avoid generic motivational language. "
                    "Return exactly 2 captions with the required format."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Return EXACTLY 2 captions.\n"
                    "Caption 1: reflective (1–3 sentences)\n"
                    "Caption 2: short/punchy (1 sentence)\n\n"
                    "STRUCTURED_TONE_BLOCK:\n"
                    f"{tone_block}\n"
                    f"TRANSCRIPT:\n{transcript}"
                ),
            },
        ],
    )

    return _parse_two_captions(resp.output_text or "")


def _parse_two_captions(text: str) -> List[str]:
    """
    Parses the model output into exactly 2 captions.
    Prefers 'Caption 1:' and 'Caption 2:' markers, but falls back safely.
    """
    text = (text or "").strip()
    if not text:
        return ["A small moment, a real feeling.", "Keeping it real."]

    cap1 = None
    cap2 = None

    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        lower = s.lower()
        if lower.startswith("caption 1:"):
            cap1 = s.split(":", 1)[1].strip()
        elif lower.startswith("caption 2:"):
            cap2 = s.split(":", 1)[1].strip()

    if cap1 and cap2:
        return [cap1, cap2]

    # Fallback: take first two non-empty lines
    parts = [p.strip() for p in text.splitlines() if p.strip()]
    if len(parts) >= 2:
        return [parts[0], parts[1]]

    # Final fallback: split by sentence-ish
    return [parts[0] if parts else "A small moment, a real feeling.", "Keeping it real."]


if __name__ == "__main__":
    sample = "I thought I’d be fine with it, but honestly it still stings a little. Maybe I just need more time."
    tone = analyze_tone(sample)
    print("TONE JSON:\n", json.dumps(tone, indent=2, ensure_ascii=False))
    print("\nSTRUCTURED:\n", generate_captions_structured(sample))

