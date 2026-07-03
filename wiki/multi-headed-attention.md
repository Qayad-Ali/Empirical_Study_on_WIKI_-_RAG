---
title: Multi-Headed Attention
sources: [transformer]
---
## Summary
Multi-headed attention allows the model to jointly attend to information from different representation subspaces, enhancing the model's ability to capture complex patterns.

## Explanation
<details>
The paper describes multi-headed attention as a key innovation that extends the self-attention mechanism. By splitting the attention process into multiple heads, the model can learn different representation subspaces and combine their outputs. [[self-attention]] Each head independently computes attention weights, and the results are concatenated and projected to a final output. [[attention-visualizations]] This approach increases the model's capacity to capture diverse relationships within the input data.

The multi-headed attention mechanism is implemented with separate linear transformations for each head, followed by concatenation and a final linear projection. [[model-architecture]] The paper also highlights that this design allows the model to focus on different aspects of the input simultaneously, improving performance on tasks like machine translation. [[translation-tasks]]
</details>

## Contradictions
"None noted."
