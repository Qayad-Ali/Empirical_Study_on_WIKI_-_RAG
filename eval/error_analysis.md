# Error analysis (v1)

Read of the wrong answers from the clean run (24 questions x 2 systems; temperature 0, so the 3
runs are identical). Correctness is on a 0-2 scale. Buckets are the recurring failure modes.

## Wiki (System B) — 6 misses / 24

| bucket | what happens | example | tier |
|---|---|---|---|
| compile-time detail loss | a specific fact is summarized out of the page, so it can't be recovered at query time | `t2_transformer_scale` (corr **0**): asked why attention scales by 1/sqrt(d_k); the page omitted it, so the wiki answered "the pages do not mention it" | 2 |
| propagated mischaracterization | an inaccuracy baked into a page at compile time reappears in every answer that reads it | `t2_gpt3_incontext`, `t3_adaptation_contrast`, `t3_objective_evolution`: GPT-3 in-context learning described incorrectly on the GPT-3 pages | 2-3 |
| partial synthesis | captures part of a multi-hop chain but hedges or drops a leg | `t4_finetuning_necessary` | 4 |

## RAG (System A) — 3 misses / 24

| bucket | what happens | example | tier |
|---|---|---|---|
| retrieval over-concentration | top-k chunks all come from one paper, so the cross-paper contrast is missing | `t4_best_task_method` (all 5 chunks from InstructGPT): overstated fine-tuning, missed alignment | 4 |
| synthesis slip | right chunks retrieved, stitched together with an error | `t3_objective_evolution`: mischaracterized GPT-3's architecture | 3 |

## The pattern that matters

RAG's errors are **retrieval misses** — recoverable, and local to one query. The wiki's errors are
**compiled in**: a detail lost or a fact distorted during compile is wrong for *every* query that
touches that page. That explains the wiki's **Tier-1/2 collapse** (1.00 vs 2.00 on both) — after correcting the judge
for rubber-stamped refusals, five of six wiki fact/reasoning answers were "not in the pages." The wiki's one edge is Tier 4 (1.83 vs 1.67), where compile-time contradiction-flagging
beats single-paper retrieval.
