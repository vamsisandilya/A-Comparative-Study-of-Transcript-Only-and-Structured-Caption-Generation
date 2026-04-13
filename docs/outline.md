# Project Outline  
## From Conversation to Captions


## 1. Introduction

In this project, I investigate how to design and build a system that converts short conversational audio into captions while preserving emotional tone and conversational meaning. Informal conversations often contain reflections or insights that could be shared as social media content, but transforming these spoken ideas into written captions typically requires additional effort. However, transcript-only approaches may fail to capture emotional tone, intent, and underlying conversational meaning, which can lead to captions that do not fully reflect the original conversation.

Research Question:
How can an audio transcript generator using captured emotions, intent, and themes improve AI-generated captions?

This question focuses on whether incorporating structured conversational signals—specifically emotion, intent, and themes—provides additional context that improves caption generation compared to relying on transcript-only input. The goal is to evaluate whether these signals lead to captions that better reflect the tone and meaning of the original conversation, as measured through human evaluation across relevance, emotion alignment, subtext, and authenticity, as well as overall preference.

To answer this question, the project compares a baseline transcript-only approach with a structured tone-guided approach using human evaluation across relevance, emotion alignment, subtext, and authenticity.

The objectives of this project are to (1) implement a system that converts conversational audio into captions, (2) incorporate structured conversational signals into caption generation, and (3) evaluate the impact of these signals through a controlled human study.


## 2. Background

Recent advances in machine learning have made it possible to process conversational audio and generate useful text from it. This project builds on three main areas: speech-to-text transcription, language model-based text generation, and emotion detection from text.

Speech-to-text systems, such as OpenAI’s Whisper[1], are widely used to convert audio into text. These systems perform well on conversational speech and can handle informal language and different speaking styles. However, they focus on capturing what is said and do not explicitly represent emotional tone or intent.

Large language models (LLMs) are commonly used for generating text, including captions. In many cases, captions are generated directly from transcripts. While this approach can capture the main idea of a conversation, it relies on the model to infer tone and meaning on its own. As a result, the generated captions may miss emotional nuance or deeper meaning.

There has also been research on detecting emotion and sentiment from text[2]. These methods can identify emotional signals, but they are usually treated as separate tasks and are not directly used to guide text generation. More recent work in prompt design suggests that giving structured information to language models can improve output quality[3], but its application to conversational caption generation remains limited.

Based on this, there are two main limitations. First, transcript-based caption generation does not explicitly include emotional or conversational signals. Second, emotion detection is often not integrated into the generation process in a structured way.

This project addresses these limitations by incorporating structured conversational signals into caption generation and evaluating their impact through human evaluation.

## 3. Objectives

The main objective of this project is to design and implement a working prototype that converts short conversational audio clips into caption suggestions suitable for social media. The system will first convert speech into text using a speech recognition model and then generate caption suggestions from the resulting transcript.

A second objective is to incorporate a structured emotional inference layer that extracts conversational signals such as emotion, intent, and themes. Using this structure, the system will generate captions using two approaches: a baseline transcript-only method and a structured emotion-guided method. The final objective is to compare these approaches through controlled evaluation.



## 3. Approach

The project is developed using a modular pipeline that transforms conversational audio into captions. A Streamlit interface allows users to upload short audio clips. These clips are transcribed using OpenAI Whisper to produce a text transcript.

Two caption-generation pipelines are used. The baseline pipeline generates captions directly from the transcript. The structured pipeline first performs text-based emotional inference that produces a constrained representation containing signals such as primary emotion, conversational intent, and themes. This structured representation is then used to guide caption generation.

The system is implemented using Python due to its strong support for machine learning and natural language processing libraries. Streamlit is used to provide a simple interface for uploading and testing audio inputs. OpenAI Whisper is selected for transcription due to its robustness to conversational speech, and the GPT-4o-mini model is used for caption generation to provide consistent and controlled outputs.

The evaluation uses a dataset of 50 short conversational audio clips collected from youtube. The clips are approximately one minute in length and include conversational and reflective speech. Each audio clip is transcribed once and reused across both baseline and structured caption generation approaches to ensure consistency during evaluation.

This design allows a direct comparison between transcript-only and structured approaches, enabling the evaluation of whether incorporating conversational signals improves caption quality.

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

3.3 Structured Caption Generation

The structured approach extends the baseline method by introducing an intermediate conversational signal extraction stage before caption generation. Instead of generating captions directly from the transcript, the system first analyzes the transcript to produce a structured representation of tone and meaning.

This representation includes multiple conversational signals such as primary emotion, secondary emotions, intensity, sarcasm likelihood, confidence, intent, themes, and supporting evidence. These signals are generated using a language model in a text-only setting, meaning the analysis relies entirely on the transcript rather than acoustic features.

A central design feature of this approach is the use of a schema-constrained JSON representation. Rather than allowing the model to produce free-form output, the system enforces a predefined schema that specifies required fields, valid data types, and structural constraints. This ensures that every output follows a consistent format across all transcripts.

The use of a schema provides several important benefits. First, it standardizes the structure of the intermediate representation, allowing the system to process outputs reliably in subsequent stages. Second, it reduces variability in model responses by preventing the use of inconsistent or invented labels. For example, emotions are restricted to a predefined set of allowed categories, and intent labels must belong to a fixed list of conversational intents. Third, it improves comparability across samples, which is essential for evaluation, as all structured outputs follow the same format.

Additional constraints are applied within the schema to further improve consistency. For example, the number of secondary emotions and themes is limited, intensity values are restricted to a bounded range, and sarcasm likelihood is selected from a fixed set of options. These constraints reduce ambiguity and ensure that the structured representation remains compact and interpretable.

Overall, the schema transforms the conversational signal extraction stage into a controlled intermediate representation, making the structured pipeline more reliable and consistent compared to unconstrained text-based analysis.


The structured output generated by the schema-constrained model is not used directly without verification. A validation and sanitization step is applied to ensure that all fields conform to the expected format and constraints. This step corrects invalid or inconsistent values, such as replacing unsupported emotion labels with default values, removing duplicate entries, clamping numerical ranges, and enforcing limits on list sizes.

In cases where the model output cannot be parsed correctly, a safe fallback representation is used. This ensures that the system remains stable and continues to function even when the model produces imperfect outputs. The sanitization process plays a critical role in maintaining consistency across the dataset and preventing errors in downstream processing.

Once validated, the structured representation is converted into a formatted intermediate representation, referred to as a tone block. This tone block summarizes the extracted conversational signals in a structured textual format and is provided as additional context to the caption generation model.

The caption generation stage then uses both the original transcript and the tone block as input. This allows the model to incorporate explicit information about emotion, intent, and thematic content when generating captions. As in the baseline approach, the system generates exactly two captions: one reflective caption consisting of 1–3 sentences and one short, punchy caption consisting of a single sentence.

A fixed and low temperature setting is used during generation to ensure stable and consistent outputs across different samples. This is important for evaluation, as it minimizes variability that is unrelated to the structured representation itself.

By combining schema-constrained extraction, validation, and tone-guided generation, the structured pipeline introduces a controlled mechanism for incorporating conversational signals into caption generation. This design aims to produce captions that better reflect emotional tone, contextual meaning, and underlying subtext compared to transcript-only methods.

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



## References

[1] Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever. 2022. Robust Speech Recognition via Large-Scale Weak Supervision.

[2] Samira Zad, Maryam Heidari, James H. Jr. Jones, and Ozlem Uzuner. Emotion Detection of Textual Data: An Interdisciplinary Survey.

[3] Pranab Sahoo, Ayush Kumar Singh, Sriparna Saha, Vinija Jain, Samrat Mondal, and Aman Chadha. A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications.
