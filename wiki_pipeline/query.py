
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import config
from common import llm

PICK_SYS = "You navigate a wiki. Given its index and a question, choose which pages to open."
PICK = """INDEX:
{index}

AVAILABLE PAGES: {names}

QUESTION: {q}

List the filenames of the 1-5 pages most relevant to the question, comma-separated.
Output only filenames (e.g. bert.md, self-attention.md)."""

ANS_SYS = "You answer strictly from the provided wiki pages. If they lack the answer, say so."
ANS = """WIKI PAGES:
{pages}

QUESTION: {q}

Answer concisely, using only the pages above."""

def _valid_pages():
    return {f.name for f in config.WIKI_DIR.glob("*.md")} - {"index.md", "log.md"}

def answer(question):
    idx = config.WIKI_DIR / "index.md"
    index_txt = idx.read_text(encoding="utf-8") if idx.exists() else ""
    valid = _valid_pages()
    names = ", ".join(sorted(valid))
    r1 = llm.complete(PICK.format(index=index_txt, names=names, q=question),
                      system=PICK_SYS, max_tokens=100)
    picked = [n for n in re.findall(r"[a-z0-9\-]+\.md", r1["text"].lower()) if n in valid]
    picked = list(dict.fromkeys(picked))[:config.TOP_K] or sorted(valid)[:config.TOP_K]  # fallback
    blob = "\n\n".join(f"### {n}\n" + (config.WIKI_DIR / n).read_text(encoding="utf-8") for n in picked)
    r2 = llm.complete(ANS.format(pages=blob, q=question), system=ANS_SYS, max_tokens=500)
    return {"answer": r2["text"], "pages": picked,
            "in_tokens": r1["in_tokens"] + r2["in_tokens"],
            "out_tokens": r1["out_tokens"] + r2["out_tokens"],
            "latency_s": round(r1["latency_s"] + r2["latency_s"], 2)}

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "What optimizer did BERT use?"
    out = answer(q)
    print("pages opened:", out["pages"])
    print("tokens:", out["in_tokens"], "in /", out["out_tokens"], "out")
    print("\n" + out["answer"])
