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

