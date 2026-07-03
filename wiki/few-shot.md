---
title: Few-Shot Learning
sources: [gpt3]
---
## Summary
Few-shot learning uses a small number of examples (K) during inference, reducing reliance on task-specific data while balancing performance and efficiency.

## Explanation
Few-shot learning (FS) provides K examples of context-completion pairs to the model, which then generates completions for a final context. The paper notes that K is typically 10-100, constrained by the context window (nctx=2048). While results lag behind fine-tuned models, few-shot offers strong sample efficiency and reduced overfitting risks [[zero-shot]].

## Contradictions
"None noted."
---
