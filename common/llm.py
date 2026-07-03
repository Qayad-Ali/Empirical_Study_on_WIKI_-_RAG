
import sys, time, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import config
import ollama

_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)
_THINKING_MODELS = ("qwen", "deepseek", "-r1", "r1:")


def _clean(text):
    text = _THINK.sub("", text)
    text = re.sub(r"<think>.*", "", text, flags=re.DOTALL)
    return text.strip()


def complete(prompt, system=None, model=None, num_ctx=8192, max_tokens=4000, think=False):
    """think=False (default) -> qwen3 reasoning OFF: clean, concise, fair-cost answers.
    think=True -> reasoning ON (used by compile, where it improves page decomposition)."""
    model = model or config.GEN_MODEL
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    kwargs = dict(model=model, messages=messages,
                  options={"temperature": config.TEMPERATURE, "num_ctx": num_ctx, "num_predict": max_tokens})
    is_thinker = any(k in model.lower() for k in _THINKING_MODELS)
    if is_thinker:
        kwargs["think"] = bool(think)
    t0 = time.time()
    try:
        resp = ollama.chat(**kwargs)
    except TypeError:                     # older ollama client without think=
        kwargs.pop("think", None)
        if is_thinker and not think:
            kwargs["messages"][-1]["content"] += " /no_think"
        resp = ollama.chat(**kwargs)
    return {"text": _clean(resp["message"]["content"]),
            "in_tokens": resp.get("prompt_eval_count", 0),
            "out_tokens": resp.get("eval_count", 0),
            "latency_s": round(time.time() - t0, 2)}
