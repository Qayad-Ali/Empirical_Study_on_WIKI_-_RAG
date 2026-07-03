---
title: Training Data Sources
sources: [instructgpt]
---
## Summary
The paper describes three distinct datasets used for fine-tuning InstructGPT models: SFT (Supervised Fine-Tuning), RM (Reward Modeling), and PPO (Proximal Policy Optimization). These datasets are derived from labeler-written prompts and API-submitted prompts.

## Explanation
- **SFT Dataset**: Contains ~13k prompts (labeler-written and API) used to train the initial supervised fine-tuning models.  
- **RM Dataset**: Includes ~33k prompts (labeler-written and API) for training reward models via human comparisons.  
- **PPO Dataset**: Composed of ~31k API-submitted prompts used for reinforcement learning.  
The datasets are split by user ID to ensure training, validation, and test sets are disjoint. PII is filtered from training data to avoid sensitive information leakage.  

## Contradictions
"None noted."  
[[fine-tuning-process]] describes how these datasets are used in the training pipeline.
