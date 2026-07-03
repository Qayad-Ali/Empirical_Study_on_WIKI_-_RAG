
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import faiss
import config
from common import llm
from common.embed import embed_texts

_SYS = "You answer strictly from the retrieved excerpts. If they lack the answer, say so."
_PROMPT = """RETRIEVED EXCERPTS:
{ctx}

QUESTION: {q}

Answer concisely, using only the excerpts above."""

def _load():
    index = faiss.read_index(str(config.RAG_INDEX_DIR / "faiss.index"))
    data = json.loads((config.RAG_INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))
    return index, data["texts"], data["meta"]

def answer(question, k=None):
    k = k or config.TOP_K
    index, texts, meta = _load()
    D, I = index.search(embed_texts([question]), k)
    hits = [(meta[i]["doc"], texts[i]) for i in I[0]]
    ctx = "\n\n".join(f"[{d}] {t}" for d, t in hits)
    res = llm.complete(_PROMPT.format(ctx=ctx, q=question), system=_SYS, max_tokens=500)
    return {"answer": res["text"], "chunks": [d for d, _ in hits],
            "in_tokens": res["in_tokens"], "out_tokens": res["out_tokens"], "latency_s": res["latency_s"]}

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "What optimizer did BERT use?"
    out = answer(q)
    print("chunks from:", out["chunks"])
    print("tokens:", out["in_tokens"], "in /", out["out_tokens"], "out")
    print("\n" + out["answer"])
