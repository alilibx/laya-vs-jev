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


def rank_in(get, k, pool):
    vs = [get(x) for x in pool if get(x) is not None]
    me = get(k)
    return None if me is None or not vs else (1 + sum(v > me for v in vs), len(vs), me == max(vs))


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
<header><a class="mark" href="/">{MARK}System One Bench</a><nav><a href="/#leaderboard">Leaderboard</a></nav></header>
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
    tiles = [
        tile("System One Index", fidx(idx) if idx is not None else '<span class="na">–</span>',
             rank_text(tr) if tr else ("Ran only some datasets" if idx is None else "Kept for reference")),
        tile("English", fidx(index(k, "English")) if index(k, "English") is not None else "–"),
        tile("Arabic", fidx(index(k, "Arabic")) if index(k, "Arabic") is not None else "–"),
        tile("Vision Index", fidx(vi) if vi is not None else '<span class="na">–</span>',
             rank_text(vr) if vr else ("No image input" if k in NO_IMAGE else "Not run on images")),
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
        rows.append(f'<tr><td>{e(sm["label"])} <small>{e(sm["lang"])}</small></td><td{" class=best" if rk and rk[2] else ""}>{100 * a:.1f}</td>'
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
        (". An earlier run, kept for reference." if reference else ".")
    body = f"""<p class="eyebrow">{e(m['maker'])} · {e(m['access'])}</p>
<h1><span class="dot" style="background:{color(k)}"></span>{e(m['label'])}</h1>
<p class="lede">{e(description)}</p>
<div class="tiles">{''.join(tiles)}</div>
<h2>Text datasets</h2><div class="card"><table>{head}{''.join(rows)}</table></div>
{f'<h2>Image datasets</h2><div class="card"><table>{head}{"".join(vrows)}</table></div>' if vrows else ''}
<h2>This run</h2>
<dl><dt>Model id</dt><dd><code>{e(m['slug'])}</code></dd><dt>Runs on</dt><dd>{e(m['access'])}</dd><dt>Run date</dt><dd>{e(m['run'])}</dd>
<dt>Latency</dt><dd>{e(m['latency'])}</dd><dt>Questions</dt><dd>{r['all']['n']:,}, {r['all'].get('failed', 0):,} failed (counted wrong)</dd></dl>
{f'<p class="note">{e(m["note"])}</p>' if m.get('note') else ''}
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


urls = [SITE + "/"]
urls += [model_page(k) for k in runs]
urls += [compare_page(a, b) for i, a in enumerate(text_rank) for b in text_rank[i + 1:]]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                 + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
# shields.io endpoint badges for the README: https://img.shields.io/endpoint?url=https://systemonebench.dev/badge/<name>.json
badges = {"models": ("models", str(len(runs)))}
if text_rank:
    badges["text-leader"] = ("text leader", f"{MODELS[text_rank[0]]['label']} · {fidx(index(text_rank[0]))}")
if vision_rank:
    badges["vision-leader"] = ("vision leader", f"{MODELS[vision_rank[0]]['label']} · {fidx(vindex(vision_rank[0]))}")
(OUT / "badge").mkdir(exist_ok=True)
for name, (label, message) in badges.items():
    (OUT / "badge" / f"{name}.json").write_text(json.dumps({"schemaVersion": 1, "label": label, "message": message, "color": "2a78d6"}) + "\n")
(OUT / "pages.json").write_text(json.dumps({k: f"/models/{slugs[k]}/" for k in runs}, indent=1) + "\n")
print(f"{len(runs)} model pages, {len(urls) - 1 - len(runs)} comparison pages, sitemap with {len(urls)} URLs")
