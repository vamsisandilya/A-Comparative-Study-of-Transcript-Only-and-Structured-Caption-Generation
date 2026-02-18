# Technology Evaluation: Speech-to-Text and Caption Generation

## Objective
Select speech-to-text (STT) and caption generation technologies for the initial prototype.

## Requirements
- Works well for short conversational audio (30–90 seconds)
- Fast to integrate and reliable for a demo/prototype
- Reasonable cost for limited usage
- Runs on a student laptop without complex setup (preferred for early milestones)

---

## Speech-to-Text Options Evaluated

### Option A: Hosted Speech-to-Text API
**Summary:** Use a cloud STT service via API.
- **Pros:**
  - Easy integration (send audio, receive transcript)
  - Reliable results without local model setup
  - No GPU required
- **Cons:**
  - Requires internet access
  - Ongoing cost based on usage

### Option B: Local/Open-Source STT (e.g., Whisper via Hugging Face)
**Summary:** Run an open-source model locally.
- **Pros:**
  - No per-request API cost after setup
  - Can work offline after installation
- **Cons:**
  - Setup complexity (PyTorch, model downloads)
  - Slow on CPU for larger models
  - Higher risk of setup issues during early demos

**Decision (for Review Cycle 1):** Choose **Hosted Speech-to-Text API** to reduce setup risk and ensure consistent demo performance. Local open-source STT may be explored later as an optional comparison.

---

## Caption Generation Options Evaluated

### Option A: Hosted LLM API
**Summary:** Use a cloud language model API to generate 1–3 caption drafts.
- **Pros:**
  - High quality text generation
  - Easy to control output with prompts and rules (length, tone, hashtag limits)
  - Quick to iterate during prototype stage
- **Cons:**
  - Requires internet access
  - Usage-based cost

### Option B: Local/Open-Source LLM
**Summary:** Run an open-source text model locally.
- **Pros:**
  - No per-request cost after setup
- **Cons:**
  - Hardware constraints (often slow or heavy)
  - More setup time and integration risk

**Decision (for Review Cycle 1):** Choose **Hosted LLM API** for speed of development and consistent output quality. Local LLMs are out of scope for the first prototype milestone.

---

## Final Selected Approach (Current)
- **STT:** Hosted Speech-to-Text API (final provider to be selected during implementation)
- **Caption Generation:** Hosted LLM API
- **Rationale:** Minimizes technical risk and setup complexity for early milestones while enabling a working prototype quickly.
