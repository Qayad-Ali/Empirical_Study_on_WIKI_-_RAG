---
title: Training Data
sources: [transformer]
---
## Summary
The Transformer model was trained on the Wall Street Journal (WSJ) portion of the Penn Treebank and semi-supervised corpora, with varying vocabulary sizes depending on the training setting.

## Explanation
<details>
The paper describes two training settings: a WSJ-only setting with a 16K token vocabulary and a semi-supervised setting using larger corpora with a 32K token vocabulary. [[training-data-sources]] The WSJ training set contains approximately 40K sentences, while the semi-supervised setting incorporates the high-confidence and BerkleyParser corpora with around 17M sentences. [[semi-supervised-training]]

The choice of vocabulary size and training data significantly impacts the model's performance. The paper notes that the semi-supervised setting leads to better results, as demonstrated in [[results-table]]. The training data sources are also relevant to the model's ability to generalize to new tasks, as discussed in [[zero-shot]].
</details>

## Contradictions
"None noted."
