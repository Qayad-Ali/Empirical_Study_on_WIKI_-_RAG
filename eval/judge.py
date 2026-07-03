
import sys, csv, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import yaml
import config
from common import llm

# an answer that says the info is not in the context is a FAILURE, not a correct answer
_REFUSAL = re.compile(r"(do(es)? not (mention|specify|address|discuss|contain|provide|state|cover|include)"
                      r"|not (mentioned|specified|addressed|discussed|provided|present|available|covered|found|included)"
                      r"|cannot (answer|be (determined|found|answered))|no (information|relevant)"
                      r"|(pages|excerpts|context|text|documents?) do(es)? not)", re.I)

QFILE = pathlib.Path(__file__).resolve().parent / "questions.yaml"
JUDGE_SYS = "You are a strict grader of answers about ML papers. Be terse and consistent."
JUDGE = """QUESTION: {q}
REFERENCE ANSWER: {ref}
CANDIDATE ANSWER: {ans}

Grade the candidate against the reference. Use this scale:
correctness: 0 wrong or missing (INCLUDING answers that say the info is not in the context), 1 partial, 2 fully correct
faithfulness: 0 contradicts or hallucinates, 1 mostly grounded, 2 fully grounded
Reply EXACTLY three lines:
correctness: <0-2>
faithfulness: <0-2>
reason: <one short line>"""

def _newest(*names):
    ps = [config.RESULTS_DIR / n for n in names if (config.RESULTS_DIR / n).exists()]
    return max(ps, key=lambda p: p.stat().st_mtime) if ps else config.RESULTS_DIR / names[0]

def _score(t, key):
    m = re.search(rf"{key}\s*[:=]\s*([0-2])", t, re.I); return int(m.group(1)) if m else 0
def _reason(t):
    m = re.search(r"reason\s*[:=]\s*(.+)", t, re.I); return m.group(1).strip() if m else ""

def _save(rows, fields):
    out = config.RESULTS_DIR / "metrics_graded.csv"
    try:
        f = out.open("w", newline="", encoding="utf-8")
    except PermissionError:
        out = config.RESULTS_DIR / "metrics_graded_new.csv"; print(f"  !! locked -> {out.name}")
        f = out.open("w", newline="", encoding="utf-8")
    with f:
        wr = csv.DictWriter(f, fieldnames=fields); wr.writeheader(); wr.writerows(rows)
    return out

def grade():
    refs = {q["id"]: q["reference"] for q in yaml.safe_load(QFILE.read_text(encoding="utf-8"))}
    src = _newest("metrics.csv", "metrics_new.csv")
    print(f"grading {src.name}")
    rows = list(csv.DictReader(src.open(encoding="utf-8")))
    for i, row in enumerate(rows, 1):
        if not str(row.get("answer", "")).strip():          # empty answer = wrong; don't ask the judge
            row["correctness"], row["faithfulness"], row["reason"] = 0, 0, "empty answer (auto 0)"
            continue
        if _REFUSAL.search(row["answer"]) and len(row["answer"].split()) <= 35:
            row["correctness"], row["faithfulness"], row["reason"] = 0, 2, "not-in-context refusal (auto 0)"
            continue
        res = llm.complete(JUDGE.format(q=row["question"], ref=refs.get(row["id"], ""), ans=row["answer"]),
                           system=JUDGE_SYS, model=config.JUDGE_MODEL, max_tokens=120)
        row["correctness"] = _score(res["text"], "correctness")
        row["faithfulness"] = _score(res["text"], "faithfulness")
        row["reason"] = _reason(res["text"])
        if i % 24 == 0: print(f"graded {i}/{len(rows)}")
    out = _save(rows, list(rows[0].keys()))
    print(f"Wrote graded scores -> {out}")

if __name__ == "__main__":
    grade()
