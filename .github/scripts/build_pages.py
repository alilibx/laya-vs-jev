"""Write one static page per model run and one per pair of ranked models, plus sitemap.xml and the README's badges, into
the assembled site.

Run by .github/workflows/pages.yml after it copies site/ and the results into _site:

    python3 .github/scripts/build_pages.py _site

The numbers follow the main page's rules: the System One Index is the mean accuracy over every text dataset, the Vision
Index over every image dataset, and ranks count only the models the main page charts.
"""
import html
import json
import math
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
SITE = "https://systemonebench.dev"
R = json.loads((OUT / "results.json").read_text())
V = json.loads((OUT / "results_vision.json").read_text()) if (OUT / "results_vision.json").exists() else {}
M = json.loads((OUT / "meta.json").read_text())
MODELS, SUITES = M["models"], M["suites"]
VSUITES = (M.get("vision") or {}).get("suites", {})
NO_IMAGE = set((M.get("vision") or {}).get("no_image", []))
e = html.escape


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def page_slug(k):
    m = MODELS[k]
    label, maker = slugify(m["label"]), slugify(m["maker"])
    slug = label if label.startswith(maker) else f"{maker}-{label}"
    return f"{slug}-{slugify(m['tag'])}" if m.get("chart") is False and m.get("tag") else slug


runs = [k for k in MODELS if k in R]
charted = [k for k in runs if MODELS[k].get("chart") is not False]
slugs = {k: page_slug(k) for k in runs}
assert len(set(slugs.values())) == len(slugs), f"two runs share a page name: {slugs}"


def val(k, s, key="acc", res=R):
    return (res.get(k) or {}).get("suite:" + s, {}).get(key)


def index(k, lang=None):
    ss = [s for s in SUITES if lang is None or SUITES[s]["lang"] == lang]
    vs = [val(k, s) for s in ss]
    return None if None in vs else 100 * sum(vs) / len(vs)


def vindex(k):
    vs = [val(k, s, res=V) for s in VSUITES]
    return None if not V.get(k) or not vs or None in vs else 100 * sum(vs) / len(vs)


def per1k(k):
    c = R[k].get("cost") or {}
    return None if c.get("usd") is None else 1000 * c["usd"] / c["calls"]


def half_up(x, nd=0):  # the main page rounds with JavaScript, which rounds halves up
    f = 10 ** nd
    return math.floor(x * f + 0.5) / f


fidx = lambda v: f"{half_up(v, 1):.1f}"
fms = lambda v: f"{int(half_up(v)):,} ms"
fpct = lambda v: f"{half_up(v, 1):.1f}%"
fusd = lambda v: "Free" if v == 0 else (f"${v:.3f}" if v < 1 else f"${v:.2f}")
ordinal = lambda n: f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
local = lambda k: MODELS[k]["access"].startswith("Open weights")

text_rank = sorted([k for k in charted if index(k) is not None], key=index, reverse=True)
vision_rank = sorted([k for k in charted if vindex(k) is not None], key=vindex, reverse=True)


def index_without(k):
    """The index without the datasets a model is in-domain on, ranked against every ranked model on those same datasets."""
    ss = [s for s in SUITES if s not in MODELS[k].get("in_domain", [])]
    mean = lambda x: None if any(val(x, s) is None for s in ss) else 100 * sum(val(x, s) for s in ss) / len(ss)
    me, vs = mean(k), [mean(x) for x in text_rank]
    return None if me is None else (me, len(ss), 1 + sum(v is not None and v > me for v in vs), sum(v is not None for v in vs))


def rank_in(get, k, pool):
    vs = [get(x) for x in pool if get(x) is not None]
    me = get(k)
    return None if me is None or not vs else (1 + sum(v > me for v in vs), len(vs), me == max(vs))


# ---------- unusually high scores ----------
# A score is flagged when it's far above what the model's other datasets and every other model's score on this dataset
# predict. Expected scores come from a two-way fit (model strength + dataset difficulty) in log-odds, by Tukey's median
# polish, which the outliers it looks for can't pull towards themselves. A flag needs both a large z (sampling noise of
# the score plus the usual model-by-dataset spread) and a large gap in points. It often means a model trained on that
# dataset or one like it, but it isn't proof, and no flag isn't proof of the opposite.
OUTLIER_Z, OUTLIER_GAP = 3.5, 0.10


def median(xs):
    xs = sorted(xs)
    h = len(xs) // 2
    return 0.0 if not xs else xs[h] if len(xs) % 2 else (xs[h - 1] + xs[h]) / 2


def unusual_scores(suites, res, pool):
    """{(model, dataset): expected accuracy} for every unusually high score."""
    cells = {}
    for k in pool:
        for s in suites:
            m = (res.get(k) or {}).get("suite:" + s)
            if not m or m.get("failed", 0) > 0.1 * m["n"]:  # rejected cases say nothing about skill
                continue
            n = SUITES.get(s, {}).get("cases") or m["n"]
            p = min(max(m["acc"], 0.5 / n), 1 - 0.5 / n)
            cells[(k, s)] = {"x": math.log(p / (1 - p)), "noise": 1 / (n * p * (1 - p)), "acc": m["acc"]}
    resid = {c: v["x"] for c, v in cells.items()}
    row, col = {k: 0.0 for k in pool}, {s: 0.0 for s in suites}
    for _ in range(30):
        for k in pool:
            mk = median([v for c, v in resid.items() if c[0] == k])
            row[k] += mk
            for c in resid:
                if c[0] == k:
                    resid[c] -= mk
        for s in suites:
            ms = median([v for c, v in resid.items() if c[1] == s])
            col[s] += ms
            for c in resid:
                if c[1] == s:
                    resid[c] -= ms
    spread = max((1.4826 * median([abs(v) for v in resid.values()])) ** 2 - median([v["noise"] for v in cells.values()]), 0.0)
    flags = {}
    for (k, s), v in cells.items():
        expected = 1 / (1 + math.exp(-(row[k] + col[s])))
        if resid[(k, s)] / math.sqrt(v["noise"] + spread) >= OUTLIER_Z and v["acc"] - expected >= OUTLIER_GAP:
            flags[(k, s)] = expected
    return flags


FLAGS = unusual_scores(list(SUITES), R, charted)  # text track only: 5 image datasets are too few to fit
flag_text = lambda k, s: (f"{100 * val(k, s):.1f}%, {100 * (val(k, s) - FLAGS[(k, s)]):.0f} points above the {100 * FLAGS[(k, s)]:.0f}% "
                          f"its other datasets predict")


CSS = """
:root { color-scheme: light; --page: #f4f6f9; --surface: #fff; --ink: #121a2b; --ink-2: #4a5468; --muted: #6f7889;
  --rule: #dfe3ea; --accent: #2a78d6; --good: #1baf7a;
  --display: "Bricolage Grotesque", system-ui, sans-serif; --body: "IBM Plex Sans", system-ui, -apple-system, sans-serif; }
@media (prefers-color-scheme: dark) { :root { color-scheme: dark; --page: #0c121d; --surface: #131b29; --ink: #eef2f8;
  --ink-2: #b6bfce; --muted: #8b95a7; --rule: #263043; --accent: #5b9ef0; --good: #199e70; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--page); color: var(--ink); font: 16px/1.55 var(--body); -webkit-font-smoothing: antialiased; }
a { color: inherit; text-underline-offset: 3px; }
.wrap { max-width: 980px; margin: 0 auto; padding: 0 16px 56px; }
header { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 18px 0; border-bottom: 1px solid var(--rule); }
.mark { display: flex; align-items: center; gap: 10px; font: 800 19px/1 var(--display); text-decoration: none; }
header nav a { color: var(--ink-2); font-size: 14.5px; }
.eyebrow { font: 600 12.5px var(--body); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); margin: 40px 0 8px; }
h1 { font: 700 clamp(30px, 5vw, 46px)/1.08 var(--display); letter-spacing: -.02em; margin: 0 0 10px; }
h2 { font: 700 22px var(--display); margin: 40px 0 12px; }
.lede { color: var(--ink-2); max-width: 70ch; margin: 0; }
.dot { display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; vertical-align: 1px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 12px; margin-top: 24px; }
.tile { background: var(--surface); border: 1px solid var(--rule); border-radius: 12px; padding: 14px 16px; }
.tile .k { font-size: 12.5px; color: var(--muted); }
.tile .v { font: 700 28px/1.2 var(--display); margin-top: 4px; font-variant-numeric: tabular-nums; }
.tile .c { font-size: 13px; color: var(--ink-2); margin-top: 2px; }
.card { background: var(--surface); border: 1px solid var(--rule); border-radius: 12px; padding: 4px 18px; overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; }
th { font: 500 13px var(--body); color: var(--muted); text-align: right; padding: 12px 10px 8px; white-space: nowrap; }
td { padding: 10px; border-top: 1px solid var(--rule); text-align: right; white-space: nowrap; }
th:first-child, td:first-child { text-align: left; padding-left: 0; }
td:last-child, th:last-child { padding-right: 0; }
td.best { color: var(--good); font-weight: 600; }
td small, .na { color: var(--muted); }
dl { display: grid; grid-template-columns: auto 1fr; gap: 6px 16px; margin: 0; }
dt { color: var(--muted); } dd { margin: 0; overflow-wrap: anywhere; }
.links { display: flex; flex-wrap: wrap; gap: 8px; list-style: none; padding: 0; margin: 0; }
.links a { display: inline-block; border: 1px solid var(--rule); background: var(--surface); border-radius: 999px; padding: 4px 12px; font-size: 14px; text-decoration: none; }
.links a:hover { border-color: var(--accent); }
.note { color: var(--ink-2); font-size: 14px; }
footer { margin-top: 48px; padding-top: 18px; border-top: 1px solid var(--rule); color: var(--muted); font-size: 14px; display: flex; flex-wrap: wrap; gap: 8px 20px; }
"""
# The same cookieless page-view counter as the main page (see site/index.html).
ANALYTICS = """<script async src="https://us-assets.i.posthog.com/static/array.js" onload="posthog.init('phc_yCVgdaCDPPpPV77usF3Ar7FmwDY23xfCJaDN7hHSQprt', {api_host: 'https://us.i.posthog.com', cookieless_mode: 'always', person_profiles: 'identified_only', autocapture: false, disable_session_recording: true, capture_pageleave: true})"></script>"""
COLORS = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a", 4: "#eda100", 5: "#e87ba4", 6: "#008300", 7: "#4a3aa7", 8: "#e34948", 9: "#8a93a3", 10: "#0b6e75"}
color = lambda k: COLORS.get(MODELS[k].get("series"), "#8a93a3")
MARK = '<svg width="24" height="24" viewBox="0 0 26 26" aria-hidden="true"><rect x="1" y="7" width="24" height="12" rx="6" fill="none" stroke="currentColor" stroke-width="2"/><rect x="4" y="10" width="13" height="6" rx="3" fill="currentColor"/></svg>'


def page(path, title, description, body):
    url = f"{SITE}/{path}"
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="System One Bench">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
{ANALYTICS}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body><div class="wrap">
<header><a class="mark" href="/">{MARK}System One Bench</a><nav><a href="/#leaderboard">Leaderboard</a> · <a href="/benchmarks/">Benchmarks</a></nav></header>
{body}
<footer><span>Results under CC BY 4.0</span><a href="/">Full leaderboard</a><a href="/results.json">Raw results (JSON)</a><a href="https://github.com/alilibx/system-one-bench/blob/main/CONTRIBUTING.md">Benchmark rules</a><a href="https://github.com/alilibx/system-one-bench/releases">Releases</a><a href="https://www.linkedin.com/company/system-one-bench/">LinkedIn</a></footer>
</div></body>
</html>
"""
    dest = OUT / path / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc)
    return url


def tile(k, v, c=""):
    return f'<div class="tile"><div class="k">{e(k)}</div><div class="v">{v}</div><div class="c">{c}</div></div>'


def rank_text(r):
    return f"{ordinal(r[0])} of {r[1]}" if r else ""


def model_page(k):
    m, r = MODELS[k], R[k]
    idx, vi = index(k), vindex(k)
    tr = rank_in(index, k, text_rank) if k in charted else None
    vr = rank_in(vindex, k, vision_rank) if k in charted else None
    lat = r.get("latency_ms")
    in_domain = m.get("in_domain", [])
    wo = index_without(k) if in_domain else None
    tiles = [
        tile("System One Index", fidx(idx) if idx is not None else '<span class="na">–</span>',
             rank_text(tr) if tr else ("Ran only some datasets" if idx is None else "Kept for reference")),
        tile("English", fidx(index(k, "English")) if index(k, "English") is not None else "–"),
        tile("Arabic", fidx(index(k, "Arabic")) if index(k, "Arabic") is not None else "–"),
        tile("Vision Index", fidx(vi) if vi is not None else '<span class="na">–</span>',
             rank_text(vr) if vr else ("No image input" if k in NO_IMAGE else "Not run on images")),
        *([tile("Without in-domain datasets", fidx(wo[0]), f"{ordinal(wo[2])} of {wo[3]} on the same {wo[1]} datasets")] if wo else []),
        tile("Calibration error", fpct(100 * r["all"]["ece"]), "Lower is better"),
        tile("Median latency", fms(lat["p50"]) if lat else "–", "Local, not comparable" if local(k) else f"95th percentile {fms(lat['p95'])}" if lat else ""),
        tile("Cost per 1,000 calls", fusd(per1k(k)) if per1k(k) is not None else ("Local" if local(k) else "–"), m.get("cost_basis", "As billed")),
    ]
    rows = []
    for s, sm in SUITES.items():
        a = val(k, s)
        if a is None:
            continue
        rk = rank_in(lambda x: val(x, s), k, charted) if k in charted else None
        best = max(val(x, s) for x in charted if val(x, s) is not None)
        rows.append(f'<tr><td>{e(sm["label"])} <small>{e(sm["lang"])}{", in-domain" if s in in_domain else ""}{", unusually high" if (k, s) in FLAGS else ""}</small></td><td{" class=best" if rk and rk[2] else ""}>{100 * a:.1f}</td>'
                    f'<td>{rank_text(rk)}</td><td>{100 * best:.1f}</td><td>{fpct(100 * val(k, s, "ece"))}</td></tr>')
    vrows = []
    for s, sm in VSUITES.items():
        a = val(k, s, res=V)
        if a is None:
            continue
        pool = [x for x in charted if val(x, s, res=V) is not None]
        rk = rank_in(lambda x: val(x, s, res=V), k, pool) if k in charted else None
        vrows.append(f'<tr><td>{e(sm["label"])}</td><td{" class=best" if rk and rk[2] else ""}>{100 * a:.1f}</td><td>{rank_text(rk)}</td>'
                     f'<td>{100 * max(val(x, s, res=V) for x in pool):.1f}</td><td>{fpct(100 * val(k, s, "ece", V))}</td></tr>')
    head = "<tr><th>Dataset</th><th>Accuracy</th><th>Rank</th><th>Best on the board</th><th>Calibration error</th></tr>"
    others = [x for x in text_rank if x != k] if k in text_rank else []
    compare = "".join(f'<li><a href="/compare/{pair_slug(k, x)}/">vs {e(MODELS[x]["label"])}</a></li>' for x in others)
    scores = []
    if idx is not None:
        scores.append(f"{fidx(idx)} on the System One Index" + (f" ({rank_text(tr)})" if tr else ""))
    if vi is not None:
        scores.append(f"{fidx(vi)} on the Vision Index" + (f" ({rank_text(vr)})" if vr else ""))
    if not scores:
        scores = [f"{fidx(index(k, lang))} on the {lang} datasets, the only ones it ran" for lang in ("English", "Arabic") if index(k, lang) is not None]
    reference = m.get("chart") is False
    description = f"{m['label']} by {m['maker']}" + (f" scores {' and '.join(scores)}" if scores else " ran some of the datasets") + \
        f". Calibration error {fpct(100 * r['all']['ece'])}" + (f", median latency {fms(lat['p50'])}" if lat and not local(k) and not reference else "") + \
        (". An earlier run, kept for reference." if reference else ".") + \
        (f" {len(in_domain)} of the datasets it ran are in-domain: it trained on another split of them." if in_domain else "")
    body = f"""<p class="eyebrow">{e(m['maker'])} · {e(m['access'])}</p>
<h1><span class="dot" style="background:{color(k)}"></span>{e(m['label'])}</h1>
<p class="lede">{e(description)}</p>
<div class="tiles">{''.join(tiles)}</div>
<h2>Text datasets</h2><div class="card"><table>{head}{''.join(rows)}</table></div>
{f'<h2>Image datasets</h2><div class="card"><table>{head}{"".join(vrows)}</table></div>' if vrows else ''}
<h2>This run</h2>
<dl><dt>Model id</dt><dd><code>{e(m['slug'])}</code></dd><dt>Runs on</dt><dd>{e(m['access'])}</dd><dt>Run date</dt><dd>{e(m['run'])}</dd>
<dt>Latency</dt><dd>{e(m['latency'])}</dd><dt>Questions</dt><dd>{r['all']['n']:,}, {r['all'].get('failed', 0):,} failed (counted wrong)</dd></dl>
{f'<p class="note"><b>In-domain:</b> {e(", ".join(SUITES[s]["label"] for s in in_domain))}. {e(m.get("in_domain_source", ""))} We test a different split. The System One Index counts all {len(SUITES)} datasets for every model.</p>' if in_domain else ''}
{f'<p class="note">{e(m["note"])}</p>' if m.get('note') else ''}
{f'<p class="note"><b>Unusually high:</b> {e("; ".join(f"{SUITES[s]['label']}, {flag_text(k, s)}" for s in SUITES if (k, s) in FLAGS))}. A score this far above a model’s other results often means it trained on that dataset or one like it. It isn’t proof, and the score still counts.</p>' if any(x == k for x, _ in FLAGS) else ''}
{f'<h2>Compare</h2><ul class="links">{compare}</ul>' if compare else ''}
<p class="note">Ranks count the models charted on the <a href="/">leaderboard</a>. Every model gets the same cases and the same request, under the <a href="https://github.com/alilibx/system-one-bench/blob/main/CONTRIBUTING.md">benchmark rules</a>.</p>"""
    return page(f"models/{slugs[k]}", f"{m['label']} ({m['maker']}): System One Bench results", description, body)


def pair_slug(a, b):
    return "-vs-".join(sorted([slugs[a], slugs[b]]))


def compare_page(a, b):
    a, b = sorted([a, b], key=lambda x: slugs[x])
    ma, mb = MODELS[a], MODELS[b]
    wins = {a: 0, b: 0, None: 0}
    rows = []
    for s, sm in SUITES.items():
        x, y = val(a, s), val(b, s)
        w = a if x > y else b if y > x else None
        wins[w] += 1
        rows.append(f'<tr><td>{e(sm["label"])} <small>{e(sm["lang"])}</small></td><td{" class=best" if w == a else ""}>{100 * x:.1f}</td><td{" class=best" if w == b else ""}>{100 * y:.1f}</td></tr>')
    vrows = []
    for s, sm in VSUITES.items():
        x, y = val(a, s, res=V), val(b, s, res=V)
        if x is None and y is None:
            continue
        cell = lambda v, o: '<td class="na">–</td>' if v is None else f'<td{" class=best" if o is not None and v > o else ""}>{100 * v:.1f}</td>'
        vrows.append(f'<tr><td>{e(sm["label"])}</td>{cell(x, y)}{cell(y, x)}</tr>')

    def line(name, fa, fb, lower=False):
        x, y = fa, fb
        best = None if x is None or y is None or x[0] == y[0] else (a if (x[0] < y[0]) == lower else b)
        c = lambda v, k: '<td class="na">–</td>' if v is None else f'<td{" class=best" if best == k else ""}>{v[1]}</td>'
        return f"<tr><td>{name}</td>{c(x, a)}{c(y, b)}</tr>"

    num = lambda f, fmt: (lambda k: None if f(k) is None else (f(k), fmt(f(k))))
    lat = lambda k: None if local(k) or not R[k].get("latency_ms") else R[k]["latency_ms"]["p50"]
    summary_rows = "".join([
        line("System One Index", num(index, fidx)(a), num(index, fidx)(b)),
        line("English", num(lambda k: index(k, "English"), fidx)(a), num(lambda k: index(k, "English"), fidx)(b)),
        line("Arabic", num(lambda k: index(k, "Arabic"), fidx)(a), num(lambda k: index(k, "Arabic"), fidx)(b)),
        line("Vision Index", num(vindex, fidx)(a), num(vindex, fidx)(b)),
        line("Calibration error", num(lambda k: 100 * R[k]["all"]["ece"], fpct)(a), num(lambda k: 100 * R[k]["all"]["ece"], fpct)(b), lower=True),
        line("Median latency", num(lat, fms)(a), num(lat, fms)(b), lower=True),
        line("Cost per 1,000 calls", num(per1k, fusd)(a), num(per1k, fusd)(b), lower=True),
    ])
    n = len(SUITES)
    verdict = (f"{ma['label']} scores {fidx(index(a))} and {mb['label']} {fidx(index(b))} on the System One Index. "
               f"{ma['label']} is more accurate on {wins[a]} of {n} text datasets, {mb['label']} on {wins[b]}"
               + (f", and {wins[None]} are tied." if wins[None] else "."))
    head = f"<tr><th></th><th>{e(ma['label'])}</th><th>{e(mb['label'])}</th></tr>"
    body = f"""<p class="eyebrow">Head to head</p>
<h1>{e(ma['label'])} vs {e(mb['label'])}</h1>
<p class="lede">{e(verdict)} Same cases, same request, same scorer.</p>
<h2>Overall</h2><div class="card"><table>{head}{summary_rows}</table></div>
<h2>Text datasets, accuracy</h2><div class="card"><table>{head}{''.join(rows)}</table></div>
{f'<h2>Image datasets, accuracy</h2><div class="card"><table>{head}{"".join(vrows)}</table></div>' if vrows else ''}
<p class="note">Model pages: <a href="/models/{slugs[a]}/">{e(ma['label'])}</a> · <a href="/models/{slugs[b]}/">{e(mb['label'])}</a>. Latency for API models is the median per call through OpenRouter, timed from a cloud server with 8 calls in flight.</p>"""
    return page(f"compare/{pair_slug(a, b)}", f"{ma['label']} vs {mb['label']}: System One Bench", verdict, body)


# ---------- one page per benchmark, and a hub of every benchmark's leader ----------
# A leader is only called a leader when its lead is larger than sampling noise. Two accuracies are "tied" when their
# difference is within 1.96 standard errors of the difference, treating the two runs as independent samples. Every
# model answers the same cases, so this overstates the noise and errs towards calling a tie, never a lead.
Z = 1.96
BOX = (M.get("vision") or {}).get("box", {})


def bench_slug(s, sm):
    lang = sm.get("lang", "English")
    label = sm["label"]
    return slugify(label if lang == "English" or lang.lower() in label.lower() else f"{lang} {label}")


BENCHES = [{"key": s, "meta": sm, "res": R, "track": "Text", "lang": sm["lang"]} for s, sm in SUITES.items()]
BENCHES += [{"key": s, "meta": sm, "res": V, "track": "Vision", "lang": None} for s, sm in VSUITES.items()]
BENCHES += [{"key": s, "meta": sm, "res": V, "track": "Box", "lang": None} for s, sm in BOX.items()]
for b in BENCHES:
    b["slug"] = bench_slug(b["key"], b["meta"])
assert len({b["slug"] for b in BENCHES}) == len(BENCHES), "two benchmarks share a page name"


def standing(get, se, pool):
    """Rank `pool` by `get`, highest first, and say which models are statistically tied with the top one."""
    ks = sorted([k for k in pool if get(k) is not None], key=get, reverse=True)
    if not ks:
        return ks, []
    top = ks[0]
    tied = [k for k in ks[1:] if get(top) - get(k) <= Z * math.hypot(se(top), se(k))]
    return ks, tied


def bench_standing(b):
    s, res = b["key"], b["res"]
    get = lambda k: val(k, s, res=res)
    n = lambda k: b["meta"].get("cases") or val(k, s, "n", res)  # typed-decisions: 5 questions share a case
    se = lambda k: math.sqrt(max(get(k) * (1 - get(k)), 1e-9) / n(k))
    ks, tied = standing(get, se, charted)
    return ks, tied, get, se


def index_standing(f, suites, res):
    """The same tie rule for an index, the mean of independent per-dataset accuracies."""
    def se(k):
        parts = [val(k, s, res=res) for s in suites]
        ns = [(SUITES.get(s) or VSUITES.get(s) or {}).get("cases") or val(k, s, "n", res) for s in suites]
        return 100 * math.sqrt(sum(p * (1 - p) / m for p, m in zip(parts, ns))) / len(suites)
    return standing(f, se, charted)


def lead_text(ks, tied, get, scale=100):
    """One sentence on who leads and by how much, honest about ties."""
    if not ks:
        return "No model has run this benchmark yet."
    top = MODELS[ks[0]]["label"]
    if len(ks) == 1:
        return f"{top} is the only model on this benchmark so far."
    gap = scale * (get(ks[0]) - get(ks[1]))
    if not tied:
        return f"{top} leads by {gap:.1f} points over {MODELS[ks[1]]['label']}, more than sampling noise."
    if gap == 0:
        return f"{top} and {MODELS[ks[1]]['label']} share the top score" + (f", and {len(tied) - 1} more are within sampling noise." if len(tied) > 1 else ".")
    others = f"{MODELS[tied[0]]['label']}" + (f" and {len(tied) - 1} more" if len(tied) > 1 else "")
    return f"{top} has the top score, {gap:.1f} points ahead of {MODELS[ks[1]]['label']}, but {others} {'is' if len(tied) == 1 else 'are'} within sampling noise: a statistical tie for first."


BENCH_CSS = """<style>
.bar { position: relative; height: 10px; min-width: 120px; background: var(--rule); border-radius: 5px; }
.bar i { position: absolute; inset: 0 auto 0 0; border-radius: 5px; }
.bar b { position: absolute; top: -3px; bottom: -3px; border-left: 1px solid var(--ink-2); border-right: 1px solid var(--ink-2); }
.tag { display: inline-block; font-size: 11.5px; padding: 1px 7px; border-radius: 999px; border: 1px solid var(--rule); color: var(--ink-2); margin-left: 6px; vertical-align: 1px; }
.tag.lead { border-color: var(--good); color: var(--good); }
td.m a { text-decoration: none; } td.m a:hover { text-decoration: underline; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.grid a.tile { text-decoration: none; display: block; } .grid a.tile:hover { border-color: var(--accent); }
.grid .who { font: 700 19px/1.25 var(--display); margin-top: 6px; }
.grid .c b { color: var(--ink); font-variant-numeric: tabular-nums; }
.tag.flag, .grid .flag { border-color: #d97706; color: #b45309; }
.grid .flag { display: inline-block; font-size: 12px; margin-top: 6px; border: 1px solid; border-radius: 999px; padding: 0 8px; }
@media (prefers-color-scheme: dark) { .tag.flag, .grid .flag { border-color: #f59e0b; color: #fbbf24; } }
</style>"""


def bench_page(b):
    sm, s, res, track = b["meta"], b["key"], b["res"], b["track"]
    ks, tied, get, se = bench_standing(b)
    n = val(ks[0], s, "n", res) if ks else 0
    lead = lead_text(ks, tied, get)
    if ks and (ks[0], s) in FLAGS:
        lead += f" But its score is unusually high for {MODELS[ks[0]]['label']}: {flag_text(ks[0], s)}."
    flagged = [k for k in ks if (k, s) in FLAGS]
    in_domain = [k for k in ks if s in MODELS[k].get("in_domain", [])]
    hi = max([100 * get(k) + 100 * Z * se(k) for k in ks] + [100]) if ks else 100
    rows = []
    for i, k in enumerate(ks):
        a, m = get(k), MODELS[k]
        lo_ci, hi_ci = max(0.0, a - Z * se(k)), min(1.0, a + Z * se(k))
        tag = '<span class="tag lead">Leader</span>' if i == 0 else '<span class="tag lead">Tied for 1st</span>' if k in tied else ""
        tag += '<span class="tag">in-domain</span>' if k in in_domain else ""
        tag += f'<span class="tag flag" title="{e(flag_text(k, s))}">unusually high</span>' if (k, s) in FLAGS else ""
        extra = (f'<td>{val(k, s, "mean_iou", res):.2f}</td>' if track == "Box"
                 else f'<td>{100 * val(k, s, "macro_f1", res):.1f}</td>')
        rows.append(
            f'<tr><td>{1 + sum(get(x) > a for x in ks)}</td>'
            f'<td class="m"><span class="dot" style="background:{color(k)}"></span><a href="/models/{slugs[k]}/">{e(m["label"])}</a> <small>{e(m["maker"])}</small>{tag}</td>'
            f'<td><b>{100 * a:.1f}</b></td><td><small>{100 * lo_ci:.1f}–{100 * hi_ci:.1f}</small></td>'
            f'<td><div class="bar"><i style="width:{100 * a / hi * 100:.2f}%;background:{color(k)}"></i><b style="left:{100 * lo_ci / hi * 100:.2f}%;width:{100 * (hi_ci - lo_ci) / hi * 100:.2f}%"></b></div></td>'
            f'{extra}<td>{fpct(100 * val(k, s, "ece", res))}</td><td>{val(k, s, "failed", res) or 0}</td></tr>')
    acc_head = "Right (IoU ≥ 0.5)" if track == "Box" else "Accuracy"
    extra_head = "Mean IoU" if track == "Box" else "Macro-F1"
    head = f"<tr><th>Rank</th><th>Model</th><th>{acc_head}</th><th>95% interval</th><th></th><th>{extra_head}</th><th>Calibration error</th><th>Failed</th></tr>"
    baseline = []
    if sm.get("constant") is not None:
        baseline = [tile("Best constant answer", f"{100 * sm['constant']:.1f}", "Always giving the most common label"),
                    tile("Random guess", f"{100 * sm['chance']:.1f}", "Uniform over the options")]
    tiles = [tile("Leader" if not tied else "Top score", e(MODELS[ks[0]]["label"]) if ks else "–",
                  f"{100 * get(ks[0]):.1f}" + (f", tied with {len(tied)} within noise" if tied else "") if ks else ""),
             tile("Lead over 2nd", f"{100 * (get(ks[0]) - get(ks[1])):.1f}" if len(ks) > 1 else "–", "Points of accuracy"),
             tile("Models", str(len(ks)), "Charted on the leaderboard"),
             tile("Cases" if not sm.get("cases") else "Questions", f"{n:,}", f"{sm['cases']} cases" if sm.get("cases") else ""),
             *baseline]
    where = {"Text": f"Text track · {b['lang']}", "Vision": "Vision track", "Box": "Vision track · Box questions"}[track]
    counts = {"Text": f"It counts towards the System One Index" + (f" and its {b['lang']} sub-index." if b["lang"] in ("English", "Arabic") else "."),
              "Vision": "It counts towards the Vision Index.", "Box": "Box questions are scored apart and stay out of the Vision Index."}[track]
    source = f'<a href="https://huggingface.co/datasets/{e(sm["source"])}">{e(sm["source"])}</a>, {e(sm["split"])} split' if sm.get("source") else "–"
    description = f"{sm['label']}: {sm['task']}. {lead}"
    body = f"""{BENCH_CSS}<p class="eyebrow">{e(where)} · <a href="/benchmarks/">All benchmarks</a></p>
<h1>{e(sm['label'])}</h1>
<p class="lede">{e(sm['task'])}. {e(lead)}</p>
<div class="tiles">{''.join(tiles)}</div>
<h2>Leaderboard</h2>
<div class="card"><table>{head}{''.join(rows)}</table></div>
<p class="note">The bar is accuracy; the bracket on it is the 95% interval for {n:,} {"questions over " + str(sm["cases"]) + " cases, counted as " + str(sm["cases"]) + " samples" if sm.get("cases") else "cases"}. <b>Tied for 1st</b> marks every model whose gap to the leader is within sampling noise (1.96 standard errors of the difference, treating the runs as independent). A failed call counts as wrong.{" <b>In-domain</b> models trained on another split of this dataset, by their maker's own account." if in_domain else ""}{" <b>Unusually high</b> marks a score far above what that model's other datasets, and every other model's score here, predict (hover for the numbers). It often means the model trained on this dataset or one like it; it isn't proof, and the score still counts." if flagged else ""}</p>
<h2>About this benchmark</h2>
<dl><dt>Question</dt><dd>{e(sm['task'])}</dd><dt>Source</dt><dd>{source}</dd><dt>Sample</dt><dd>{e(sm.get('sample', '–'))}</dd>
<dt>Pinned</dt><dd>Every source is pinned to an exact commit, and the cases are frozen by hash in <a href="https://github.com/alilibx/system-one-bench/blob/main/data.lock.json">data.lock.json</a>.</dd></dl>
<p class="note">{e(counts)} Every model gets the same cases and the same request, under the <a href="https://github.com/alilibx/system-one-bench/blob/main/CONTRIBUTING.md">benchmark rules</a>.</p>"""
    return page(f"benchmarks/{b['slug']}", f"{sm['label']} leaderboard: System One Bench", description, body)


def hub_page():
    def card(href, label, sub, ks, tied, get, scale=100, flag=False):
        if not ks:
            return ""
        status = (f"leads by <b>{scale * (get(ks[0]) - get(ks[1])):.1f}</b>" if len(ks) > 1 and not tied
                  else f"tied with {e(MODELS[tied[0]]['label'])}" + (f" and {len(tied) - 1} more" if len(tied) > 1 else "") if tied
                  else "the only model so far")
        return (f'<a class="tile" href="{href}"><div class="k">{e(label)} · {e(sub)}</div>'
                f'<div class="who"><span class="dot" style="background:{color(ks[0])}"></span>{e(MODELS[ks[0]]["label"])}</div>'
                f'<div class="c"><b>{scale * get(ks[0]):.1f}</b> · {status} · {len(ks)} model{"s" if len(ks) != 1 else ""}</div>'
                + (f'<div class="flag">Unusually high for this model</div>' if flag else "") + "</a>")

    tk, tt = index_standing(index, list(SUITES), R)
    idx_cards = [card("/#index", "System One Index", f"{len(SUITES)} text datasets", tk, tt, index, 1)]
    for lang in ("English", "Arabic"):
        f = lambda k, lang=lang: index(k, lang)
        lk, lt = index_standing(f, [s for s in SUITES if SUITES[s]["lang"] == lang], R)
        idx_cards.append(card("/#index", f"{lang} sub-index", f"{sum(SUITES[s]['lang'] == lang for s in SUITES)} datasets", lk, lt, f, 1))
    if VSUITES:
        vk, vt = index_standing(vindex, list(VSUITES), V)
        idx_cards.append(card("/#vision", "Vision Index", f"{len(VSUITES)} image datasets", vk, vt, vindex, 1))
    groups = []
    for title, pick in [*[(f"Text, {lang}", lambda b, lang=lang: b["track"] == "Text" and b["lang"] == lang) for lang in M["languages"]],
                        ("Vision", lambda b: b["track"] in ("Vision", "Box"))]:
        cards = []
        for b in filter(pick, BENCHES):
            ks, tied, get, _ = bench_standing(b)
            cards.append(card(f"/benchmarks/{b['slug']}/", b["meta"]["label"], b["meta"]["task"], ks, tied, get,
                              flag=bool(ks) and (ks[0], b["key"]) in FLAGS))
        if any(cards):
            groups.append(f'<h2>{e(title)}</h2><div class="grid">{"".join(cards)}</div>')
    ties = sum(1 for b in BENCHES if bench_standing(b)[1])
    description = (f"The leader of every System One Bench benchmark: {len(BENCHES)} datasets and {len(idx_cards)} indexes. "
                   f"On {ties} of the {len(BENCHES)} datasets, the top score is a statistical tie.")
    body = f"""{BENCH_CSS}<p class="eyebrow">Every benchmark</p>
<h1>Benchmark leaders</h1>
<p class="lede">{e(description)} A model is only called the leader when its lead is larger than sampling noise; otherwise the card says who it's tied with. Each card opens that benchmark's full leaderboard.</p>
<h2>Indexes</h2><div class="grid">{''.join(idx_cards)}</div>
{''.join(groups)}
<p class="note">Ranks count the {len(charted)} models charted on the <a href="/">leaderboard</a>. Ties use 1.96 standard errors of the difference in accuracy, treating two runs as independent samples, which errs towards calling a tie. <b>Unusually high</b> marks a leader whose score is far above what its other datasets predict, which often means it trained on that dataset or one like it.</p>"""
    return page("benchmarks", "Benchmark leaders: System One Bench", description, body)


urls = [SITE + "/"]
urls += [model_page(k) for k in runs]
urls += [compare_page(a, b) for i, a in enumerate(text_rank) for b in text_rank[i + 1:]]
urls += [hub_page()] + [bench_page(b) for b in BENCHES]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                 + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
# shields.io endpoint badges for the README: https://img.shields.io/endpoint?url=https://systemonebench.dev/badge/<name>.json
badges = {"models": ("models", str(len(runs)))}
if text_rank:
    badges["text-leader"] = ("text leader", f"{MODELS[text_rank[0]]['label']} · {fidx(index(text_rank[0]))}")
if vision_rank:
    badges["vision-leader"] = ("vision leader", f"{MODELS[vision_rank[0]]['label']} · {fidx(vindex(vision_rank[0]))}")
for b in BENCHES:  # badge/bench-<benchmark>.json: that benchmark's leader, or "tie" when the lead is within noise
    ks, tied, get, _ = bench_standing(b)
    if ks:
        badges[f"bench-{b['slug']}"] = (f"{b['meta']['label']} leader",
                                        f"{MODELS[ks[0]]['label']} · {100 * get(ks[0]):.1f}" + (f" (tied with {len(tied)})" if tied else ""))
(OUT / "badge").mkdir(exist_ok=True)
for name, (label, message) in badges.items():
    (OUT / "badge" / f"{name}.json").write_text(json.dumps({"schemaVersion": 1, "label": label, "message": message, "color": "2a78d6"}) + "\n")
(OUT / "pages.json").write_text(json.dumps({k: f"/models/{slugs[k]}/" for k in runs}, indent=1) + "\n")
flags = {}
for (k, s), expected in FLAGS.items():
    flags.setdefault(k, {})[s] = round(expected, 4)
(OUT / "flags.json").write_text(json.dumps(flags, indent=1) + "\n")  # read by the main page's leaderboard
(OUT / "benchmarks.json").write_text(json.dumps({b["key"]: f"/benchmarks/{b['slug']}/" for b in BENCHES}, indent=1) + "\n")
n_compare = len(text_rank) * (len(text_rank) - 1) // 2
print(f"{len(runs)} model pages, {n_compare} comparison pages, {len(BENCHES)} benchmark pages and a hub, sitemap with {len(urls)} URLs")
