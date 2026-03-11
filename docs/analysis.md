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

After collecting evaluator scores, the results were aggregated across all clips and evaluators. The structured caption generation method achieved higher average scores across all evaluation categories.

Average scores for the baseline method were:
- Relevance: 4.125
- Emotion alignment: 3.438
- Subtext: 3.781
- Authenticity: 3.875

Average scores for the structured method were:
- Relevance: 4.531
- Emotion alignment: 4.500
- Subtext: 4.156
- Authenticity: 4.281

Evaluator preferences also favored the structured approach. Across all evaluations, structured captions were selected 42 times, while baseline captions were selected 22 times.

## Observations

The results suggest that the structured caption generation method performed better overall than the transcript-only baseline. Structured captions received higher scores across all four evaluation criteria.
The biggest improvement appeared in emotion alignment, where the structured approach scored noticeably higher than the baseline. This suggests that identifying emotional signals before caption generation helps the language model produce captions that better match the tone and intent of the original speech.
Evaluator preferences also supported this pattern. Even in cases where both captions were reasonable, evaluators more often selected the structured captions as the better option.


## Limitations




