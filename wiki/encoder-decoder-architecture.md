---
title: Encoder-Decoder Architecture
sources: [transformer]
---
## Summary
The Transformer model uses an encoder-decoder architecture based entirely on self-attention mechanisms, replacing traditional recurrence layers.

## Explanation
<details>
The paper presents an encoder-decoder architecture where both the encoder and decoder are composed of stacked self-attention layers. [[self-attention]] The encoder processes the input sequence to generate a contextual representation, while the decoder uses this representation to generate the output sequence. [[translation-tasks]] This architecture eliminates the need for recurrence, enabling parallel processing and improving training efficiency. [[recurrent-models]]

Each encoder layer contains two sub-layers: multi-headed self-attention and a position-wise fully connected network. [[model-architecture]] Similarly, each decoder layer includes multi-headed attention over the encoder output and the previous decoder states, along with a position-wise fully connected network. [[model-architecture]] The paper emphasizes that this design allows the model to handle long-range dependencies more effectively than traditional recurrent architectures. [[recurrent-models]]
</details>

## Contradictions
"None noted."
