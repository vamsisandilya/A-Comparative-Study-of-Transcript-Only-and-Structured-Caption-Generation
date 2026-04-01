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

3.1 Speech-to-Text Transcription

The first stage of the system converts conversational audio into text using the Whisper model. In this implementation, the “base” variant of the model is used to provide a balance between transcription accuracy and computational efficiency.

Given an input audio file, the system applies Whisper’s transcription function to generate a textual representation of the spoken content. The output of this stage is a plain text transcript, which is then used as the input for caption generation.

A key design decision in this stage is that the same transcript is reused for both the baseline and structured caption generation approaches. This ensures that any differences in generated captions are due to the caption generation method rather than variations in transcription, thereby maintaining consistency in the evaluation.

The use of Whisper is particularly suitable for this project because conversational audio often includes informal speech patterns, pauses, and variations in tone. Whisper is robust to such variations, making it effective for accurately capturing real-world conversational content.

3.2 Baseline Caption Generation

In the baseline approach, captions are generated directly from the transcript without incorporating any additional conversational or emotional signals. The transcript produced by the speech-to-text component is provided as the sole input to a language model (GPT-based), which generates caption suggestions based only on the textual content.

The system is designed to return exactly two captions for each transcript:
- one reflective caption (1–3 sentences)
- one short, punchy caption (1 sentence)

To ensure consistency and improve output quality, the prompt includes specific constraints. The model is instructed to produce concise, natural captions that are directly grounded in the transcript. Generic motivational phrases and clichés are explicitly discouraged to maintain authenticity and relevance to the original conversation.

This baseline method serves as the control condition in the evaluation. Because it relies only on the transcript, it does not explicitly account for emotional tone, conversational intent, or underlying subtext. As a result, while it may capture the main idea of the conversation, it may fail to fully reflect nuanced emotional or contextual aspects of the spoken content.



## 4. Expected Results

The expected result of this project is a working prototype that can take short conversational audio and generate caption suggestions suitable for social media posts. The system should be able to convert natural speech into captions that capture the main idea of the conversation while preserving its tone.

Another expected outcome is a comparison between two caption generation approaches. The first approach generates captions directly from the transcript of the conversation. The second approach uses structured conversational signals such as emotion and intent to guide caption generation.

Based on the design of the system, it is expected that the structured approach will produce captions that better reflect the emotional tone and meaning of the conversation. These captions may feel more natural and more appropriate for social media compared to captions generated directly from the transcript.

The evaluation results will help show whether using structured conversational signals improves caption quality in terms of relevance, emotional alignment, and authenticity.



## 5. Evaluation

To compare the baseline and structured caption generation approaches, a controlled human evaluation is conducted using a dataset of short conversational audio clips.

The dataset consists of 50 conversational audio clips. Each clip is transcribed using the speech-to-text component of the system. For each transcript, two sets of captions are generated: one using the baseline transcript-only approach and one using the structured tone-guided approach.

During evaluation, each evaluator first listens to the original audio clip to understand the context and tone of the conversation. The evaluator then reads the transcript, followed by both caption sets.

To ensure a fair comparison, the captions are presented in a blinded format. For each clip, the two caption sets are labeled as “Set X” and “Set Y,” and their order is randomized. This prevents evaluators from knowing which method produces each caption and reduces potential bias.

Evaluators assess each caption set independently based on four criteria: relevance, emotion alignment, subext and authenticity. Each criteria is scored on scale from 1 to 7 using a defined rubric.

- Relevance
Refers to the degree to which the caption is related or useful to what is being expressed in the conversation.

1: The caption is unrelated or does not reflect the conversation
4: The caption partially reflects the main idea
7: The caption clearly and accurately reflects the main idea of the conversation

- Emotion Alignment
Measures how well the caption matches the emotional tone of the conversation.
1: The emotional tone is incorrect or mismatched
4: The caption partially reflects the emotional tone
7: The caption strongly matches the emotional tone

- Subtext
Refers to the hidden or less obvious meaning conveyed by the caption beyond the literal words.
1: The caption does not capture any implied meaning
4: The caption captures some implied meaning
7: The caption effectively reflects underlying meaning or nuance

- Authenticity
Refers to the quality of the caption being real, natural, and believable in a social media context.
1: The caption feels unnatural, forced, or artificial
4: The caption is somewhat natural but not fully convincing
7: The caption feels natural, genuine, and appropriate

In addition to scoring, evaluators select which caption set (X or Y) they prefer overall. This provides a direct comparison between the two approaches and helps identify which method produces more effective captions in practice.

After evaluation, the collected scores are aggregated to compare the baseline and structured approaches. Since evaluators assess caption sets labeled as X and Y, a mapping is used to convert these labels back to their corresponding methods (baseline or structured).

For each approach, the scores across all clips and evaluators are averaged for each metric (relevance, emotion alignment, subtext, and authenticity). These average scores provide a quantitative comparison of how each method performs across different aspects of caption quality.

In addition to metric averages, preference selections are also aggregated by counting how many times each approach is chosen by evaluators. This provides a direct measure of which method is more often preferred in practice.

The structured approach is considered to perform better if it achieves higher average scores across the evaluation metrics and receives a higher number of preference selections compared to the baseline approach.
