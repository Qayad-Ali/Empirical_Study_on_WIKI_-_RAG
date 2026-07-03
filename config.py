
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RAW_DIR=ROOT/"raw"
WIKI_DIR=ROOT/"wiki"
RAG_INDEX_DIR=ROOT/"rag"/"index"
RESULTS_DIR=ROOT/"results"
REPORTS_DIR=ROOT/"reports"
#creating the folders
for d in (RAW_DIR,WIKI_DIR,RAG_INDEX_DIR,RESULTS_DIR,REPORTS_DIR):
    d.mkdir(parents=True,exist_ok=True)

##llm setting
PROVIDER="ollama"
GEN_MODEL="qwen3:8b"
JUDGE_MODEL="llama3.1:8b"
TEMPERATURE=0

##RAG SETTINGS
EMBED_MODEL="all-MiniLM-L6-v2"
CHUNK_SIZE_WORDS=220
CHUNK_OVERLAP_WORDS=40
TOP_K=5
SOURCE_BUDGET_WORDS = 6000   # both systems see exactly this much per paper

##EVAL SETTINGS
N_RUNS = 3                   # run the whole eval this many times -> mean +/- spread

ARXIV_PAPERS=[
   {"id": "transformer", "arxiv_id": "1706.03762", "title": "Attention Is All You Need"},
    {"id": "bert",        "arxiv_id": "1810.04805", "title": "BERT"},
    {"id": "gpt3",        "arxiv_id": "2005.14165", "title": "GPT-3: Language Models are Few-Shot Learners"},
    {"id": "foundation",  "arxiv_id": "2108.07258", "title": "On the Opportunities and Risks of Foundation Models", "skip": True},
    {"id": "instructgpt", "arxiv_id": "2203.02155", "title": "InstructGPT: Training LMs to follow instructions with human feedback"},
]
