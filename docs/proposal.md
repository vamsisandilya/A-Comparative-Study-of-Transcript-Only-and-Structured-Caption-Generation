# From Conversation to Instagram Captions  


## Abstract

Many meaningful ideas come up naturally during everyday conversations. However, turning those spoken thoughts into clear and engaging social media captions takes extra time and effort. Because of this, many valuable insights are never shared. Most AI content tools focus only on written input and do not fully consider emotional tone or subtle meaning in speech.

This project presents a prototype system that converts short conversational audio clips into Instagram-style caption suggestions. The system combines speech-to-text transcription, simple emotional analysis, and AI-based caption generation. The goal is to preserve emotional tone and intent while making it easier for users to share their spoken thoughts as structured social media content.


## 1. Introduction

People often express honest, thoughtful, and emotional ideas when speaking casually. These moments can be reflective, motivating, humorous, or vulnerable. However, rewriting spoken ideas into social media posts requires editing and restructuring, which many people may not take the time to do.

Although AI tools can generate captions, most rely only on written prompts and do not attempt to understand emotional tone or subtext such as sarcasm or insecurity. As a result, captions may be relevant but not fully aligned with how the speaker actually felt. This project focuses on preserving emotional meaning when transforming conversation into captions.


## 2. Objectives

The main objectives of this project are:

- To build a working prototype that accepts short conversational audio clips and generates caption suggestions.
- To convert speech into text using a reliable speech recognition model.
- To analyze the transcript to identify emotional tone, intensity, sarcasm likelihood, intent, and key themes.
- To generate Instagram-style captions using both the transcript and emotional information.
- To compare captions generated with and without emotional analysis to see whether emotional information improves quality and authenticity.


## 3. System Overview

The system works in several steps:

1. A user uploads a short audio clip (up to 60 seconds) through a Streamlit web interface.  
2. The audio is converted into text using OpenAI Whisper.  
3. The transcript is analyzed to identify emotional tone and related details.  
4. The transcript and emotional metadata are sent to a language model (GPT-4o-mini) to generate 1–3 caption suggestions.  
5. The transcript and generated captions are displayed to the user.  

The system only provides suggestions and does not automatically post content.


## 4. Methodology

To evaluate the system, 8–12 short conversational clips representing varied emotional tones (e.g., neutral reflection, frustration, humor, insecurity, sarcasm) will be used. The goal is not large-scale statistical generalization, but structured comparison between two caption generation approaches.

For each clip, captions will be generated under two conditions:

- **Condition A:** Transcript-only generation  
- **Condition B:** Transcript plus structured emotional metadata  

At least two human evaluators will independently rate the generated captions using a 1–5 Likert scale across the following dimensions:

- Relevance to spoken content  
- Emotional alignment  
- Preservation of conversational subtext  
- Authenticity and suitability as an Instagram caption  

Average ratings across conditions will be compared to identify consistent differences in perceived quality. Qualitative feedback will also be collected to understand how emotional metadata influences tone and nuance.


## 5. Expected Outcomes

This project is expected to show that conversational speech can be transformed into meaningful caption suggestions. It also aims to demonstrate that including emotional information can help generate captions that feel more natural, authentic, and aligned with the speaker’s intent.


## 6. Limitations and Future Work

The evaluation will use a small number of audio clips and human ratings, which may limit how broadly the results can be applied. The current version analyzes emotions only from text and does not include audio features such as tone, pitch, or speaking speed. Future versions may incorporate vocal features to improve emotional understanding.


## 7. Technologies Used

- Python  
- Streamlit  
- OpenAI Whisper  
- OpenAI GPT-4o-mini API  

