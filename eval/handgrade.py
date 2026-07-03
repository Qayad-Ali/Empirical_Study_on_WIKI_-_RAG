"""Validate the LLM judge by grading a sample yourself, then comparing.
  python -m eval.handgrade make    # -> results/handgrade.csv  (fill the my_correctness column: 0/1/2)
  python -m eval.handgrade score   # -> % agreement between you and the judge"""
import sys, csv, random, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import yaml
import config

QFILE = pathlib.Path(__file__).resolve().parent / "questions.yaml"
SHEET = config.RESULTS_DIR / "handgrade.csv"

def _rows():
    src = config.RESULTS_DIR / "metrics_graded.csv"
    seen, uniq = set(), []
    for r in csv.DictReader(src.open(encoding="utf-8")):     # csv module = robust to multiline answers
        k = (r["system"], r["id"])
        if k not in seen:
            seen.add(k); uniq.append(r)
    return uniq

def make(n=10):
    refs = {q["id"]: q["reference"] for q in yaml.safe_load(QFILE.read_text(encoding="utf-8"))}
    uniq = _rows(); random.seed(0)
    sample = random.sample(uniq, min(n, len(uniq)))
    with SHEET.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","tier","system","question","reference","answer","judge_correctness","my_correctness"])
        for r in sample:
            w.writerow([r["id"], r["tier"], r["system"], r["question"], refs.get(r["id"], ""),
                        r["answer"], r["correctness"], ""])
    print(f"Wrote {len(sample)} rows -> {SHEET}")
    print("Open it, fill my_correctness (0/1/2) for each, then run:  python -m eval.handgrade score")

def score():
    rows = [r for r in csv.DictReader(SHEET.open(encoding="utf-8")) if r["my_correctness"].strip()]
    if not rows:
        print("Fill the my_correctness column first."); return
    exact = sum(int(float(r["judge_correctness"])) == int(float(r["my_correctness"])) for r in rows) / len(rows)
    within1 = sum(abs(int(float(r["judge_correctness"])) - int(float(r["my_correctness"]))) <= 1 for r in rows) / len(rows)
    print(f"Judge vs you on {len(rows)} answers:  exact agreement {exact:.0%},  within-1 {within1:.0%}")

if __name__ == "__main__":
    (score if "score" in sys.argv else make)()
