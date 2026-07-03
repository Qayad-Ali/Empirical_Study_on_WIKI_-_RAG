---
title: Hyperparameter Ablation
sources: [instructgpt]
---
## Summary
The paper mentions hyperparameter tuning in training but does not provide detailed ablation studies. Key parameters include learning rate decay, dropout rates, and KL penalty coefficients.

## Explanation
- **Learning Rate Decay**: Cosine decay is used during SFT training.  
- **Dropout**: Residual dropout of 0.2 is applied in SFT.  
- **KL Penalty**: β controls the strength of the KL divergence penalty in PPO.  
The paper notes that training for more epochs improves RM scores despite overfitting risks.  

## Contradictions
"None noted."  
[[training-process]] covers hyperparameter tuning in a broader context.
