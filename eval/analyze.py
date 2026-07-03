
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                       
import matplotlib.pyplot as plt
import config

CHARTS = config.RESULTS_DIR / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

def wiki_build_tokens():
    p = config.RESULTS_DIR / "wiki_build_cost.txt"
    if not p.exists():
        return 0
    tin, tout, _ = p.read_text().strip().split(",")
    return int(tin) + int(tout)

def main():
    _g = [config.RESULTS_DIR / n for n in ("metrics_graded.csv", "metrics_graded_new.csv")
          if (config.RESULTS_DIR / n).exists()]
    df = pd.read_csv(max(_g, key=lambda q: q.stat().st_mtime))
    df["tokens"] = df["in_tokens"] + df["out_tokens"]

    per_run = df.groupby(["run", "system", "tier"])["correctness"].mean().reset_index()
    acc = per_run.groupby(["system", "tier"])["correctness"].agg(["mean", "min", "max"]).reset_index()

    perq = df.groupby("system").agg(
        in_tokens=("in_tokens", "mean"), out_tokens=("out_tokens", "mean"),
        tokens=("tokens", "mean"), latency=("latency_s", "mean"),
        correctness=("correctness", "mean"), faithfulness=("faithfulness", "mean")).reset_index()

    build = wiki_build_tokens()
    tok = perq.set_index("system")["tokens"]
    wiki_q, rag_q = float(tok.get("wiki", 0)), float(tok.get("rag", 0))
    diff = rag_q - wiki_q
    breakeven = build / diff if diff > 0 else float("inf")  
    tiers = sorted(df["tier"].unique()); x = np.arange(len(tiers)); w = 0.38
    plt.figure(figsize=(7, 4))
    for k, s in enumerate(["rag", "wiki"]):
        sub = acc[acc.system == s].set_index("tier").reindex(tiers)
        m = sub["mean"].values
        yerr = [m - sub["min"].values, sub["max"].values - m]
        plt.bar(x + (k - 0.5) * w, m, w, yerr=yerr, capsize=3, label=s)
    plt.xticks(x, [f"Tier {t}" for t in tiers]); plt.ylim(0, 2)
    plt.ylabel("mean correctness (0-2)"); plt.title("Accuracy by question tier"); plt.legend()
    plt.tight_layout(); plt.savefig(CHARTS / "accuracy_by_tier.png", dpi=120); plt.close()

    plt.figure(figsize=(5, 4))
    plt.bar(perq["system"], perq["tokens"])
    plt.ylabel("mean tokens / query"); plt.title("Cost per query")
    plt.tight_layout(); plt.savefig(CHARTS / "tokens_per_query.png", dpi=120); plt.close()

    n = np.arange(0, 201)
    plt.figure(figsize=(7, 4))
    plt.plot(n, build + wiki_q * n, label=f"wiki (build {build:,} + {wiki_q:.0f}/q)")
    plt.plot(n, rag_q * n, label=f"rag (0 build + {rag_q:.0f}/q)")
    if 0 < breakeven < 200:
        plt.axvline(breakeven, ls="--", color="gray")
        plt.text(breakeven + 2, plt.ylim()[1] * 0.1, f"break-even ~{breakeven:.0f} queries")
    plt.xlabel("number of queries"); plt.ylabel("cumulative tokens")
    plt.title("Amortized cost: when the wiki's build pays off"); plt.legend()
    plt.tight_layout(); plt.savefig(CHARTS / "cost_vs_queries.png", dpi=120); plt.close()

    lines = ["# Results summary", "",
             f"- Wiki build cost (one-time): **{build:,} tokens**",
             f"- Tokens/query — wiki **{wiki_q:.0f}**, rag **{rag_q:.0f}**",
             f"- Break-even: **~{breakeven:.0f} queries** before the wiki's build cost is repaid"
             + ("" if diff > 0 else "  (RAG is not more expensive/query here, so no break-even)"),
             "", "## Per-system overall", "",
             "| system | correctness | faithfulness | tokens/q | latency(s) |",
             "|---|---|---|---|---|"]
    for _, r in perq.iterrows():
        lines.append(f"| {r['system']} | {r['correctness']:.2f} | {r['faithfulness']:.2f} "
                     f"| {r['tokens']:.0f} | {r['latency']:.2f} |")
    lines += ["", "## Accuracy by tier (mean, min-max over runs)", "",
              "| tier | wiki | rag |", "|---|---|---|"]
    for t in tiers:
        wr = acc[(acc.system == "wiki") & (acc.tier == t)]
        rr = acc[(acc.system == "rag") & (acc.tier == t)]
        wc = f"{wr['mean'].iloc[0]:.2f} ({wr['min'].iloc[0]:.1f}-{wr['max'].iloc[0]:.1f})" if len(wr) else "-"
        rc = f"{rr['mean'].iloc[0]:.2f} ({rr['min'].iloc[0]:.1f}-{rr['max'].iloc[0]:.1f})" if len(rr) else "-"
        lines.append(f"| {t} | {wc} | {rc} |")
    (config.RESULTS_DIR / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    print(f"\nCharts -> {CHARTS}/  (3 PNGs)   Summary -> results/summary.md")

if __name__ == "__main__":
    main()
