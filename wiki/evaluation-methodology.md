---
title: Evaluation Methodology
sources: [instructgpt]
---
## Summary
The paper evaluates model alignment through human preference ratings, truthfulness metrics, and bias/toxicity benchmarks. Evaluations are conducted on API prompts and GPT-3-style prompts.

## Explanation
- **Human Preference Ratings**: Labelers rate model outputs on held-out API prompts (excluding training data).  
- **Truthfulness Metrics**: Measures hallucinations on closed-domain tasks and uses the TruthfulQA dataset.  
- **Bias/Toxicity Benchmarks**: Tests on RealToxicityPrompts and CrowS-Pairs datasets.  
- **Alignment Criteria**: Models are judged on helpfulness, honesty, and harmlessness, with labeler judgments as the primary metric.  

## Contradictions
"None noted."  
[[ablation-studies]] may explore specific evaluation aspects.
