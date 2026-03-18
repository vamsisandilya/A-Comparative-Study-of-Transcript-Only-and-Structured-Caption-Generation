# Project Outline  
## From Conversation to Instagram Captions


## 1. Introduction

In this project, I investigate how to design and build a system that converts short conversational audio into Instagram-style captions while preserving emotional tone and conversational meaning. Informal conversations often contain reflections or insights that could be shared as social media content, but transforming these spoken ideas into written captions typically requires additional effort.

This project explores whether incorporating structured emotional inference into caption generation improves the relevance and authenticity of generated captions compared to a transcript-only approach.



## 2. Objectives

The main objective of this project is to design and implement a working prototype that converts short conversational audio clips into caption suggestions suitable for social media. The system will first convert speech into text using a speech recognition model and then generate caption suggestions from the resulting transcript.

A second objective is to incorporate a structured emotional inference layer that extracts conversational signals such as emotion, intent, and themes. Using this structure, the system will generate captions using two approaches: a baseline transcript-only method and a structured emotion-guided method. The final objective is to compare these approaches through controlled evaluation.



## 3. Approach

The project will be developed using a modular pipeline that transforms conversational audio into captions. A Streamlit interface will allow users to upload short audio clips. These clips will be transcribed using OpenAI Whisper to produce a text transcript.

Two caption-generation pipelines will then be implemented. The baseline pipeline generates captions directly from the transcript. The structured pipeline first performs text-based emotional inference that produces a constrained representation containing signals such as primary emotion, conversational intent, and themes. This structured representation is then used to guide caption generation.

The system will be implemented using Python, Streamlit, OpenAI Whisper for speech-to-text transcription, and the GPT-4o-mini API for caption generation. GitHub will be used for version control and iterative development.



## 4. Expected Results

The expected result of this project is a working prototype that can take short conversational audio and generate caption suggestions suitable for social media posts. The system should be able to convert natural speech into captions that capture the main idea of the conversation while preserving its tone.

Another expected outcome is a comparison between two caption generation approaches. The first approach generates captions directly from the transcript of the conversation. The second approach uses structured conversational signals such as emotion and intent to guide caption generation.

Based on the design of the system, it is expected that the structured approach will produce captions that better reflect the emotional tone and meaning of the conversation. These captions may feel more natural and more appropriate for social media compared to captions generated directly from the transcript.

The evaluation results will help show whether using structured conversational signals improves caption quality in terms of relevance, emotional alignment, and authenticity.



## 5. Evaluation

The system will be evaluated through a controlled comparison of the two caption-generation approaches. A dataset of approximately 16 short conversational audio clips representing a range of emotional contexts will be used.

Captions will be generated under two conditions: transcript-only generation and structured emotion-guided generation. All other variables will remain constant, including the language model, temperature settings, prompt design, transcript input, and output format.

Outputs will be randomized into two sets (X and Y) so that evaluators cannot determine which method produced each caption set. Two independent evaluators will rate the captions using a 1–5 scale based on relevance, emotional alignment, preservation of conversational subtext, and authenticity as an Instagram caption. Evaluators will also indicate their overall preference. Results will be averaged across clips and evaluators to identify consistent differences between the approaches.
