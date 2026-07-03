---
title: Recurrent Models
sources: [transformer]
---
## Summary
The paper highlights the limitations of recurrent neural networks (RNNs) in sequence modeling tasks, particularly their inability to handle long-range dependencies effectively.

## Explanation
<details>
The paper contrasts the Transformer's self-attention mechanism with traditional RNNs, noting that RNNs suffer from the vanishing gradient problem and sequential processing limitations. [[self-attention]] This makes it difficult for RNNs to capture long-range dependencies in sequences, which is critical for tasks like machine translation. [[translation-tasks]] The paper also mentions that RNN-based sequence-to-sequence models have not achieved state-of-the-art results in small-data regimes. [[training-data]]

The Transformer's attention-based architecture overcomes these limitations by allowing each position in the sequence to attend to all others in parallel. [[encoder-decoder-architecture]] This enables more efficient training and better performance on tasks requiring understanding of long-range contextual relationships. [[attention-visualizations]]
</details>

## Contradictions
"None noted."
