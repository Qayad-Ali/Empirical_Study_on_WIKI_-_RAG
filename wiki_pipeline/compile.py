"""System B build step: read raw/ papers ONE AT A TIME and write linked entity pages to wiki/.
Run:  python -m wiki_pipeline.compile"""
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import config
from common import llm
from common.utils import load_corpus, append_log

FILE_RE = re.compile(r"^=== FILE:\s*(.+?)\s*===\s*$", re.M)

SYSTEM = ("You are a meticulous wiki compiler. You read ONE research paper and write "
          "Wikipedia-style entity pages in Markdown: one concept per page. Be concise and "
          "factual; never invent facts that are not in the paper.")

PROMPT = """A new paper has been added to the corpus. Read it and write entity pages for its key concepts.

PAPER_ID: {pid}
PAPER_TITLE: {title}

PAPER TEXT:
{text}

PAGES THAT ALREADY EXIST (reuse and link to these instead of duplicating):
{existing}

Rules:
- ONE concept per page. 5-9 pages for this paper is typical.
- Link related concepts with [[double-brackets]] using the page slug, e.g. [[self-attention]].
- If this paper agrees or disagrees with an existing page, say so under "## Contradictions".
- Output NOTHING but page blocks, each EXACTLY in this format:

=== FILE: <slug>.md ===
---
title: <Human Readable Title>
sources: [{pid}]
---
## Summary
<2-3 sentences>

## Explanation
<details, with [[links]]>

## Contradictions
<"None noted." or the conflict>
"""

def _front(body, key):
    m = re.search(rf"^{key}:\s*(.+)$", body, re.M)
    return m.group(1).strip() if m else ""

def _summary_line(body):
    m = re.search(r"##\s*Summary\s*\n+([^\n]+)", body)
    return m.group(1).strip() if m else ""

def existing_pages():
    out = []
    for f in sorted(config.WIKI_DIR.glob("*.md")):
        if f.name in ("index.md", "log.md"):
            continue
        out.append((f.stem, _front(f.read_text(encoding="utf-8"), "title") or f.stem))
    return out

def parse_blocks(text):
    parts = FILE_RE.split(text)
    pages = []
    for i in range(1, len(parts), 2):
        name = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        slug = re.sub(r"[^a-z0-9\-]+", "-", name.lower().replace(".md", "")).strip("-")
        if slug and body:
            pages.append((slug + ".md", body))
    return pages

def rebuild_index():
    lines = ["# Index", "", "_Catalog of every page. The query step reads this first._", ""]
    for f in sorted(config.WIKI_DIR.glob("*.md")):
        if f.name in ("index.md", "log.md"):
            continue
        body = f.read_text(encoding="utf-8")
        lines.append(f"- [[{f.stem}]] — {_front(body,'title') or f.stem}: "
                     f"{_summary_line(body)}  (sources: {_front(body,'sources')})")
    (config.WIKI_DIR / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def compile_corpus():
    docs = load_corpus()
    if not docs:
        print("No sources in raw/. Run download_papers.py first.")
        return
    tin = tout = tpages = 0
    for d in docs:
        ex = existing_pages()
        ex_txt = "\n".join(f"- [[{s}]] {t}" for s, t in ex) or "(none yet)"
        prompt = PROMPT.format(pid=d["id"], title=d["title"], text=d["text"], existing=ex_txt)
        res = llm.complete(prompt, system=SYSTEM, max_tokens=4000, think=True)
        pages = parse_blocks(res["text"])
        for name, body in pages:
            (config.WIKI_DIR / name).write_text(body + "\n", encoding="utf-8")
        tin += res["in_tokens"]; tout += res["out_tokens"]; tpages += len(pages)
        append_log(f"ingest | {d['title']} | +{len(pages)} pages | {res['in_tokens']}+{res['out_tokens']} tok")
        print(f"[{d['id']:<12}] {len(pages)} pages  ({res['in_tokens']} in / {res['out_tokens']} out)")
    rebuild_index()
    (config.RESULTS_DIR / "wiki_build_cost.txt").write_text(f"{tin},{tout},{tpages}\n", encoding="utf-8")
    print(f"\nWiki built: {tpages} pages, {tin} in + {tout} out tokens. Open wiki/ in Obsidian.")

if __name__ == "__main__":
    compile_corpus()
