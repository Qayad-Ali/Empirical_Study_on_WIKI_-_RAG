
import functools
import config

@functools.lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(config.EMBED_MODEL)

def embed_texts(texts):
    """Return an (n, d) float32 array of L2-normalized embeddings."""
    return _model().encode(list(texts), normalize_embeddings=True,
                           convert_to_numpy=True).astype("float32")
