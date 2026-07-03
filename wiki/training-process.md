---
title: Training Process
sources: [gpt3]
---
## Summary
Training involves large-scale model parallelism, optimized batch sizes, and learning rates tailored to model size.

## Explanation
Models are trained on V100 GPUs with mixed model parallelism (depth and width). Batch sizes and learning rates are adjusted based on model size, with larger models using higher batch sizes and lower learning rates. Training data is not sampled proportionally to size, prioritizing quality over quantity [[fine-tuning-process]].

## Contradictions
"None noted."
---
