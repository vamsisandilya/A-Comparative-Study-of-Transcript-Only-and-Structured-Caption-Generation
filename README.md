# From Conversation to Instagram Captions  

**Master’s Project

## Project Overview

This project investigates whether adding structured conversational metadata improves the quality of AI-generated Instagram-style captions.

The system converts short conversational audio into captions using two experimental conditions:

- **Condition A (Baseline)** – Transcript-only caption generation  
- **Condition B (Structured)** – Transcript + structured conversational signal metadata  

The research goal is to evaluate whether structured tone guidance improves:

- Relevance  
- Emotional alignment  
- Subtext preservation  
- Perceived authenticity  

This is a controlled academic prototype. It is not intended for production use.


## Research Motivation

Conversational speech contains emotional nuance and implicit meaning that may not be fully captured through raw transcript text alone.

This project introduces a **Level 1 structured intermediate representation**, extracted from transcript text only:

- Primary emotion  
- Secondary emotions (0–3)  
- Emotional intensity (0–3)  
- Sarcasm likelihood  
- Communicative intent  
- Themes (short noun phrases)  
- Evidence quote (grounded in transcript)  
- Confidence score  

The hypothesis is that explicitly conditioning generation on structured signals may produce captions that better align with emotional subtext.


## System Architecture

### 1️⃣ Audio Input
- User uploads short conversational audio (~60 seconds)
- Implemented using Streamlit interface

### 2️⃣ Speech-to-Text
- OpenAI Whisper (local model)
- Converts audio → transcript

### 3️⃣ Structured Inference (Text-Only)
- GPT-4o-mini
- Constrained JSON schema output
- Conservative inference (no over-speculation)
- No prosodic features (Level 2 reserved for future work)

### 4️⃣ Caption Generation

**Condition A – Baseline**

Transcript → Caption Generator

**Condition B – Structured**

Transcript → Structured Tone Extraction → Caption Generator

Each condition returns:

- Caption 1: Reflective (1–3 sentences)
- Caption 2: Short/punchy (1 sentence)

### 5️⃣ UI Output

The Streamlit interface displays:

- Transcript  
- Baseline captions  
- Structured captions (side-by-side comparison)


## Technical Stack

- Python  
- Streamlit  
- OpenAI Whisper (local)  
- OpenAI GPT-4o-mini  
- JSON Schema-constrained outputs  
- python-dotenv  
- GitHub for version control  

## Evaluation Plan

- 8–12 short conversational clips  
- Two independent graduate-level evaluators  
- 1–5 rating scale  
- Evaluation criteria:
  - Relevance  
  - Emotional alignment  
  - Subtext preservation  
  - Authenticity  

This is an exploratory comparison rather than a large statistical study.


## ▶️ How to Run

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set OpenAI API Key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

### 4. Run the App

```bash
streamlit run src/app.py
```

## Future Work (Review Cycle 2+)

- Refine structured inference clarity  
- Add conversational pattern classification  
- Explore Level 2 prosodic emotional signals  
- Expand evaluation methodology  
- Formalize results documentation  


