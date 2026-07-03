
import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import config
from common import llm

LINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")

def load_pages():
    return {f.stem: f.read_text(encoding="utf-8")
            for f in sorted(config.WIKI_DIR.glob("*.md"))
            if f.name not in ("index.md", "log.md")}

def structural(pages):
    issues, linked = [], set()
    for stem, body in pages.items():
        for tgt in LINK_RE.findall(body):
            linked.add(tgt)
            if tgt not in pages:
                issues.append(("broken-link", f"{stem}.md -> [[{tgt}]] (no such page)"))
    for stem, body in pages.items():
        if stem not in linked:
            issues.append(("orphan", f"{stem}.md (nothing links to it)"))
        if not re.search(r"^title:",   body, re.M): issues.append(("no-title",   f"{stem}.md"))
        if not re.search(r"^sources:", body, re.M): issues.append(("no-sources", f"{stem}.md"))
    return issues

def llm_contradiction_scan(pages):
    cat = []
    for stem, body in pages.items():
        m = re.search(r"##\s*Summary\s*\n+([^\n]+)", body)
        cat.append(f"[[{stem}]]: {m.group(1).strip() if m else ''}")
    prompt = ("Here are one-line summaries of wiki pages:\n\n" + "\n".join(cat) +
              "\n\nList any pairs of pages whose claims appear to contradict each other, one per "
              "line as 'pageA vs pageB: reason'. If none, reply 'None found.'")
    return llm.complete(prompt, system="You are a wiki auditor.", max_tokens=400)["text"]

def main():
    pages = load_pages()
    lines = ["# Lint report", "", f"{len(pages)} content pages audited."]
    issues = structural(pages)
    lines += ["", f"## Structural issues ({len(issues)})"]
    lines += [f"- [{k}] {m}" for k, m in issues] or ["- none"]
    if "--llm" in sys.argv and pages:
        lines += ["", "## LLM contradiction scan", llm_contradiction_scan(pages)]
    report = "\n".join(lines) + "\n"
    (config.RESULTS_DIR / "lint_report.md").write_text(report, encoding="utf-8")
    print(report)

if __name__ == "__main__":
    main()
