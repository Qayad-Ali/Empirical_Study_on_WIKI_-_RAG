# Results summary

- Wiki build cost (one-time): **24,064 tokens**
- Tokens/query — wiki **2364**, rag **1796**
- Break-even: **~inf queries** before the wiki's build cost is repaid  (RAG is not more expensive/query here, so no break-even)

## Per-system overall

| system | correctness | faithfulness | tokens/q | latency(s) |
|---|---|---|---|---|
| rag | 1.79 | 2.00 | 1796 | 2.46 |
| wiki | 1.29 | 2.00 | 2364 | 2.82 |

## Accuracy by tier (mean, min-max over runs)

| tier | wiki | rag |
|---|---|---|
| 1 | 1.00 (1.0-1.0) | 2.00 (2.0-2.0) |
| 2 | 1.00 (1.0-1.0) | 2.00 (2.0-2.0) |
| 3 | 1.33 (1.3-1.3) | 1.83 (1.8-1.8) |
| 4 | 1.83 (1.8-1.8) | 1.33 (1.3-1.3) |
