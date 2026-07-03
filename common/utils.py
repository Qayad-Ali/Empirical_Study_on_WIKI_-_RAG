import sys,pathlib,datetime
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import config

def append_log(message):
    
    line=f"## [{datetime.date.today()}] {message}\n"
    with (config.WIKI_DIR/"log.md").open("a",encoding="utf-8") as f:
        f.write(line)

def read_text(path):
    return pathlib.Path(path).read_text(encoding="utf-8",errors="ignore")
def extract_pdf_text(path):
    import fitz
    doc=fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def load_corpus(raw_dir=None):
    raw_dir=pathlib.Path(raw_dir or config.RAW_DIR)
    docs,seen=[],set()
    for ext in (".md",".txt",".pdf"):
        for f in sorted(raw_dir.glob(f"*{ext}")):
            if f.stem in seen:
                continue
            seen.add(f.stem)
            text=extract_pdf_text(f) if ext==".pdf" else read_text(f)
            docs.append({"id":f.stem,"title":f.stem.replace("_"," "),"text":text})
    for d in docs:
       d["text"] = " ".join(d["text"].split()[:config.SOURCE_BUDGET_WORDS])        
    return docs

def word_count(text):
    return len(text.split())        
