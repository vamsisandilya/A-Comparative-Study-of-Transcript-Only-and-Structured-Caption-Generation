# Project Outline  
## From Conversation to Instagram Captions


## 1. What Am I Investigating?

In this project, I am investigating how to design and build a system that converts short conversational audio into Instagram-style captions while preserving emotional tone and conversational meaning.

More specifically, I am investigating:

- How to build a pipeline that turns spoken conversation into structured written content.
- How structured emotional inference can guide caption generation.
- How transcript-only caption generation compares to caption generation that incorporates emotional metadata.

This project combines system development and structured comparison. The goal is to understand whether adding emotional inference improves the relevance and authenticity of generated captions.


## 2. What Are My Objectives?

The main objectives of this project are:

- To build a working prototype that accepts short conversational audio clips.
- To convert speech into text using a speech recognition model.
- To implement structured text-based emotional inference (Level 1).
- To generate captions using two approaches:
  - A baseline transcript-only method.
  - A structured emotion-guided method.
- To compare the two approaches in a controlled evaluation.



## 3. How Will I Carry Out the Work?

The project will be developed using a modular and incremental approach.

### System Components

- **Streamlit Web Interface** for user interaction.
- **Speech-to-Text Module** using OpenAI Whisper.
- **Structured Emotional Inference Module (Level 1)** using constrained JSON output.
- **Baseline Caption Generator** (transcript-only).
- **Structured Emotion-Guided Caption Generator**.
- **Comparison Interface** displaying both outputs side-by-side.

### Planned Milestones

- Establish clean project structure and environment setup.
- Integrate speech-to-text transcription.
- Implement structured emotional inference.
- Implement baseline and structured caption generators.
- Integrate comparison display in the UI.
- Prepare evaluation samples and rating rubric.

### Tools and Technologies

- Python  
- Streamlit  
- OpenAI Whisper  
- OpenAI GPT-4o-mini API  
- GitHub for version control  



## 4. What Results Do I Expect?

The result of my study is expected to include:

- A working prototype that converts conversational speech into caption suggestions.
- A structured method for incorporating emotional inference into caption generation.
- A clear comparison between transcript-only and structured emotion-guided approaches.
- Analysis of how emotional structure affects tone, alignment, and perceived authenticity.



## 5. How Will I Evaluate the Results?

The system will be evaluated through structured comparison.

Using 8–12 short conversational audio clips representing different emotional tones, captions will be generated under two conditions:

- **Condition A:** Transcript-only generation.
- **Condition B:** Structured emotion-guided generation.

Two independent graduate-level evaluators will assess the generated captions using a 1–5 rating scale based on:

- Relevance to the spoken content  
- Emotional alignment  
- Preservation of conversational subtext  
- Authenticity and suitability as an Instagram caption  

Ratings will be averaged across both approaches to identify consistent differences. The evaluation is exploratory and intended to compare approaches.

