---
title: Self-Attention Mechanism
sources: [transformer]
---
## Summary
The Transformer model replaces traditional recurrence with self-attention mechanisms, enabling parallel processing and capturing long-range dependencies.

## Explanation
<details>
The paper introduces self-attention as the core component of the Transformer architecture. This mechanism allows each position in the sequence to attend to all positions in the previous layer, creating a dynamic representation of the input. [[model-architecture]] The self-attention mechanism is implemented through query, key, and value vectors, with multi-headed attention allowing parallel computation across different representation subspaces. [[multi-headed-attention]] This approach enables the model to focus on relevant parts of the input when generating outputs, as demonstrated in [[attention-visualizations]].

The self-attention mechanism is critical for both the encoder and decoder components. In the encoder, self-attention processes input sequences to capture contextual relationships, while in the decoder, it enables the model to attend to encoder outputs and previous decoder states. [[encoder-decoder-architecture]] The paper also discusses how self-attention improves performance compared to recurrent models by avoiding the vanishing gradient problem and allowing for more efficient parallelization. [[recurrent-models]]
</details>

## Contradictions
"None noted."
