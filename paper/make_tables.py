"""Write the paper's tables and headline numbers from results.json, results_vision.json and site/meta.json.

    python3 paper/make_tables.py      # -> paper/tables.tex, paper/numbers.tex

Every number in the paper comes from these files, so re-running this after a new round updates the paper.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = json.loads((ROOT / "results.json").read_text())
V = json.loads((ROOT / "results_vision.json").read_text())
M = json.loads((ROOT / "site/meta.json").read_text())
SUITES, VSUITES = M["suites"], M["vision"]["suites"]
charted = [k for k in M["models"] if k in R and M["models"][k].get("chart") is not False]
local = lambda k: M["models"][k]["access"].startswith("Open weights")
acc = lambda k, s, res=R: res.get(k, {}).get("suite:" + s, {}).get("acc")


def index(k, lang=None):
    vs = [acc(k, s) for s in SUITES if lang is None or SUITES[s]["lang"] == lang]
    return None if None in vs else 100 * sum(vs) / len(vs)


def vindex(k):
    vs = [acc(k, s, V) for s in VSUITES]
    return None if k not in V or None in vs else 100 * sum(vs) / len(vs)


def n_items(s, res=R, k=None):
    # typed-decisions has 5 questions per case; its decisions aren't independent, so count cases for the error bar.
    n = (res[k] if k else R["or_jev"])["suite:" + s]["n"]
    return n // 5 if s == "typed-decisions" else n


def index_se(k):
    # Binomial standard error of the mean of per-dataset accuracies, treating datasets as independent.
    return 100 * math.sqrt(sum(acc(k, s) * (1 - acc(k, s)) / n_items(s) for s in SUITES)) / len(SUITES)


def half_up(x, nd=1):
    f = 10 ** nd
    return math.floor(x * f + 0.5) / f


f1 = lambda x: f"{half_up(x):.1f}"
ms = lambda x: f"{int(half_up(x, 0)):,}".replace(",", "{,}")
usd = lambda k: (lambda c: "free" if c == 0 else f"\\${c:.3f}")(1000 * R[k]["cost"]["usd"] / R[k]["cost"]["calls"]) if (R[k].get("cost") or {}).get("usd") is not None else "local"
tex = lambda s: s.replace("&", "\\&").replace("_", "\\_").replace("%", "\\%")

text_rank = sorted([k for k in charted if index(k) is not None], key=index, reverse=True)
vision_rank = sorted([k for k in charted if vindex(k) is not None], key=vindex, reverse=True)
best = lambda f, ks, low=False: (min if low else max)(f(k) for k in ks)

lines = []
# Table 1: datasets.
lines += [r"\begin{table}[t]\centering\small", r"\caption{Datasets. $n$ is the number of cases; typed decisions asks 5 questions per case.}\label{tab:data}",
          r"\begin{tabular}{llrp{8cm}}\toprule Dataset & Language & $n$ & Question \\ \midrule"]
for s, m in SUITES.items():
    lines.append(f"{tex(m['label'])} & {m['lang']} & {n_items(s)} & {tex(m['task'])} \\\\")
lines.append(r"\midrule")
for s, m in list(VSUITES.items()) + list(M["vision"]["box"].items()):
    lines.append(f"{tex(m['label'])} & image & {V['or_jev_114']['suite:' + s]['n']} & {tex(m['task'])} \\\\")
lines += [r"\bottomrule\end{tabular}\end{table}", ""]

# Table 2: text leaderboard.
lines += [r"\begin{table*}[t]\centering\small",
          r"\caption{Text track, ranked by the System One Index (mean accuracy over the 16 datasets, equal weight). $\pm$ is a 95\% interval from binomial sampling error. Calibration is top-label ECE. Latency is the median per call through OpenRouter, timed from one machine, except for the " + str(sum(map(local, text_rank))) + r" open-weight models run locally. Failed answers count as wrong. Best value per column in bold; latency compares API models only.}\label{tab:text}",
          r"\resizebox{\textwidth}{!}{\begin{tabular}{rllrrrrrrr}\toprule \# & Model & Maker & Index & English & Arabic & ECE (\%) & Median ms & \$ / 1k calls & Failed \\ \midrule"]
api = [k for k in text_rank if not local(k)]
bI, bE, bA = best(index, text_rank), best(lambda k: index(k, "English"), text_rank), best(lambda k: index(k, "Arabic"), text_rank)
bC = best(lambda k: R[k]["all"]["ece"], text_rank, True)
bL = best(lambda k: R[k]["latency_ms"]["p50"], api, True)
bold = lambda v, b, s: f"\\textbf{{{s}}}" if v == b else s
# Local latency marks: dagger for the Apple GPU (Laya), double dagger for the cloud CPU runs.
mark = lambda k: "$^\\dagger$" if "Apple" in M["models"][k]["latency"] else "$^\\ddagger$"
for i, k in enumerate(text_rank, 1):
    m, r = M["models"][k], R[k]
    lat = r["latency_ms"]["p50"]
    lines.append(" & ".join([str(i), tex(m["label"]), tex(m["maker"]),
        bold(index(k), bI, f1(index(k))) + f" $\\pm${f1(1.96 * index_se(k))}",
        bold(index(k, "English"), bE, f1(index(k, "English"))), bold(index(k, "Arabic"), bA, f1(index(k, "Arabic"))),
        bold(r["all"]["ece"], bC, f1(100 * r["all"]["ece"])),
        (ms(lat) + mark(k)) if local(k) else bold(lat, bL, ms(lat)), usd(k), f"{r['all'].get('failed', 0):,}"]) + r" \\")
lines += [r"\bottomrule\end{tabular}}", r"\\[2pt]\footnotesize $^\dagger$Local, one call at a time on an Apple M5 GPU. $^\ddagger$Local, one call at a time on a 4-vCPU cloud CPU (llama.cpp Q8\_0, or PyTorch for Naluri). Neither is comparable with API latency.", r"\end{table*}", ""]

# Table 3: vision leaderboard.
heads = " & ".join(tex(VSUITES[s].get("short", VSUITES[s]["label"])) for s in VSUITES)
lines += [r"\begin{table*}[t]\centering\small",
          r"\caption{Vision track, ranked by the Vision Index (mean accuracy over the 5 image datasets). Text rank is the model's place on the System One Index in Table~\ref{tab:text}.}\label{tab:vision}",
          r"\resizebox{\textwidth}{!}{\begin{tabular}{rlr" + "r" * len(VSUITES) + r"rr}\toprule \# & Model & Vision Index & " + heads + r" & ECE (\%) & Text rank \\ \midrule"]
for i, k in enumerate(vision_rank, 1):
    cols = [f1(100 * acc(k, s, V)) for s in VSUITES]
    lines.append(" & ".join([str(i), tex(M["models"][k]["label"]), f1(vindex(k))] + cols + [f1(100 * V[k]["all"]["ece"]), str(text_rank.index(k) + 1)]) + r" \\")
lines += [r"\bottomrule\end{tabular}}\end{table*}", ""]
(ROOT / "paper/tables.tex").write_text("\n".join(lines) + "\n")

# Headline numbers used in the prose.
n = {}
n["nModels"] = len(text_rank)
n["nApi"] = len(api)
n["nMakers"] = len({M["models"][k]["maker"] for k in api})
n["nVision"] = len(vision_rank)
n["nLocal"] = sum(map(local, text_rank))
# The best open-weight models, and the API model ranked just above them.
lw = [k for k in text_rank if local(k)]
above = text_rank[text_rank.index(lw[0]) - 1]
n["localA"], n["localAIdx"], n["localARank"] = M["models"][lw[0]]["label"], f1(index(lw[0])), text_rank.index(lw[0]) + 1
n["localB"], n["localBIdx"], n["localBRank"] = M["models"][lw[1]]["label"], f1(index(lw[1])), text_rank.index(lw[1]) + 1
n["localCI"] = f1(max(1.96 * index_se(k) for k in lw[:2]))
n["aboveLocal"], n["aboveLocalIdx"] = M["models"][above]["label"], f1(index(above))
n["aboveLocalGap"] = f1(index(above) - index(lw[1]))
by_ece = sorted(text_rank, key=lambda k: R[k]["all"]["ece"])
n["eceSecond"], n["eceSecondVal"], n["eceSecondRank"] = M["models"][by_ece[1]]["label"], f1(100 * R[by_ece[1]]["all"]["ece"]), text_rank.index(by_ece[1]) + 1
# How the smallest models lose Arabic: d1-omni-600M against the full d1, and Kev 0.8B's English-Arabic gap.
n["omniEnGap"] = f1(index("liquid_d1", "English") - index("d1_omni_600m", "English"))
n["omniArGap"] = f1(index("liquid_d1", "Arabic") - index("d1_omni_600m", "Arabic"))
n["kevSmallGap"] = f1(index("kev_0_8b", "English") - index("kev_0_8b", "Arabic"))
n["dThreeEdgeLite"] = f1(index("d3_lite") - index("d3_edge"))
n["dThreeLiteNano"] = f1(index("d3_nano") - index("d3_lite"))
n["topText"], n["topTextIdx"] = M["models"][text_rank[0]]["label"], f1(index(text_rank[0]))
n["secondText"], n["secondTextIdx"] = M["models"][text_rank[1]]["label"], f1(index(text_rank[1]))
n["topTextGap"] = f1(index(text_rank[0]) - index(text_rank[1]))
n["topTextCI"] = f1(1.96 * index_se(text_rank[0]))
n["topFiveSpread"] = f1(index(text_rank[0]) - index(text_rank[4]))
n["topVision"], n["topVisionIdx"] = M["models"][vision_rank[0]]["label"], f1(vindex(vision_rank[0]))
n["topTextVisionRank"] = str(vision_rank.index(text_rank[0]) + 1)
n["topVisionTextRank"] = str(text_rank.index(vision_rank[0]) + 1)
eces = [100 * R[k]["all"]["ece"] for k in text_rank]
n["eceMin"], n["eceMax"] = f1(min(eces)), f1(max(eces))
gaps_en = [100 * (acc(k, "img_sst2", V) - acc(k, "sst2")) for k in vision_rank]
gaps_ar = [100 * (acc(k, "img_ar_sentiment", V) - acc(k, "ar_sentiment")) for k in vision_rank]
n["enGapWorst"], n["arGapBest"], n["arGapWorst"] = f1(-min(gaps_en)), f1(-max(gaps_ar)), f1(-min(gaps_ar))
box = V["or_jev_114"]["suite:img_refcoco"]
n["boxRight"], n["boxConf"], n["boxAuroc"], n["boxIou"] = f1(100 * box["acc"]), f1(100 * box["mean_conf"]), f"{box['conf_auroc']:.2f}", f"{box['mean_iou']:.2f}"
n["nCases"], n["nDecisions"] = "3{,}250", f"{R['or_jev']['all']['n']:,}".replace(",", "{,}")
macro = lambda name, v: f"\\newcommand{{\\{name}}}{{{tex(str(v))}}}"
(ROOT / "paper/numbers.tex").write_text("\n".join(macro(k, v) for k, v in n.items()) + "\n")
print("\n".join(f"{k} = {v}" for k, v in n.items()))
