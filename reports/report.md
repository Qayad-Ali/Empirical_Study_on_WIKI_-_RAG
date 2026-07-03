# When Does a Compiled LLM Wiki Beat RAG? — A Small Empirical Study (v1)

**Finding:** on a single-domain corpus of four foundational ML papers, answered by a local
qwen3:8b model, a compiled "LLM wiki" was **substantially worse than vanilla RAG** for
question-answering (overall correctness 1.29 vs 1.79 on a 0-2 scale) and cost more per query. Its
*only* advantage was on **contradiction** questions. The reason is concrete: compiling papers into
summary pages **drops specific facts**, so the wiki could no longer answer basic questions its
source papers plainly contain.

## 1. Question & motivation
RAG assembles knowledge at *query* time (retrieve raw chunks, synthesize on the spot). The
LLM-wiki pattern assembles it once at *compile* time into linked markdown pages, then just reads
them. The useful question is not "is the wiki better?" but **"when, and by how much?"** This is a
small, single-domain probe of that boundary.

## 2. Method
- **Corpus:** *Attention Is All You Need*, *BERT*, *GPT-3*, *InstructGPT* (arXiv), each capped at
  6,000 words so both systems see identical input.
- **System A (RAG):** 220-word chunks, MiniLM embeddings (all-MiniLM-L6-v2), FAISS top-5,
  answered by qwen3:8b.
- **System B (Wiki):** qwen3:8b compiles `raw/` into linked entity pages (reasoning ON) -> 22
  pages; a query reads `index.md`, opens the relevant pages, and answers (reasoning OFF).
- **Controls:** same generator (qwen3:8b), same 24 questions, same word budget. Reasoning was
  disabled for both systems' *answers* so per-query token cost reflects context size, not hidden
  chain-of-thought. Grading by a **different** model (llama3.1:8b) on a 0-2 rubric.
- **Questions:** 24, six per tier — (1) single fact, (2) single-doc reasoning, (3) multi-hop
  synthesis, (4) contradiction. Run 3x at temperature 0.
- **Judge correction:** the raw judge over-credited "the information is not in the context"
  non-answers as fully correct. A 10-answer hand-check agreed with the judge only 70% of the time,
  and every disagreement was this failure. We therefore score such refusals 0. All numbers below
  are **post-correction** (this dropped the wiki's overall score from 1.71 to 1.29, since the wiki
  produces nearly all the refusals).

## 3. Results
Wiki build cost: **24,064 tokens** (one-time). Tokens/query: **wiki 2,364 vs RAG 1,796** — the
wiki is *more* expensive per query (two calls plus whole-page context), so there is **no break-even**.

| Tier | Wiki | RAG |
|---|---|---|
| 1 single fact | 1.00 | 2.00 |
| 2 single-doc reasoning | 1.00 | 2.00 |
| 3 multi-hop synthesis | 1.33 | 1.83 |
| 4 contradiction | 1.83 | 1.33 |
| **Overall correctness** | **1.29** | **1.79** |
| Faithfulness | 2.00 | 2.00 |

(Min-max spread across the 3 runs was ~0 because temperature = 0.) The wiki's faithfulness ties
RAG's only because it **abstains** ("not in the pages") instead of fabricating — honest, but a
non-answer.

## 4. Error analysis
See `eval/error_analysis.md`. The wiki's dominant failure is **compile-time information loss**:
basic facts (d_model = 512, the 15% mask rate, GPT-3's 175B parameters) were summarized out of the
pages, so five of six Tier-1/2 wiki answers became "the pages do not specify this." A second mode is
**propagated mischaracterization** (a wrong statement baked into a page harms every query that reads
it). RAG's few misses are **retrieval over-concentration** (top-k drawn from one paper, missing the
cross-paper contrast). RAG errors are per-query and recoverable; wiki errors are compiled in.

## 5. Interpretation — when to use each
- **RAG** for almost everything here — facts, single-document reasoning, and even synthesis — and
  it is cheaper per query. Keeping the raw text retrievable is what saves it.
- **The wiki** only where **relationships across sources** are the whole point: contradictions,
  where compile-time cross-linking (1.83) beat RAG's single-paper retrieval (1.33). Its
  compression is a liability everywhere detail matters.
- Practical read: at this scale, compile-time summarization loses more (specific facts) than it
  gains (precomputed links). A wiki would need faithfulness-preserving compilation, or a much
  larger corpus where retrieval genuinely struggles, to pay off.

## 6. Limitations
- **Tiny n:** 6 questions/tier; with temperature 0 the 3 runs are identical, so a one-question
  difference is not significant. Directional evidence, not statistics.
- **Judge:** an 8B model (llama3.1) with a known bias we corrected (refusals -> 0); other grading
  noise remains unmeasured beyond the 10-answer hand-check.
- **Single domain, 4 papers, 6,000-word cap.**
- **Implementation-dependent:** the wiki's cost and detail loss reflect this compile prompt and
  two-call query design. This is evidence about *this* wiki, not the pattern in the abstract.

## 7. Reproduce
See `readme.md`. `python -m eval.run_eval && python -m eval.judge && python -m eval.analyze`.
