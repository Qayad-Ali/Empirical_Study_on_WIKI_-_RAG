import ollama
import config
response=ollama.chat(model=config.GEN_MODEL,messages=[{"role":"user","content":"say hello in 5 words"}],)
print("reply:",response["message"]["content"])
print("input token:",response["prompt_eval_count"])
print("output token:",response["eval_count"])