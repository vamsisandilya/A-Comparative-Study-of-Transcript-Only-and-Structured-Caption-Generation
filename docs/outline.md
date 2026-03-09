# Project Outline  
## From Conversation to Instagram Captions


## 1. Introduction

In this project, I investigate how to design and build a system that converts short conversational audio into Instagram-style captions while preserving emotional tone and conversational meaning. Informal conversations often contain reflections or insights that could be shared as social media content, but transforming these spoken ideas into written captions typically requires additional effort.

This project explores whether incorporating structured emotional inference into caption generation improves the relevance and authenticity of generated captions compared to a transcript-only approach.

More specifically, I am investigating:

- How to build a pipeline that turns spoken conversation into structured written content.
- How structured emotional inference can guide caption generation.
- How transcript-only caption generation compares to caption generation that incorporates emotional metadata.


## 2. Objectives

The main objective of this project is to design and implement a working prototype that converts short conversational audio clips into caption suggestions suitable for social media. The system will first convert speech into text using a speech recognition model and then generate caption suggestions from the resulting transcript.

A second objective is to incorporate a structured emotional inference layer that extracts conversational signals such as emotion, intent, and themes. Using this structure, the system will generate captions using two approaches: a baseline transcript-only method and a structured emotion-guided method. The final objective is to compare these approaches through controlled evaluation.

The main objectives of this project are:

- To build a working prototype that accepts short conversational audio clips.
- To convert speech into text using a speech recognition model.
- To implement structured text-based emotional inference (Level 1).
- To generate captions using two approaches:
  - A baseline transcript-only method.
  - A structured emotion-guided method.
- To compare the two approaches in a controlled evaluation.



## 3. Approach

The project will be developed using a modular pipeline that transforms conversational audio into captions. A Streamlit interface will allow users to upload short audio clips. These clips will be transcribed using OpenAI Whisper to produce a text transcript.

Two caption-generation pipelines will then be implemented. The baseline pipeline generates captions directly from the transcript. The structured pipeline first performs text-based emotional inference that produces a constrained representation containing signals such as primary emotion, conversational intent, and themes. This structured representation is then used to guide caption generation.

The system will be implemented using Python, Streamlit, OpenAI Whisper for speech-to-text transcription, and the GPT-4o-mini API for caption generation. GitHub will be used for version control and iterative development.

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



## 4. Expected Results

The result of my study is expected to include:

- A working prototype that converts conversational speech into caption suggestions.
- A structured method for incorporating emotional inference into caption generation.
- A clear comparison between transcript-only and structured emotion-guided approaches.
- Analysis of how emotional structure affects tone, alignment, and perceived authenticity.



## 5. Evaluation

The system will be evaluated through a controlled comparison of the two caption-generation approaches. A dataset of approximately 8–12 short conversational audio clips representing a range of emotional contexts will be used.

Captions will be generated under two conditions: transcript-only generation and structured emotion-guided generation. All other variables will remain constant, including the language model, temperature settings, prompt design, transcript input, and output format.

Outputs will be randomized into two sets (X and Y) so that evaluators cannot determine which method produced each caption set. Two independent evaluators will rate the captions using a 1–5 scale based on relevance, emotional alignment, preservation of conversational subtext, and authenticity as an Instagram caption. Evaluators will also indicate their overall preference. Results will be averaged across clips and evaluators to identify consistent differences between the approaches.

The system will be evaluated through structured comparison.

Using 8–12 short conversational audio clips representing different emotional tones, captions will be generated under two conditions:

- **Condition A:** Transcript-only generation.
- **Condition B:** Structured emotion-guided generation.

All other variables will be held constant, including:
- Model (gpt-4o-mini)
- Temperature (0.2)
- Caption-writing prompt
- Transcript input text
- Output format (two captions per clip)

For each audio clip:
1. A transcript will be generated and saved.
2. Captions will be generated under both conditions.
3. The outputs will be randomized into Set X and Set Y.
4. Evaluators will not know which condition produced which set.

Two independent graduate-level evaluators will assess the generated captions using a 1–5 rating scale based on:

- Relevance to the spoken content  
- Emotional alignment  
- Preservation of conversational subtext  
- Authenticity and suitability as an Instagram caption  

Evaluators will also indicate overall preference (X or Y).

Scores will be averaged across clips and evaluators to identify consistent differences between approaches. 
 
 The evaluation is exploratory and intended to compare approaches.

