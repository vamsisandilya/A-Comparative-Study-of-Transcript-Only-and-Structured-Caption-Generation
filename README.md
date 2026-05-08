# A Comparative Study of Transcript-Only and Structured Signal-Based Caption Generation

## Master’s Project – University of New Hampshire

## Project Overview

This project investigates whether explicitly modeled conversational signals improve emotionally aligned AI-generated captions derived from spoken conversation transcripts.

The system converts short conversational audio clips into Instagram-style captions using two experimental conditions:

### Condition A — Baseline (Transcript-Only)
Captions are generated directly from the transcript using a language model.

### Condition B — Structured Signal-Based Generation
Captions are generated using the transcript along with structured conversational metadata extracted from the conversation.

The project evaluates whether structured conversational guidance improves:

- Relevance
- Emotional alignment
- Subtext preservation
- Perceived authenticity

This work is designed as an academic comparative study focused on structured conversational guidance for caption generation.

---

# Research Question

> How can an audio transcript generator using captured emotions, intent, and themes improve AI-generated captions?

---

# Research Motivation

Conversational speech contains emotional nuance, implied meaning, and communicative intent that may not be fully represented through transcript text alone.

Traditional transcript-only generation approaches rely on the language model to infer conversational tone implicitly. However, conversational subtext and emotional context may be inconsistently interpreted during generation.

This project introduces a structured intermediate representation that explicitly models conversational signals extracted from transcript text. The hypothesis is that providing structured conversational guidance may improve emotional consistency and alignment in generated captions.

The structured representation includes:

- Primary emotion
- Secondary emotions (0–3)
- Emotional intensity (0–3)
- Sarcasm likelihood
- Communicative intent
- Themes
- Evidence quote grounded in transcript
- Confidence score

---

# System Architecture

The system follows a two-branch comparative pipeline.

## 1. Audio Input

Users upload short conversational audio clips (~60 seconds) through a Streamlit interface.

---

## 2. Speech-to-Text Conversion

The uploaded audio is transcribed using OpenAI Whisper (local model).

### Input
Audio clip

### Output
Transcript text

---

## 3. Structured Conversational Signal Extraction

The structured branch performs conversational signal inference using GPT-4o-mini.

The system extracts:

- Emotions
- Intent
- Themes
- Emotional intensity
- Sarcasm likelihood
- Supporting evidence

The extraction process uses schema-constrained JSON generation to enforce a consistent structured format.

---

## 4. Validation and Sanitization

After structured extraction, the system validates and sanitizes all generated fields.

This stage:

- Enforces valid value ranges
- Restricts outputs to allowed categories
- Removes malformed or unsupported values
- Improves reliability of downstream generation

This step ensures that structurally correct outputs also contain valid and usable conversational metadata.

---

## 5. Tone Block Construction

The validated structured metadata is converted into a readable tone block representation.

This tone block acts as an explicit conditioning input for caption generation.

---

## 6. Caption Generation

### Baseline Condition

Transcript → Caption Generator

### Structured Condition

Transcript → Structured Signal Extraction → Tone Block → Caption Generator

Each condition produces:

### Caption 1
Reflective caption (1–3 sentences)

### Caption 2
Short/punchy caption (1 sentence)

The baseline approach relies on implicit conversational inference, while the structured approach explicitly guides generation using extracted conversational signals.

---

## 7. User Interface

The Streamlit interface displays:

- Transcript
- Baseline captions
- Structured captions
- Side-by-side comparison outputs

---

# Technical Stack

## Languages and Frameworks

- Python
- Streamlit

## AI Models

- OpenAI Whisper (local STT)
- OpenAI GPT-4o-mini

## Supporting Components

- JSON schema-constrained outputs
- python-dotenv
- GitHub for version control

---

# How to Run

## 1. Clone the Repository

```bash
git clone https://github.com/master-projects-theses/2026-Spring-Adipudi-Vamsi.git
cd 2026-Spring-Adipudi-Vamsi
```

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
OPENAI_API_KEY=your_api_key_here
```

## 5. Run the Streamlit Application

```bash
streamlit run src/app.py
```

After running the command, the Streamlit application will open in the browser.

The application allows users to:

- Upload a short conversational audio clip
- Generate a transcript using Whisper
- Generate transcript-only baseline captions
- Generate structured signal-based captions
- Compare both caption outputs side by side

---

# Evaluation Commands

## Run Evaluation Pipeline

```bash
python3 -m src.eval.run_evaluation
```

This command generates:

- Transcripts
- Baseline captions
- Structured captions
- Evaluator packets
- Randomized X/Y mappings

## Aggregate Evaluation Results

```bash
python3 -m src.eval.aggregate_scores
```

This command computes:

- Average scores for each evaluation metric
- Evaluator preference counts
- Baseline vs structured comparison results

---

# Evaluation Methodology

## Dataset

- 50 conversational audio clips
- Approximately 1 minute per clip

## Evaluators

- 5 human evaluators

## Evaluation Process

Each evaluator:

1. Listens to the audio clip
2. Reads the transcript
3. Reviews two blinded caption sets (X and Y)
4. Scores both outputs independently
5. Selects preferred caption set

The baseline and structured outputs were randomized as X/Y to reduce evaluator bias.

---

# Evaluation Metrics

Captions were evaluated using a 1–7 scoring rubric across four dimensions:

| Metric | Description |
| Relevance | Alignment with transcript content |
| Emotion Alignment | Consistency with conversational emotion |
| Subtext | Preservation of implied meaning |
| Authenticity | Natural and believable caption quality |

---

# Results Summary

The structured signal-based approach showed moderate but consistent improvements over the transcript-only baseline.

## Average Scores

| Metric            | Baseline | Structured |
| Relevance         | 5.124    | 5.160      |
| Emotion Alignment | 5.028    | 5.740      |
| Subtext           | 4.632    | 4.716      |
| Authenticity      | 4.720    | 4.744      |

## Preference Results

| Condition  | Preference Percentage |
| Baseline   | 35.2%                 |
| Structured | 64.8%                 |

The largest improvement was observed in emotional alignment, suggesting that explicit conversational signal modeling helps guide generation toward emotionally consistent captions.

---

# Key Contributions

This project contributes:

- A comparative framework for transcript-only vs structured caption generation
- A structured conversational signal extraction pipeline
- Schema-constrained conversational metadata generation
- Validation and sanitization for reliable structured inference
- Human-centered evaluation methodology for emotionally aligned caption generation

---

# Repository Structure

```text
src/
├── app.py
├── stt.py
├── captions_base.py
├── captions_emotion.py
├── eval/
│   ├── run_evaluation.py
│   └── aggregate_scores.py

data/
├── eval_outputs/
│   ├── baseline/
│   ├── structured/
│   ├── transcripts/
│   ├── packets/
│   ├── scores.csv
│   └── xy_mapping.csv
