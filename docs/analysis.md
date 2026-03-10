# Caption Generation Analysis

This document analyzes the differences between transcript-only caption generation and structured emotion-guided caption generation used in this project based on the results

## Evaluation Setup

To better understand how structured conversational signals affect caption generation, I ran a small evaluation comparing two approaches used in the prototype. The first approach generates captions directly from the transcript (baseline). The second approach first extracts conversational signals such as emotion, intent, and themes, and then uses that structure to guide caption generation.

The evaluation used sixteen short conversational audio clips. For each clip, captions were generated using both approaches. To avoid bias during evaluation, the captions were randomized into two sets labeled X and Y. Evaluators did not know which method produced each set.

Each caption set was scored on a scale from 1 to 5 based on four criteria:

- Relevance to the original conversation  
- Emotional alignment with the tone of the speech  
- Preservation of conversational subtext  
- Authenticity as an Instagram-style caption  

Evaluators also selected which caption set they preferred overall.

## Results

## Observations

