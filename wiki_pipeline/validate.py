
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import config
from common.utils import load_corpus

LINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")
SRC_RE = re.compile(r"^sources:\s*\[(.*?)\]", re.M)

def main():
    corpus = {d["id"] for d in load_corpus()}
    pages = {f.stem: f.read_text(encoding="utf-8")
             for f in config.WIKI_DIR.glob("*.md") if f.name not in ("index.md", "log.md")}
    issues, linked, sourced = [], set(), 0
    for stem, body in pages.items():
        m = SRC_RE.search(body)
        srcs = [s.strip() for s in (m.group(1).split(",") if m else []) if s.strip()]
        if srcs and all(s in corpus for s in srcs):
            sourced += 1
        if not srcs:
            issues.append(("no-source", f"{stem}.md has no sources: field"))
        for s in srcs:
            if s not in corpus:
                issues.append(("bad-source", f"{stem}.md cites '{s}' (not a paper in raw/)"))
        for tgt in LINK_RE.findall(body):
            linked.add(tgt)
            if tgt not in pages:
                issues.append(("broken-link", f"{stem}.md -> [[{tgt}]] (no such page)"))
    for stem in pages:
        if stem not in linked:
            issues.append(("orphan", f"{stem}.md (nothing links to it)"))
    lines = ["# Chain-of-custody report", "",
             f"Corpus in raw/: {sorted(corpus)}",
             f"Pages audited: {len(pages)}",
             f"**Pages with valid source provenance: {sourced}/{len(pages)} "
             f"({(sourced/len(pages)*100 if pages else 0):.0f}%)**", "",
             f"## Issues ({len(issues)})"]
    lines += [f"- [{k}] {m}" for k, m in issues] or ["- none: every page cites a real source and all links resolve"]
    (config.RESULTS_DIR / "custody_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:6]), f"\n... {len(issues)} issues -> results/custody_report.md")

if __name__ == "__main__":
    main()
