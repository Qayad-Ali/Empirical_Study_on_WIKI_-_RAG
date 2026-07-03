
import sys, csv, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import yaml
import config
from wiki_pipeline import query as wiki_q
from rag import query as rag_q

QFILE = pathlib.Path(__file__).resolve().parent / "questions.yaml"
HEADER = ["run","id","tier","system","question","answer","in_tokens","out_tokens","latency_s","sources"]

def ensure_built():
    if not (config.WIKI_DIR / "index.md").exists():
        print("wiki not built -> compiling ..."); from wiki_pipeline.compile import compile_corpus; compile_corpus()
    if not (config.RAG_INDEX_DIR / "faiss.index").exists():
        print("rag index missing -> building ..."); from rag.build_index import build; build()

def _save(rows):
    out = config.RESULTS_DIR / "metrics.csv"
    try:
        f = out.open("w", newline="", encoding="utf-8")
    except PermissionError:                       # metrics.csv locked (open in Excel?)
        out = config.RESULTS_DIR / "metrics_new.csv"
        print(f"  !! metrics.csv is locked (close it in Excel) -> saving to {out.name}")
        f = out.open("w", newline="", encoding="utf-8")
    with f:
        wr = csv.writer(f); wr.writerow(HEADER); wr.writerows(rows)
    return out

def run():
    ensure_built()
    questions = yaml.safe_load(QFILE.read_text(encoding="utf-8"))
    rows = []
    for r in range(1, config.N_RUNS + 1):
        for q in questions:
            w = wiki_q.answer(q["question"])
            rows.append([r,q["id"],q["tier"],"wiki",q["question"],w["answer"],w["in_tokens"],w["out_tokens"],w["latency_s"]," ".join(w["pages"])])
            a = rag_q.answer(q["question"])
            rows.append([r,q["id"],q["tier"],"rag",q["question"],a["answer"],a["in_tokens"],a["out_tokens"],a["latency_s"]," ".join(a["chunks"])])
        out = _save(rows)                          # save after each run so a lock/crash can't wipe progress
        print(f"run {r}/{config.N_RUNS} done -> {out.name} ({len(rows)} rows)")
    print(f"\nDone. {len(rows)} rows in {out}")

if __name__ == "__main__":
    run()
