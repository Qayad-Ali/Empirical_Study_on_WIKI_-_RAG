import sys
import pathlib
import urllib.request
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))

import config
from common.utils import load_corpus,word_count
ARXIV_PDF="https://arxiv.org/pdf/{arxiv_id}.pdf"
def download():
    config.RAW_DIR.mkdir(parents=True,exist_ok=True)
    for p in config.ARXIV_PAPERS:
        if p.get("skip"): continue
        dest=config.RAW_DIR/f"{p['id']}.pdf"
        if dest.exists() or (config.RAW_DIR/f"{p['id']}.md").exists():
            print(f"[skip] {p['id']} already present")
            continue
        url=ARXIV_PDF.format(arxiv_id=p["arxiv_id"])
        print(f" [get] {p['title']}")
        try:
            req=urllib.request.Request(url,headers={"user-agent":"mozilla/5.0(research)"})
            with urllib.request.urlopen(req,timeout=60) as r,open(dest,"wb") as fh:
                fh.write(r.read())
        except Exception as e:
            print(f" [warn] could not download {p['id']}: {e}") 
            print(f"    download manually and save as raw/{p['id']}.pdf(or .md/.txt).")



def stats():
    docs=load_corpus()
    if not docs:
        print("\nNo sources found in raw/. Add files and re-run.")
        return
    print(f"\n{'id':<14}{'words':>9} title")
    total=0
    for d in docs:
        wc=word_count(d["text"])
        total+=wc
        print(f"{d['id']:<14}{wc:>9,}   {d['title']}")
    print(f"{'TOTAL':<14}{total:>9,} words   (~{total * 1.3 / 1000:.0f}K tokens, rough)")
if __name__=="__main__":
    print("done corpus")
    download()
    stats()