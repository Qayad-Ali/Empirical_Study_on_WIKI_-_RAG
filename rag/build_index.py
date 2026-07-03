
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import faiss
import config
from common.utils import load_corpus
from common.embed import embed_texts

def chunk(text, size, overlap):
    words = text.split()
    step = max(1, size - overlap)
    return [" ".join(words[i:i+size]) for i in range(0, len(words), step) if words[i:i+size]]

def build():
    docs = load_corpus()
    texts, meta = [], []
    for d in docs:
        for j, c in enumerate(chunk(d["text"], config.CHUNK_SIZE_WORDS, config.CHUNK_OVERLAP_WORDS)):
            texts.append(c); meta.append({"doc": d["id"], "chunk": j})
    vecs = embed_texts(texts)                    # (n, d), normalized
    index = faiss.IndexFlatIP(vecs.shape[1])     # inner product on normalized vecs = cosine
    index.add(vecs)
    faiss.write_index(index, str(config.RAG_INDEX_DIR / "faiss.index"))
    (config.RAG_INDEX_DIR / "chunks.json").write_text(
        json.dumps({"texts": texts, "meta": meta}), encoding="utf-8")
    print(f"RAG index: {len(texts)} chunks from {len(docs)} papers, dim {vecs.shape[1]}.")

if __name__ == "__main__":
    build()
