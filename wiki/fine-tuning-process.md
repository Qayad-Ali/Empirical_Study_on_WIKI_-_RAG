---
title: Fine-tuning Process
sources: [instructgpt]
---
## Summary
InstructGPT uses three-stage fine-tuning: Supervised Fine-Tuning (SFT), Reward Modeling (RM), and Reinforcement Learning with Human Feedback (PPO). Each stage builds on the previous one to align models with human preferences.

## Explanation
1. **SFT**: GPT-3 is fine-tuned on labeler demonstrations using supervised learning. Training lasts 16 epochs with cosine decay and 0.2 dropout.  
2. **RM**: A reward model is trained on human comparisons of model outputs, using a cross-entropy loss framework.  
3. **PPO**: Reinforcement learning optimizes the model using the reward model, with KL divergence penalties to prevent over-optimization.  
The final models are called "PPO-ptx" when pretraining gradients are mixed with PPO gradients.  

## Contradictions
"None noted."  
[[training-process]] provides broader context on training procedures.
