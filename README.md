<h1 align="center">
  <a href="https://systemonebench.dev/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
      <img src="docs/assets/logo.svg" alt="System One Bench" width="420">
    </picture>
  </a>
</h1>

<p align="center"><b>Every decision model, measured the same way.</b><br>
Accuracy, calibration, latency and cost on frozen data, with byte-identical requests.</p>

<p align="center">
  <a href="https://systemonebench.dev/"><img src="https://img.shields.io/website?url=https%3A%2F%2Fsystemonebench.dev&label=leaderboard&up_message=live&up_color=2a78d6" alt="Leaderboard"></a>
  <a href="https://github.com/alilibx/system-one-bench/releases"><img src="https://img.shields.io/github/v/release/alilibx/system-one-bench?label=release&color=2a78d6" alt="Latest release"></a>
  <a href="https://github.com/alilibx/system-one-bench/actions/workflows/data.yml"><img src="https://img.shields.io/github/actions/workflow/status/alilibx/system-one-bench/data.yml?branch=main&label=frozen%20data" alt="Frozen data check"></a>
  <a href="https://github.com/alilibx/system-one-bench/actions/workflows/pages.yml"><img src="https://img.shields.io/github/actions/workflow/status/alilibx/system-one-bench/pages.yml?branch=main&label=site" alt="Site deploy"></a>
  <br>
  <a href="https://systemonebench.dev/#leaderboard"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fsystemonebench.dev%2Fbadge%2Fmodels.json" alt="Models on the board"></a>
  <a href="https://systemonebench.dev/#index"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fsystemonebench.dev%2Fbadge%2Ftext-leader.json" alt="Text leader"></a>
  <a href="https://systemonebench.dev/#vision"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fsystemonebench.dev%2Fbadge%2Fvision-leader.json" alt="Vision leader"></a>
  <a href="#full-benchmark"><img src="https://img.shields.io/badge/cases-3%2C250%20text%20%C2%B7%201%2C200%20image-555" alt="Cases"></a>
  <a href="#full-benchmark"><img src="https://img.shields.io/badge/languages-EN%20%C2%B7%20FR%20%C2%B7%20AR-555" alt="Languages"></a>
  <br>
  <a href="LICENSE"><img src="https://img.shields.io/badge/code-Apache--2.0-555" alt="Code licence: Apache-2.0"></a>
  <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/results-CC%20BY%204.0-555" alt="Results licence: CC BY 4.0"></a>
  <a href="CITATION.cff"><img src="https://img.shields.io/badge/cite-CITATION.cff-555" alt="Cite this repository"></a>
  <a href="https://github.com/alilibx/system-one-bench/issues/new?template=request-a-model.yml"><img src="https://img.shields.io/badge/request-a%20model-2a78d6" alt="Request a model"></a>
</p>

<p align="center">
  <a href="https://systemonebench.dev/"><b>Leaderboard</b></a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="CONTRIBUTING.md">Benchmark rules</a> ·
  <a href="https://github.com/alilibx/system-one-bench/releases">Releases</a> ·
  <a href="#licence-and-citation">Cite</a> ·
  <a href="https://github.com/alilibx/system-one-bench/issues/new?template=request-a-model.yml">Request a model</a> ·
  <a href="https://www.linkedin.com/company/system-one-bench/">LinkedIn</a>
</p>

A benchmark for System One models: models that read a `state` and answer named questions with typed, probabilistic
answers (`noul` yes/no, `choice`, and ordered `score`) in one fast call. Every model gets byte-identical `state` +
`questions` bodies, and is scored on accuracy, calibration, latency, and cost across 16 labelled datasets (3,250 cases,
4,850 decisions) in English, French, and Arabic. A [vision track](#vision-track) adds 6 image datasets (1,200 cases) for
the models that read images, including Box questions. A live race runs two models side by side on the same cases.

Models covered so far:

| Model | Maker | How it runs | Round |
|---|---|---|---|
| Jev 1.13 (`typesafe/jev-1.13`) | TypeSafe | OpenRouter Decisions API, or the TypeSafe API | all |
| Jev 1.14 (`typesafe/jev-1.14`), preview | TypeSafe | OpenRouter Decisions API | 2026-10-15, text and vision |
| GPT-6 Luna Decisions (`openai/gpt-6-luna-decisions`) | OpenAI | OpenRouter Decisions API | 2026-10-07 |
| Decider V1.2 and Decider Flash V1.2 (`perplexity/pplx-decider-v1.2`, `perplexity/pplx-decider-flash-v1.2`) | Perplexity | OpenRouter Decisions API | 2026-10-25, text and vision |
| Decider V1.1 27B (`perplexity/pplx-decider-v1.1-27b`), retired | Perplexity | OpenRouter Decisions API, no longer served | 2026-10-12 |
| Decider V1 27B (`perplexity/pplx-decider-v1-27b`), retired | Perplexity | OpenRouter Decisions API, no longer served | 2026-10-07 |
| d1 (`liquid/d1`) | Liquid AI | OpenRouter Decisions API | 2026-10-07 |
| d1-ultra (`liquid/d1-ultra`) | Liquid AI | OpenRouter Decisions API | 2026-10-25, text and vision |
| d1.1 (`liquid/d1.1`) | Liquid AI | OpenRouter Decisions API | 2026-10-30, text and vision |
| Clef and Clef Flash (`cloudflare/clef`, `cloudflare/clef-flash`) | Cloudflare | OpenRouter Decisions API | 2026-10-07 |
| Clef Omni (`cloudflare/clef-omni`) | Cloudflare | OpenRouter Decisions API | 2026-10-12 |
| Solar Decide (`upstage/solar-decide`) | Upstage | OpenRouter Decisions API | 2026-10-07 |
| Solar Decide Flash (`upstage/solar-decide-flash`) | Upstage | OpenRouter Decisions API | 2026-10-12 |
| Mercury Decide (`inception/mercury-decide:free`) | Inception | OpenRouter Decisions API, free tier | 2026-10-07 |
| Kev 4B (`jaredpalmer/kev-4b`) | Jared Palmer | OpenRouter Decisions API | 2026-10-07 |
| Tev1 4B Experimental (`togethercomputer/tev1-4b-experimental`) | Together AI | OpenRouter Decisions API | 2026-10-07 |
| Microsoft-Decision-1 (`microsoft/microsoft-decision-1`) | Microsoft | OpenRouter Decisions API | 2026-10-12 |
| Drex v1.5 (`nace-ai/drex-v1.5`) | Nace AI | OpenRouter Decisions API | 2026-10-12 |
| Drex v2.0 and Drex Max (`nace-ai/drex-v2.0`, `nace-ai/drex-max`) | Nace AI | OpenRouter Decisions API | 2026-10-25 |
| Span-02 (`respan/span-02`) | Respan | OpenRouter Decisions API | 2026-10-25, text and vision |
| Classify-1 (`scaledown/classify-1`) | ScaleDown | OpenRouter Decisions API; rejects most of our cases | 2026-10-25 |
| Mammoth 1, Elephant 1 and Joey 1 (`baseten/mammoth-1`, `baseten/elephant-1`, `baseten/joey-1`) | Baseten | OpenRouter Decisions API | 2026-10-30 |
| GLiDE (`fastino/GLiDE`) | Fastino | Fastino API | 2026-11-02, text and vision |
| Celeris-1 Decision (`celeris-1-decision`) | Celeris | Celeris API | 2026-11-08 |
| Decider 1 (`decider-1`) | meraGPT | meraGPT API; rejects questions with more than 10 options | 2026-11-08 |
| [Laya](https://huggingface.co/convaiinnovations/laya) and its Arabic fine-tunes | Convai Innovations, Wouze | open weights, locally on Apple MPS | 2026-09-23, 2026-09-25 |
| d1-3B and d1-omni-600M (`LiquidAI/d1-3B`, `LiquidAI/d1-omni-600M`) | Liquid AI | open weights, llama.cpp on a 4-vCPU CPU | 2026-10-17, 2026-10-18 |
| d3 edge, lite and nano (`vllm-sr/d3-{edge,lite,nano}`) | vLLM Semantic Router | open weights, llama.cpp on a 4-vCPU CPU | 2026-10-17, 2026-10-18 |
| Kev 0.8B (`jaredpalmer/kev-0.8b`) | Jared Palmer | open weights, llama.cpp on a 4-vCPU CPU | 2026-10-18 |
| Naluri-279M and Naluri-308M (`jerichosiahaya/Naluri-{279M,308M}-encoder`) | Jericho Siahaya | open weights, PyTorch on a 4-vCPU CPU | 2026-10-17 |
| Dexy-Decision-9B (`Patrick-18/Dexy-Decision-9B`) | Patrick-18 | open weights, the maker's vLLM adapter on a cloud A100 GPU | 2026-11-11 |

Every API model is called at `POST https://openrouter.ai/api/alpha/decisions`, so they all share one gateway.

**Latest results: [systemonebench.dev](https://systemonebench.dev/)**

**What changed and when: [releases](https://github.com/alilibx/system-one-bench/releases)**, one per round, with notes
in [`releases/`](releases/).

**Adding a model or changing the data? Follow the [benchmark rules](CONTRIBUTING.md):** every model runs on the frozen
data (`python data_lock.py` must match), gets identical requests, and is added without disturbing other runs.

System One Bench is a living benchmark: we keep adding models as they're released, and every new model runs the same
cases through the same scorer. The [roadmap](#roadmap) lists what's next. The [plan](docs/plan.md) lists what we're building to make it the
reference for decision models.

## Quick start

```bash
git clone https://github.com/alilibx/system-one-bench && cd system-one-bench
python3 -m venv .venv && .venv/bin/pip install -r requirements-data.txt
.venv/bin/python build_suites.py && .venv/bin/python build_arabic.py    # -> cases.jsonl
.venv/bin/python build_images.py                                        # -> image_cases.jsonl, images/
.venv/bin/python data_lock.py                                           # both files: matches
OPENROUTER_API_KEY=<your key> .venv/bin/python run_decisions.py --model typesafe/jev-1.14 --name my_run
.venv/bin/python score.py --merge preds_my_run.jsonl                    # -> results.json
```

[Full benchmark](#full-benchmark) has every option, the [vision track](#vision-track) the image cases, and the
[benchmark rules](CONTRIBUTING.md) what a run needs before it goes on the board.

## Contents

- [Licence and citation](#licence-and-citation) · [Results site](#results-site) · [Roadmap](#roadmap) · [Live race](#live-race)
- [Frozen data](#frozen-data) · [Full benchmark](#full-benchmark) · [Vision track](#vision-track) ·
  [Open-weight models, run locally](#open-weight-models-run-locally)
- Rounds: [12, Dexy-Decision-9B and in-domain tags](#round-12-dexy-decision-9b-on-a-gpu-and-in-domain-tags-2026-11-11) ·
  [11, Celeris-1 and Decider 1 on their own APIs](#round-11-celeris-1-decision-and-meragpt-decider-1-on-their-own-apis-2026-11-08) ·
  [10, Fastino GLiDE on its own API](#round-10-fastino-glide-on-its-own-api-2026-11-02) ·
  [9, four more from OpenRouter](#round-9-four-more-models-from-openrouter-2026-10-30) ·
  [8, seven more from OpenRouter](#round-8-seven-more-models-from-openrouter-2026-10-25) ·
  [7, open weights on a CPU](#round-7-eight-small-open-weight-models-on-a-cpu-2026-10-18) ·
  [6, vision](#round-6-the-vision-track-2026-10-15) · [5, Jev 1.14](#round-5-jev-114-2026-10-15) ·
  [latency](#latency-every-api-model-from-one-machine-2026-10-15) ·
  [4](#round-4-four-more-models-from-openrouter-2026-10-12) · [3](#round-3-microsoft-decision-1-2026-10-12) ·
  [2](#round-2-eleven-models-2026-10-07) · [Jev vs OpenAI](#jev-vs-openai-decisions-2026-10-07) ·
  [Laya vs Jev](#laya-vs-jev-2026-09-23-apple-m5-24-gb) · [Laya Arabic](#laya-arabic-fine-tunes-vs-jev-2026-09-25) ·
  [Laya takeaways](#laya-takeaways)
- [Contributing, conduct and security](#contributing-conduct-and-security)

## Licence and citation

- **Code:** [Apache-2.0](LICENSE).
- **Results** (`results.json`, `results_vision.json` and the numbers on the site): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Use them anywhere, with a link back to [systemonebench.dev](https://systemonebench.dev/).
- **Cases and images** come from public datasets and keep their sources' licences. The build scripts list every source
  and the exact revision it's pinned to; the [vision track](#vision-track) table gives the image datasets' licences.

To cite System One Bench, use GitHub's "Cite this repository" button, which reads [CITATION.cff](CITATION.cff).

### Badge for model makers

A model that has run here can link to its results with this badge. Replace the model id with the model's own (as in
the table above); the link opens the board filtered to that model.

[![Scored on System One Bench](https://img.shields.io/badge/System_One_Bench-scored-2a78d6)](https://systemonebench.dev/?q=perplexity/pplx-decider-v1.2)

```markdown
[![Scored on System One Bench](https://img.shields.io/badge/System_One_Bench-scored-2a78d6)](https://systemonebench.dev/?q=<model id>)
```

Want a model run? [Request it](https://github.com/alilibx/system-one-bench/issues/new?template=request-a-model.yml).

## Results site

`site/` is a static page that reads `results.json`, `results_vision.json` and `site/meta.json` (display names, makers, run
dates, dataset descriptions, and the vision track's datasets). Its layout follows [Artificial Analysis](https://artificialanalysis.ai/):

- **Two tracks, two indexes.** The **System One Index** (text: mean accuracy across the 16 datasets, equal weight per
  dataset, 0 to 100, with English and Arabic sub-indexes) and the **Vision Index** (the same over the 5 image datasets).
  They rank models separately. The headline and the leader tiles are computed from the data and name the leader of
  each, with its margin, so the page never claims one model leads both unless it does.
- **Search and filters.** The search box (press `/`) and the maker chips filter every chart and table at once, and the
  filter is kept in the URL (`?q=clef`, `?maker=Perplexity`) so a filtered view can be shared.
- **Leaderboard.** One table with both indexes side by side, sortable by any column. Clicking a model shows its run
  details and every dataset score with its rank.
- **A page per model, and per pair.** `.github/scripts/build_pages.py` runs at deploy time and writes
  `/models/<model>/` (every score, with its rank and the best on the board) and `/compare/<a>-vs-<b>/` for every pair of
  ranked models, plus `sitemap.xml`. They're built from the results, so they never need editing by hand.
- **Analytics.** Page views are counted with PostHog in cookieless mode: no cookies or browser storage, IP addresses
  dropped, no autocapture or session recording. The snippet is in `site/index.html` and `.github/scripts/build_pages.py`.
- **Charts.** Index-against-latency and index-against-cost scatters with a Pareto line, calibration, latency and cost
  bar charts, one bar chart per dataset, and the vision track's charts and tables. Latency charts show API models only:
  Laya runs locally, so its timing doesn't compare and is listed in the leaderboard instead.

`.github/workflows/pages.yml` publishes it to GitHub Pages on every push to `main` that touches
`results.json`, `results_vision.json` or `site/`, so re-running `score.py` and merging updates it. Each run needs an entry in `site/meta.json` with its run
date; the newest run date becomes the page's "Updated" date, and runs without an entry are listed as not shown.
The site is served at systemonebench.dev: the domain's DNS (Vercel) points the apex at GitHub Pages' A records and
`www` at `alilibx.github.io`. To preview locally:

```bash
mkdir -p _site && cp site/* results.json results_vision.json _site/ && python3 .github/scripts/build_pages.py _site \
  && python3 -m http.server 8062 -d _site
```

## Roadmap

The roadmap lives in `site/meta.json` and is published at [systemonebench.dev/#roadmap](https://systemonebench.dev/#roadmap).
As of 2026-11-08 it lists 1 hosted model on its own API with the same request shape (Hanzo Kai 1, waiting for a higher
quota), 7 open-weight entries (the rest of the Kev size sweep, the leading community
models, GLiNER2.5-Decide, the larger d3 sizes, GLiClass, and THX-01 and vLLM's Decision-1.0 Eos 0.8B for the next CPU
round), 3 entries that need a track of their own (Span-01's conversations, Cloudflare Clairic's extraction and plain
chat-model baselines), and 4 on a watch list. [Round 9](#round-9-four-more-models-from-openrouter-2026-10-30) ran every
decision model on OpenRouter's Decisions API as of 30 October except Span-01 and Span-01 Lite, which need a conversation
track. That includes Baseten's Mammoth 1 and Elephant 1, which round 8 left out because they were then only on the free
tier. Several vendors publish their own scores; none go on the site until they've run here like every other model.

## Live race

```bash
OPENROUTER_API_KEY=<your key> .venv/bin/python server.py
# or, with the key in Kerstel:
OPENROUTER_API_KEY=kerstel://global/OPENROUTER_API_KEY ks run -- .venv/bin/python server.py
```

Then open http://localhost:8061, pick any set of models with the chips (or **All**), choose a dataset, and press **Start
race**. Every selected model gets its own lane and they all run at the same time on the same cases: everything vs
everything. Each lane shows accuracy, median latency, finish position and the summed `usage.cost` of its calls; the
standings table ranks lanes by accuracy as answers arrive, and the verdict names the fastest, most accurate and
cheapest model. The key stays in the server process and never reaches the browser; keep it in a secrets manager, never
in this repo. "Parallel per model 1" is the fair setting: one request in flight per model.

To add Laya lanes, start the server with `LAYA=1 OMP_NUM_THREADS=1 HF_HUB_OFFLINE=1`. Laya runs on the Apple GPU (MPS);
`OMP_NUM_THREADS=1` avoids a libomp deadlock when several checkpoints load in one process. Without
`OPENROUTER_API_KEY`, only Jev is available, through the TypeSafe API (`TYPESAFE_API_KEY`).

## Frozen data

Every model on the board has to see the same bytes, including models added months from now. So the data is frozen:

- **`data.lock.json`** holds a SHA-256 for every suite: each case's `state`, `questions` and gold labels, and every
  image file it points to. `python data_lock.py` checks the local `cases.jsonl` and `image_cases.jsonl` against it.
- **`run_decisions.py` and `score.py` refuse cases that don't match** and name the suites that differ. Every run
  `score.py` scores now records the hash it ran on as `data_sha256`; the text runs already on the board were scored
  before the check existed and don't carry it. `--unverified` skips the check for experiments that aren't for the board.
- **Every source is pinned.** The build scripts load each Hugging Face dataset at a fixed commit, the fonts come from
  fixed URLs checked by hash, and `requirements-data.txt` pins the libraries. Upstream does move: `lmms-lab` renamed
  itself `lmms-lab-encoder`, and typed-decisions was edited on 14 October (its test split is unchanged).
- **The rendered-text images are committed** (`images/img_sst2`, `images/img_ar_sentiment`, 6.4 MB). Text drawn by a
  different Pillow comes out with different pixels (11.3 and 12.3 differ on all 400), so they can't be rebuilt
  exactly. Photos rebuild byte for byte from the pinned sources, so they aren't committed.
- **`.github/workflows/data.yml`** rebuilds everything from scratch and compares it with the lock on every pull request
  that touches the data code, and every Monday, so a source that changes or disappears is caught before a model runs on it.

The text cases have been the same since the first runs: rebuilt on 15 October, Jev 1.14 billed exactly the 2,157,160
input tokens of Jev 1.13's run on 7 October.

To add a model, build the data, check it, then run and score as below:

```bash
.venv/bin/pip install -r requirements-data.txt
.venv/bin/python build_suites.py && .venv/bin/python build_arabic.py && .venv/bin/python build_images.py
.venv/bin/python data_lock.py                     # cases.jsonl: matches ... image_cases.jsonl: matches
```

Changing a case, a prompt or a dataset makes a new benchmark version: rebuild, run `data_lock.py --write cases.jsonl
image_cases.jsonl`, and rerun every model, since scores on different data don't compare. `build_images.py --rerender`
redraws the committed text images for such a version.

## Full benchmark

```bash
.venv/bin/python build_suites.py                  # -> cases.jsonl (2,050 cases, 3,650 decisions)
.venv/bin/python build_arabic.py                  # appends 1,200 Arabic cases (4,850 decisions in all)
.venv/bin/python data_lock.py                     # checks cases.jsonl against data.lock.json
export OPENROUTER_API_KEY=<your key>
.venv/bin/python run_decisions.py --model openai/gpt-6-luna-decisions --name luna   # -> preds_luna.jsonl
.venv/bin/python run_decisions.py --model typesafe/jev-1.13 --name or_jev           # -> preds_or_jev.jsonl
.venv/bin/python score.py preds_or_jev.jsonl preds_luna.jsonl                       # -> results.json
```

`score.py` rewrites `results.json` from only the files you pass, in that order, and the site lists models in that order.
`--merge` instead keeps the runs already there and adds or replaces just the ones you pass
(`score.py --merge preds_or_jev_114.jsonl`). To rebuild the published file, pass every run:

```bash
.venv/bin/python score.py preds_laya_router.jsonl preds_laya_ara.jsonl preds_laya_ara-rag.jsonl preds_jev.jsonl \
  preds_or_jev.jsonl preds_luna.jsonl preds_pplx.jsonl preds_liquid_d1.jsonl preds_clef.jsonl preds_clef_flash.jsonl \
  preds_solar.jsonl preds_mercury.jsonl preds_kev.jsonl preds_tev1.jsonl preds_msft_d1.jsonl preds_pplx_v11.jsonl \
  preds_clef_omni.jsonl preds_drex.jsonl preds_solar_flash.jsonl preds_or_jev_114.jsonl preds_naluri_279m.jsonl \
  preds_naluri_308m.jsonl preds_d1_omni_600m.jsonl preds_d3_edge.jsonl preds_kev_0_8b.jsonl preds_d3_lite.jsonl \
  preds_d3_nano.jsonl preds_d1_3b.jsonl preds_pplx_v12.jsonl preds_d1_ultra.jsonl preds_pplx_flash_v12.jsonl \
  preds_drex_max.jsonl preds_span02.jsonl preds_drex_v2.jsonl preds_classify1.jsonl preds_d1_1.jsonl \
  preds_mammoth1.jsonl preds_elephant1.jsonl preds_joey1.jsonl
```

Latency on the site comes from a separate re-run of every API model from one machine (see
[latency](#latency-every-api-model-from-one-machine-2026-10-15)). After a full re-score, put it back with
`set_latency.py`, which replaces only `latency_ms`:

```bash
.venv/bin/python set_latency.py lat/preds_*.jsonl   # re-runs written by run_decisions.py run inside lat/
```

Round 9's models (d1.1, Mammoth 1, Elephant 1, Joey 1), GLiDE, Celeris-1 Decision and Decider 1 have no latency on the
board, since they ran from machines whose round trips don't compare (see
[round 9](#round-9-four-more-models-from-openrouter-2026-10-30), [round 10](#round-10-fastino-glide-on-its-own-api-2026-11-02)
and [round 11](#round-11-celeris-1-decision-and-meragpt-decider-1-on-their-own-apis-2026-11-08)). After a full re-score, set their `latency_ms` back to
`null`.

Models on their vendor's own API take the same request body. `--provider fastino|celeris|hanzo|meragpt` sets the
endpoint, model id and auth header, and reads the key from `FASTINO_API_KEY`, `CELERIS_API_KEY`, `HANZO_API_KEY` or
`MERAGPT_API_KEY`. `--url` points the runner at any other endpoint that takes this body, such as a local server
(`--key-env ""` when it needs no key):

```bash
CELERIS_API_KEY=kerstel://global/CELERIS_API_KEY ks run -- .venv/bin/python run_decisions.py --provider celeris --name celeris
.venv/bin/python run_decisions.py --url http://localhost:8000/v1/systemone --key-env "" --model kev-9b --name kev_9b
```

`run_decisions.py` is resumable: re-running it retries only the cases that failed. Laya and direct-TypeSafe runs:

```bash
.venv/bin/python run_laya.py --variant router     # -> preds_laya_router.jsonl
.venv/bin/python run_laya.py --variant ara        # Wouze/laya-ara, Arabic suites only
.venv/bin/python run_laya.py --variant ara-rag    # Wouze/laya-ara-rag, Arabic suites only
TYPESAFE_API_KEY=<your key> .venv/bin/python run_jev.py
```

## Vision track

`build_images.py` builds 1,200 image cases (200 per dataset) into `image_cases.jsonl`, with the images under `images/`.
A case's `state` holds `{"image": "images/<suite>/<n>.jpg"}` (`.png` for the two rendered-text datasets), and `run_decisions.py` sends it as an `image_url` part with a
base64 data URL, the shape OpenRouter's Decisions API reads. Every image is rotated by its EXIF tag and resized to fit
every model's limits: each side 280 to 1,568 px, at least 78,400 pixels, at most about 300 KB.

| Dataset | Question | Source |
|---|---|---|
| SST-2, as an image | yes/no | The 200 SST-2 reviews from `cases.jsonl`, rendered in Noto Sans |
| Arabic sentiment, as an image | 3 options | The 200 Arabic tweets from `cases.jsonl`, rendered in Noto Naskh Arabic |
| Oxford-IIIT Pet | 37 options | `timm/oxford-iiit-pet` test, CC BY-SA 4.0 |
| VQAv2 yes/no | yes/no | `lmms-lab-encoder/VQAv2` validation, first shard, one question per image, CC BY 4.0 |
| CountBench | score, 2 to 10 | `vikhyatk/CountBenchQA` |
| RefCOCO | box | `lmms-lab-encoder/RefCOCO` testA (people) and testB (objects), 100 each, one phrase per image |

The two rendered datasets reuse the exact items of the text datasets, so the gap between them is what reading from
pixels costs. Those 400 images are committed (see [Frozen data](#frozen-data)); `build_images.py` reuses them and only
fetches and resizes the photos. The Box dataset only runs on models that answer Box questions, so pass `--suites` to the
others:

```bash
.venv/bin/python build_images.py                  # needs cases.jsonl; -> image_cases.jsonl, images/
.venv/bin/python data_lock.py                     # both files should match
V=img_sst2,img_ar_sentiment,img_pets,img_vqa_yesno,img_count
.venv/bin/python run_decisions.py --cases image_cases.jsonl --out-dir vision --model typesafe/jev-1.14 --name or_jev_114
.venv/bin/python run_decisions.py --cases image_cases.jsonl --out-dir vision --model openai/gpt-6-luna-decisions --name luna --suites $V
.venv/bin/python score.py --cases image_cases.jsonl --out results_vision.json vision/preds_or_jev_114.jsonl vision/preds_or_jev.jsonl \
  vision/preds_luna.jsonl vision/preds_pplx_v11.jsonl vision/preds_clef.jsonl vision/preds_clef_flash.jsonl \
  vision/preds_clef_omni.jsonl vision/preds_mercury.jsonl vision/preds_d1_ultra.jsonl vision/preds_pplx_v12.jsonl \
  vision/preds_pplx_flash_v12.jsonl vision/preds_span02.jsonl vision/preds_d1_1.jsonl
```

To add one vision run without touching the others, merge it: `score.py --merge --cases image_cases.jsonl --out
results_vision.json vision/preds_<name>.jsonl`.

Box answers are scored by intersection over union with the labelled box: right when IoU is 0.5 or more, plus mean IoU,
and calibration of the answer's `confidence` against being right. They're reported apart and stay out of the Vision
Index, since only Jev 1.14 answers them. Run names match the text runs, so the site shows both under one name.

## Open-weight models, run locally

Most open decision models now run under llama.cpp, whose `llama-server` answers `POST /v1/systemone` with the same
request and response shape as the APIs above, so `run_decisions.py --url` runs them unchanged. Kev and Laya need
llama.cpp 0.6.0; Liquid AI's d1 needs build b11480 or later, and vLLM's d3 needs b11570 or later (12 October 2026), from
the [GitHub releases](https://github.com/ggml-org/llama.cpp/releases) or `brew install --HEAD llama.cpp`.

```bash
llama-server -hf LiquidAI/d1-3B-GGUF:Q8_0 --no-mmproj --port 8080
.venv/bin/python run_decisions.py --url http://localhost:8080/v1/systemone --key-env "" --model d1-3b --name d1_3b --concurrency 1
```

| Model | GGUF (Q8_0) | Size | Notes |
|---|---|---|---|
| Liquid AI d1-3B | `LiquidAI/d1-3B-GGUF` | 2.9 GB | LFM Open License; pass `--no-mmproj` for text only |
| Liquid AI d1-omni-600M | `LiquidAI/d1-omni-600M-GGUF` | 0.4 GB | Add `-b 4096 -ub 4096` so a whole prompt fits in one batch |
| Kev 0.8B, 4B, 9B | `ggml-org/Kev-{0.8B,4B,9B}-GGUF` | 0.8, 4.5, 9.5 GB | English only; Kev 4B is already on the board through OpenRouter |
| vLLM d3 edge, lite, nano, mini, flash | `ggml-org/vllm-d3-{edge,lite,nano,mini,flash}-GGUF` | 0.8 to 9.5 GB | Decision 3.0, released 10 October 2026; `-ub` must hold the whole prompt |

The other open models need their own runners:

- **Hugging Face `system_one`:** d1 and the vLLM Decision-1.0 and 2.0 models load with `trust_remote_code` and answer
  through `model.system_one(state, questions)`, the same shape. The project's `.venv` already has the transformers
  version they need.
- **`kev.serve`:** Kev 0.5B, 0.6B and 8B ship as LoRA adapters, served by [jaredpalmer/kev](https://github.com/jaredpalmer/kev)
  on `/v1/systemone`. It needs Python 3.12 or 3.13.
- **Naluri `serve.py`:** the Naluri encoders (279M, 308M) answer `/v1/systemone` through `serve.py` in
  [jerichosiahaya/naluri](https://github.com/jerichosiahaya/naluri), so `run_decisions.py --url` runs them:
  `python serve.py --model jerichosiahaya/Naluri-308M-encoder --port 8000`, then
  `run_decisions.py --url http://localhost:8000/v1/systemone --key-env "" --model naluri-308m --name naluri_308m --concurrency 1`.
- **Adapters still to write:** GLiNER2.5-Decide and GLiClass answer label questions only, so noul and score map onto
  labels. bekko-system-one takes its own input format, and its weights have no licence yet.

A 24 GB Mac fits everything up to 9B at Q8. The 27B models (Kev 27B, d3 27B, Open-Jev 27B) and Open-Jev 9B, whose base
model alone is 19 GB, need a bigger machine. Laya Multilingual is already covered: Laya Router sends every non-English
state, Arabic and French included, to those same weights.

## Round 12: Dexy-Decision-9B on a GPU, and in-domain tags (2026-11-11)

Dexy-Decision-9B, an independent fine-tune of Qwen3.5-9B, was [requested by its developer](https://github.com/alilibx/system-one-bench/issues/29).
It ran on 11 November on all 3,250 text cases from a rented cloud GPU (one NVIDIA A100 80 GB on RunPod), at revision
`afee4ba`, through the maker's own vLLM adapter (`deployment/vllm/start.sh`, vLLM 0.32.0, default settings), which
answers `POST /v1/systemone`. `run_decisions.py --url` sent it the same bodies as every other model, 8 calls in flight.
Every call succeeded.

| Model | Maker | Weights (revision) | Index | Without in-domain datasets | English | Arabic | Calibration error | Median latency, GPU |
|---|---|---|---|---|---|---|---|---|
| Dexy-Decision-9B | Patrick-18 | `Patrick-18/Dexy-Decision-9B` (`afee4ba`), 17.9 GB, BF16 | 84.7 (1st) | 83.4 (7th of 38, 12 datasets) | 82.3 (6th) | 86.8 (2nd) | 3.5% | 62 ms |

Ranks are out of the 38 models on the System One Index.

- **It has the top index, 84.7, but it isn't clearly the best model.** It leads Decider V1.2 by 0.07 points (84.71
  against 84.63), and 4 of its 16 datasets are in-domain. Its developer reported fine-tuning on the train splits of
  typed-decisions and Banking77, and on MASSIVE's English and Chinese train splits, so the Arabic MASSIVE datasets share
  its training labels in another language. It's 1st on typed-decisions (80.0%) and tied 1st on both Arabic MASSIVE
  datasets (89.5% scenario, 91.5% intent).
- **On the other 12 datasets it averages 83.4, 7th**, against Decider V1.2 and Drex Max at 85.1. Without only
  typed-decisions and Banking77 it averages 84.5, 2nd.
- **It didn't see our test cases.** None of our 200 Banking77 or 400 typed-decisions cases appear in those train
  splits. But 100 of the 400 typed-decisions cases share their task text with a train example (with different details
  around it), so training on that split helps on its test split.
- **It matches the developer's own run.** They reported 84.82 on the same 3,250 cases from an A800 GPU; this run
  measured 84.71. Only this run's numbers are on the board.
- **Its weakest dataset is DAIR Emotion** (54.0%, 35th). It's 15th on calibration (3.5%).
- **Latency isn't comparable** with the API models: it's a local GPU with no network. The board's figure is the
  one-call-at-a-time probe (90 single-question calls, 62 ms median, 172 ms at the 95th percentile), not the run with 8 in
  flight, and like the other open-weight models it stays out of the latency charts.
- **No vision score.** It reads text only, so it's listed under `vision.no_image`.

**In-domain tags.** A model whose maker says it trained on another split of a dataset we test is now marked
**in-domain** on the leaderboard, and its row and page list those datasets with its index without them, ranked
against every model on the same datasets. Its System One Index still counts all 16, like every other model's. The
tags come from what each maker published (`in_domain` in `site/meta.json`):

| Model | In-domain datasets | Source |
|---|---|---|
| Dexy-Decision-9B | typed-decisions, Banking77, Arabic MASSIVE scenario and intent | the developer, in #29 |
| Kev 4B, Kev 0.8B | AG News, SST-5, Banking77, BoolQ | the model cards' training datasets |
| Naluri-308M, Naluri-279M | XNLI English, French and Arabic, Arabic MASSIVE scenario and intent, DAIR Emotion | the model cards |
| laya-ara | XNLI Arabic, Arabic MASSIVE scenario and intent, OSACT4 offensive | [Laya Arabic fine-tunes](#laya-arabic-fine-tunes-vs-jev-2026-09-25) |
| laya-ara-rag | Arabic MIRACL reranking and pairs, Arabic MASSIVE scenario and intent | [Laya Arabic fine-tunes](#laya-arabic-fine-tunes-vs-jev-2026-09-25) |

Models that don't publish their training data may overlap too; we can't tell, so they carry no tag.

## Round 11: Celeris-1 Decision and meraGPT Decider 1 on their own APIs (2026-11-08)

Neither model is on OpenRouter, so both ran on their vendor's own System One endpoint (`run_decisions.py --provider
celeris` and `--provider meragpt`) with the same request bodies as every other model, on the 3,250 text cases, 8 calls in
flight. Celeris-1 answered every case. Decider 1 rejected 600 (see below), which count as wrong.

| Model | Maker | Index | English | Arabic | Calibration error | Failed | Cost per 1,000 calls |
|---|---|---|---|---|---|---|---|
| **Celeris-1 Decision** | Celeris | **83.6** (4th) | 83.2 (2nd) | 83.1 (9th) | 2.6% | 0 | $0.014 |
| Decider 1 | meraGPT | 61.9 (33rd) | 67.4 (30th) | 54.7 (35th) | 7.9% | 600 | $0.012 |

Ranks are out of the 37 models on the System One Index.

- **Celeris-1 is 4th**, 1.0 point behind Decider V1.2 (84.6) and 0.5 behind GLiDE and Drex Max (84.1), and 2nd on the
  English index. It's 2nd on typed decisions (76.4%) and XNLI French (90.0%); its weakest ranks are 17th, on BoolQ
  (89.5%) and Arabic MIRACL reranking (86.5%).
- It's 9th on calibration (2.6%). Celeris's API reports tokens but no cost, so the cost is input tokens at the $0.04 per
  1M list price (`cost_from_list_price`).
- **Decider 1 rejects any question with more than 10 options** (400: "a choice can offer at most 10 labels"), so all 200
  cases each of Banking77 (77 options), Arabic MASSIVE scenario (18) and Arabic MASSIVE intent (20) count as wrong. On
  the other 13 datasets it averages 75.5, which would rank 26th. Its 4,096-token cap didn't reject any text case.
- meraGPT's API reports cost as a string (`"$0.000007"`), rounded to the millionth of a dollar per call;
  `run_decisions.py` now reads it as a number. The API accepts both `state-decider-1` and `decider-1` and reports
  `decider-1`.

**Vision.** Neither model has a vision score. Celeris-1 accepts images but scored at chance on all 5 Vision Index
datasets: 50.0% on SST-2 from an image (against 95.5% on the same reviews as text), 1.5% on the 37 pet breeds and 11.0%
on CountBench. Its usage counted about 34,000 input tokens per image, the length of the base64 text, so it reads the
image as text. Decider 1 rejects every image: one counts as about 10,000 tokens, over its 4,096-token cap. Both are listed
under `vision.no_image` in `site/meta.json`, and neither answers Box questions.

**Hanzo Kai 1 waits.** It started this round on Hanzo's own API, but our key allows 60,000 tokens per 8 hours
(`x-ratelimit-limit: 60000`, then 429 "Usage limit reached for this 8h"), and a full run needs about 765,000, so after
102 cases it stopped. It stays on the roadmap until the quota is raised; `run_decisions.py` resumes where it stopped. It
also counts images as text (a 422 for "208,982 tokens" on one photo), so it would have no vision score either.

**Latency isn't on the board for either model.** This round ran from a different machine from the board's timings, and
not through OpenRouter. `latency_ms` is `null`, and each model's `latency` field in `site/meta.json` says why. Decider 1
took about 10 seconds a call there, against about half a second for Celeris-1.

## Round 10: Fastino GLiDE on its own API (2026-11-02)

GLiDE isn't on OpenRouter, so it ran on Fastino's own API (`run_decisions.py --provider fastino`) with the same request
bodies as every other model, on the 3,250 text cases, 8 calls in flight. Every case got an answer. A second full run, not
published, scored the same index (84.13): 3,110 cases came back identical and 7 answers changed.

| Model | Maker | Index | English | Arabic | Calibration error | Cost per 1,000 calls |
|---|---|---|---|---|---|---|
| **GLiDE** | Fastino | **84.1** (2nd) | 83.0 (2nd) | 84.8 (2nd) | 3.6% | $0.017 |

Ranks are out of the 35 models on the System One Index.

- **GLiDE is 2nd**, 0.5 points behind Decider V1.2 (84.6) and 0.04 ahead of Drex Max, so both show as 84.1.
- It's 2nd on XNLI English (94.7%, behind Drex Max's 95.3%), but it doesn't lead any dataset. Its weakest rank is 15th,
  on Arabic MIRACL reranking (87.0%).
- It's 14th on calibration (3.6%, against Decider V1.2's 0.7%).
- Fastino's API reports tokens but no cost, so the cost is input tokens at the $0.04 per 1M list price
  (`cost_from_list_price`).
- The API reports the model as `glide_v2`. Fastino's open weights are V1.2, and we can't tell from the API which version
  it serves, so the board calls it GLiDE.

**Vision.** GLiDE reads images but rejects Box questions (422: only `noul`, `choice` and `score`), so it ran the 5 Vision
Index datasets. Every case got an answer.

| Model | Vision Index | SST-2 image | Arabic sentiment image | Pets (37) | VQAv2 yes/no | CountBench | Calibration error | Cost per 1,000 calls |
|---|---|---|---|---|---|---|---|---|
| GLiDE | 82.5 (7th) | 94.0 | 51.5 | 84.5 | 89.0 | 93.5 | 3.0% | $0.016 |

- It's the third best calibrated on images (3.0%), and 3rd on VQAv2 yes/no.
- It loses 22.0 points reading Arabic from a picture (51.5% on the images against 73.5% on the same tweets as text). Only
  Decider Flash V1.2, Mercury and Clef have lost more.
- Ranks are out of the 13 models on the Vision Index.

**Latency isn't on the board for GLiDE.** This round ran from the same machine as round 9, and it doesn't go through
OpenRouter like the board's timings. As a control, Jev 1.14 ran on 200 AG News cases through OpenRouter (not published):
521 ms median with 8 calls in flight, against 136 ms on the board. `latency_ms` is `null`, and the model's `latency`
field in `site/meta.json` says why.

## Round 9: four more models from OpenRouter (2026-10-30)

On 30 October, OpenRouter's catalog (`GET /api/v1/models?output_modalities=decisions`) listed four decision models that
weren't on the board: Liquid AI d1.1, the successor to d1, and Baseten's Mammoth 1, Elephant 1 and Joey 1, from Base Labs,
Baseten's research team. Round 8 left Mammoth 1 and Elephant 1 out because they were only on the free tier; both now
have paid endpoints. All four ran on the 3,250 text cases through the Decisions API, 8 calls in flight. Before each run,
one case of every question type checked that the model answers our request shape. Every case got an answer: Joey 1's
run hit rate limits, and the 3 cases that gave up on 429 succeeded when the run was resumed.

| Model | Maker | Index | English | Arabic | Calibration error | Cost per 1,000 calls |
|---|---|---|---|---|---|---|
| **Mammoth 1** | Baseten | **82.9** (4th) | **82.5** | 82.8 | 4.9% | $0.037 |
| d1.1 | Liquid AI | 82.3 (7th) | 81.2 | **83.3** | **2.1%** | $0.005 |
| Elephant 1 | Baseten | 82.1 (8th) | 81.3 | 82.0 | 3.7% | $0.013 |
| Joey 1 | Baseten | 73.3 (24th) | 72.9 | 73.5 | **2.1%** | **$0.004** |

Ranks are out of the 34 models on the System One Index.

- **Mammoth 1 is 4th**, 0.04 points behind d1-ultra, so both show as 82.9. It's built on Qwen3.5-27B, and it's 2nd on
  the typed decisions (76.4%, behind Microsoft-Decision-1's 79.0%). It's also the dearest of the four.
- **Elephant 1 is 0.8 points behind Mammoth 1 at about a third of the price.** It's built on Qwen3.5-9B, like
  Microsoft-Decision-1 (82.0), and is tied 2nd on XNLI English (94.0%) and XNLI French (90.0%), behind Drex Max.
- **d1.1 is 0.4 points behind d1 (82.7)**, the model it replaces. It gains on Arabic sentiment (+5.0) and SST-5 (+3.5)
  and loses on Arabic offensive language and DAIR Emotion (3.0 each). It's the most accurate model on SST-2 (98.0%)
  and better calibrated than d1 (2.1% against 2.9%). Its $0.005 per 1,000 calls is a third of d1's $0.015, but that
  gap comes from when d1 ran: it was billed about $0.04 per 1M input tokens on 7 October, and both now list $0.02.
- **Joey 1 is the cheapest paid model on the board** ($0.004 per 1,000 calls). It's built on Qwen3.5-2B and scores 73.3,
  above Tev1 4B (71.5) and below Kev 4B (76.8). It scores 93.0% on Banking77 but falls on SST-5 (40.5%) and Arabic
  MIRACL reranking (62.0%).

**Vision.** d1.1 reads images but doesn't answer Box questions, so it ran the 5 Vision Index datasets. Baseten's three
reject images ("BaseTen does not accept \"image_url\" parts in state") and are listed under `vision.no_image`.

| Model | Vision Index | SST-2 image | Arabic sentiment image | Pets (37) | VQAv2 yes/no | CountBench | Calibration error | Cost per 1,000 calls |
|---|---|---|---|---|---|---|---|---|
| d1.1 | 85.8 (2nd) | 96.5 | 61.0 | 90.5 | 89.5 | 91.5 | 3.3% | $0.009 |

- d1.1 is 2nd on the Vision Index, 0.3 points behind Span-02 (86.1) and 0.2 above d1-ultra. d1, which it replaces,
  has no image input. It ties d1-ultra on VQAv2 yes/no (89.5%) and is the third best calibrated on images (3.3%).
- It loses 11.5 points reading Arabic from a picture (61.0% on the images against 72.5% on the same tweets as text).
  Only Span-02 loses less (6.0); every other model has lost 12.5 or more.
- Ranks are out of the 12 models on the Vision Index.

**Latency isn't on the board for these four.** This round ran from a machine where round trips through OpenRouter take
far longer than from the cloud server behind the board's timings. As a control, Jev 1.14 ran again alongside the four
(not published): 492 ms median with 8 calls in flight, against 136 ms on the board. Accuracy, calibration and cost don't
depend on the network, so only latency is left out (`latency_ms` is `null`), and the four don't appear in the latency
charts. Each model's `latency` field in `site/meta.json` says so.

## Round 8: seven more models from OpenRouter (2026-10-25)

On 25 October, OpenRouter's catalog (`GET /api/v1/models?output_modalities=all`) listed nine decision models that
weren't on the board. Seven ran on all 3,250 text cases through the Decisions API, 8 calls in flight, from a cloud
server: Perplexity Decider V1.2 and Decider Flash V1.2, Nace AI Drex Max and Drex v2.0, Liquid AI d1-ultra, Respan
Span-02 and ScaleDown Classify-1. The four that read images also ran the vision track. Before each run, one case of every
question type checked that the model answers our request shape. Every call succeeded except Classify-1's, below.

| Model | Maker | Index | English | Arabic | Calibration error | Median latency | Cost per 1,000 calls |
|---|---|---|---|---|---|---|---|
| **Decider V1.2** | Perplexity | **84.6** (1st) | 82.0 | **86.9** | **0.7%** | 178 ms | $0.007 |
| Drex Max | Nace AI | 84.1 (2nd) | **82.8** | 84.5 | 6.2% | 277 ms | $0.021 |
| d1-ultra | Liquid AI | 82.9 (3rd) | 81.7 | 84.2 | 1.0% | 168 ms | $0.010 |
| Decider Flash V1.2 | Perplexity | 81.9 (7th) | 80.0 | 83.3 | 1.8% | **104 ms** | **$0.005** |
| Span-02 | Respan | 79.5 (11th) | 77.9 | 82.3 | 10.5% | 204 ms | **$0.005** |
| Drex v2.0 | Nace AI | 78.6 (14th) | 77.8 | 79.6 | 1.5% | 294 ms | $0.015 |
| Classify-1 | ScaleDown | 30.6 (30th) | 30.7 | 30.6 | 3.2% | 254 ms | $0.018 |

Ranks are out of the 30 models on the System One Index, with Decider V1.1 retired (below).

- **Decider V1.2 leads the System One Index**, 1.2 points above Decider V1.1 (83.4). Most of the gain is Banking77
  (+7.0) and Arabic MASSIVE scenario (+6.5). It's the most accurate model on XNLI Arabic (90.0%) and the best
  calibrated on the board: 0.7% over all decisions (pooling every dataset evens out over- and under-confidence, so
  every model's figure is lower than its per-dataset ones; Decider V1.2's are 1.5% to 8.5%). It's also the cheapest
  paid model at its accuracy.
- **Drex Max is 2nd, 0.5 points behind**, and most accurate on BoolQ (93.0%), XNLI English (95.3%) and XNLI French
  (91.3%). It's 6.5 points above Drex v1.5; Drex v2.0 adds only 1.0 of those. It's the dearest of the new models: Nace
  bills about 1.2 M output tokens per run, though the price on OpenRouter counts input tokens only.
- **d1-ultra is 3rd**, 0.2 points above Liquid AI's d1, and well calibrated (1.0%).
- **Decider Flash V1.2 is the fastest API model on the board** (104 ms median) and, with Span-02, the cheapest
  ($0.005 per 1,000 calls), 2.7 points behind Decider V1.2.
- **Span-02 fits the normal text track**, unlike Span-01, which only takes a conversation. Its first 441 answers were
  checked by hand before the full run counted. It's the most accurate model on Arabic offensive language (97.0%) and
  ties Decider V1.2 on MIRACL pairwise (91.5%), but it's overconfident (10.5%) and slow on long states: 2.1 s median on
  the 5-question typed-decisions cases against 190 ms on the rest.
- **Classify-1 rejects most of our cases.** It only accepts a state that is a string or an object with `text` and
  `document` fields, and returns 400 for any other. Only DAIR Emotion's state (`{"text": ...}`) fits, so it answered
  those 200 cases (59.0%, in line with the other models) and failed the other 3,050, which count as wrong. Its latency
  and cost come from those 200 calls.

**Vision.** Decider V1.2, Decider Flash V1.2, d1-ultra and Span-02 read images; none answers Box questions, so they ran
the 5 Vision Index datasets. Drex Max, Drex v2.0 and Classify-1 reject images (Classify-1: "does not accept image_url
parts") and are listed under `vision.no_image`.

| Model | Vision Index | SST-2 image | Arabic sentiment image | Pets (37) | VQAv2 yes/no | CountBench | Calibration error | Median latency | Cost per 1,000 calls |
|---|---|---|---|---|---|---|---|---|---|
| **Span-02** | **86.1** (1st) | 92.5 | **70.0** | **92.5** | 87.0 | 88.5 | 4.4% | 231 ms | $0.004 |
| d1-ultra | 85.6 (2nd) | **97.0** | 62.5 | 87.5 | **89.5** | 91.5 | 3.9% | 183 ms | $0.019 |
| Decider V1.2 | 83.8 (5th) | 94.5 | 57.0 | 85.5 | 86.5 | **95.5** | 4.2% | 226 ms | $0.009 |
| Decider Flash V1.2 | 77.5 (10th) | 93.5 | 35.0 | 84.0 | 87.5 | 87.5 | 6.0% | **134 ms** | **$0.004** |

- **Span-02 leads the Vision Index**, 1.0 point above Jev 1.14 (85.1), with d1-ultra between them. It reads Arabic from
  a picture better than any model so far, losing 6.0 points against its text score on the same 200 tweets; every other
  model has lost 12.5 or more.
- d1-ultra scores higher on the SST-2 images (97.0%) than on the same reviews as text (95.5%). Decider V1.2 is the best
  counter (95.5% on CountBench). Decider Flash V1.2 falls to 35.0% on the Arabic images, near the 3-way floor.
- Ranks are out of the 11 models on the Vision Index.

**Decider V1.1 is retired.** It has left OpenRouter's catalog, and its slug returns 404 ("No endpoints found"), so
it's tagged retired and left out of the charts and rankings like Decider V1. Decider V1.2 replaces it in the live race,
and every new model except Classify-1 joins it.

**Baseten's Mammoth 1 and Elephant 1 are left out of this round.** They're served only on OpenRouter's free tier, which
allows 1,000 requests a day, and a text run takes 3,341 (3,250 cases and the 91-call latency probe), so a run would
take days and free access may end first. Both answered our request shape correctly; a partial Mammoth 1 run was stopped
and isn't published. Their open weights (`baselabs/mammoth-1`, `baselabs/elephant-1`, MIT) are on the roadmap.

**Latency.** These runs were timed from a different cloud server than the one behind the board's 15 October timings,
with several models running at once. As a control, Jev 1.14 ran again alongside them (not published): 122 ms median
here against 136 ms on the board, so the new models' latencies compare with the others to within about 10%. Tails were
wider with several runs at once (Jev 1.14's 95th percentile was 215 ms against 175 ms).

## Round 7: eight small open-weight models on a CPU (2026-10-18)

Eight open-weight models from the roadmap, run on 17 and 18 October on all 3,250 cases from a 4-vCPU Linux cloud
server with no GPU, one call at a time. The GGUF models ran under `llama-server` from llama.cpp b11716, built from
source, at Q8_0 with `-b 8192 -ub 8192 -c 8192 -t 4` and no mmproj, so text only. d1-3B's server died with those
settings 80 seconds into its first attempt, most likely out of memory, so it ran again from scratch with
`-b 4096 -ub 4096 -c 4096 -np 1`, which still holds the longest prompt (2,973 tokens) in one batch. The Naluri
encoders ran under `serve.py` from [jerichosiahaya/naluri](https://github.com/jerichosiahaya/naluri) (commit
`473a789`) on PyTorch's CPU build. Both answer `POST /v1/systemone`, so `run_decisions.py --url` sent every model the
same bodies as the API models. Every call in the published runs succeeded.

| Model | Maker | Weights (revision) | Index | English | Arabic | Calibration error | Median latency, CPU |
|---|---|---|---|---|---|---|---|
| **d1-3B** | Liquid AI | `LiquidAI/d1-3B-GGUF` (`bb1e436`), 2.9 GB | **78.4** (10th) | **78.4** | **78.3** | **2.4%** | 1,134 ms |
| d3 nano | vLLM Semantic Router | `ggml-org/vllm-d3-nano-GGUF` (`67baf94`), 2.6 GB | 78.0 (11th) | 77.9 | 76.9 | 7.0% | 1,167 ms |
| d3 lite | vLLM Semantic Router | `ggml-org/vllm-d3-lite-GGUF` (`a1f9fa1`), 1.1 GB | 74.9 (15th) | 74.3 | 74.7 | 7.1% | 620 ms |
| d3 edge | vLLM Semantic Router | `ggml-org/vllm-d3-edge-GGUF` (`753af7a`), 0.8 GB | 65.9 (18th) | 69.1 | 62.2 | 18.7% | 294 ms |
| d1-omni-600M | Liquid AI | `LiquidAI/d1-omni-600M-GGUF` (`8eb2d2a`), 0.4 GB | 65.2 (19th) | 75.5 | 53.4 | 9.8% | 251 ms |
| Kev 0.8B | Jared Palmer | `ggml-org/Kev-0.8B-GGUF` (`e551e31`), 0.8 GB | 63.6 (21st) | 71.0 | 54.9 | 4.3% | 705 ms |
| Naluri-308M | Jericho Siahaya | `jerichosiahaya/Naluri-308M-encoder` (`2346b40`) | 61.0 (22nd) | 59.3 | 61.9 | 5.7% | 189 ms |
| Naluri-279M | Jericho Siahaya | `jerichosiahaya/Naluri-279M-encoder` (`765d51e`) | 50.4 (24th) | 52.6 | 50.7 | 8.3% | **138 ms** |

Ranks are out of the 24 models on the System One Index.

- **d1-3B is the first open-weight model in the top 10, with d3 nano right behind it.** Both place above Drex v1.5,
  Kev 4B and GPT-6 Luna Decisions, 0.6 and 1.0 points below Jev 1.13, and both are under 3 GB at Q8_0.
- **d1-3B is the second best calibrated model on the board** (2.4%, behind Clef's 2.2%), and keeps English and Arabic
  level. It is 4.3 points below the full d1 on the index: 2.9 in English and 5.6 in Arabic. Its best dataset is
  SST-2 (95.5%); emotion (63.5%) and SST-5 (56.0%) are its weakest.
- **d3 nano** scores 93.0% on Banking77 and 86.0% on XNLI French; emotion (59.5%) and SST-5 (55.5%) are its weakest
  datasets. Each d3 size up adds points: edge to lite +9.0, lite to nano +3.1.
- **The smallest models hold up in English and fall off in Arabic.** d1-omni-600M scores 75.5 in English, within 6
  points of the full d1, and 53.4 in Arabic, 30 points below it. Kev 0.8B (English-only, like Kev 4B) loses 16 points
  between its English and Arabic sub-indexes. d1-3B, d3 nano and d3 lite keep the two within 1 point.
- **Naluri scores match their model cards exactly** (61.0 and 50.4), which reported results on this benchmark before
  it ran here. Both are trained on the train splits of XNLI, MASSIVE and DAIR Emotion, three of the datasets tested
  here (we use their test splits). Even so, Naluri-279M answers "entailment" to 145 of 150 XNLI English cases and scores
  near chance on all three XNLI sets.
- **Latency isn't comparable** with the API models: these are local CPU timings, one call at a time, with no network,
  so they stay out of the latency charts like Laya's. d1-omni-600M's run was stopped after 2,615 cases to reorder the
  queue and resumed on the same machine.
- **No vision scores.** Kev 0.8B and the Naluri encoders don't read images, so they're listed under `vision.no_image`.
  d1 and d3 can with their mmproj files, but these runs left them out; they show as not run on images.

## Round 6: the vision track (2026-10-15)

Jev 1.14 (round 5) can read images and answer Box questions, which return a bounding box; TypeSafe marks both as early
features that aren't production-ready. This round starts a [vision track](#vision-track) for every model on OpenRouter's
Decisions API that accepts images: 6 image datasets, 1,200 cases. Every model ran from a cloud server on 15 October,
8 calls in flight, so the vision latencies compare with each other.

**Vision.** 8 models accept images; d1, Microsoft-Decision-1, Kev 4B, Tev1, Solar Decide, Solar Decide Flash and Drex
return 400 ("does not accept image_url parts"). The Vision Index is the mean accuracy over 5 image datasets, kept apart
from the System One Index.

| Model | Vision Index | SST-2 image | Arabic sentiment image | Pets (37) | VQAv2 yes/no | CountBench | Calibration error | Median latency | Cost per 1,000 calls |
|---|---|---|---|---|---|---|---|---|---|
| **Jev 1.14** | **85.1** | 93.5 | 63.5 | **88.5** | 86.5 | 93.5 | 2.9% | **183 ms** | $0.046 |
| Jev 1.13 | 83.9 | 94.5 | 59.0 | 83.5 | 88.0 | **94.5** | **2.8%** | 192 ms | $0.046 |
| Decider V1.1 27B | 83.0 | **96.0** | 51.0 | 84.0 | **89.5** | **94.5** | 5.6% | 302 ms | $0.009 |
| GPT-6 Luna Decisions | 81.6 | 88.5 | **67.0** | 87.0 | 80.5 | 85.0 | 5.3% | 221 ms | $0.047 |
| Mercury Decide | 79.4 | 93.0 | 39.0 | 84.5 | 87.0 | 93.5 | 9.9% | 305 ms | free tier |
| Clef | 78.1 | 95.5 | 35.0 | 82.5 | 87.5 | 90.0 | 3.6% | 502 ms | $0.138 |
| Clef Flash | 78.0 | 95.5 | 33.5 | 85.0 | 88.0 | 88.0 | 9.4% | 429 ms | $0.022 |
| Clef Omni | 72.2 | 89.5 | 28.5 | 88.0 | 87.0 | 68.0 | 20.6% | 274 ms | $0.086 |

- Jev 1.14 leads the Vision Index by 1.2 points over Jev 1.13, mostly on pet breeds (+5.0) and the Arabic tweets
  (+4.5). Both Jevs are the best calibrated on images.
- The two indexes rank models differently. Decider V1.1 27B, which leads the System One Index on text, is 3rd on
  images (83.0), 2.1 points behind Jev 1.14; Jev 1.14 is 8th on text. Neither model leads both.
- Reading English from a picture costs little: every model is within 7.5 points of its text SST-2 score, and Decider,
  Jev 1.13 and Clef Flash lose nothing. Reading Arabic from a picture costs a lot: 12.5 to 23.5 points on the same 200
  tweets. GPT-6 Luna Decisions is best at it (67.0); the Clef models fall to near the 3-way floor.
- Jev bills about 1,100 input tokens per image call, twice what the others count, but its price per token is lower, so
  it costs the same as Luna. Decider V1.1 is again the cheapest paid model.
- GPT-6 Luna Decisions returned a 502 on the same 2 cases on every retry (`img_sst2-187`, `img_vqa_yesno-105`); they
  count as wrong.

**Box questions** (Jev 1.14 only; Jev 1.13 and the others reject them). On 200 RefCOCO phrases, 100 about people
(testA) and 100 about objects (testB):

| | Right (IoU ≥ 0.5) | Mean IoU | Mean confidence | Calibration error | Confidence AUROC |
|---|---|---|---|---|---|
| People (testA) | 83.0% | 0.74 | 52.9% | 30.7% | 0.82 |
| Objects (testB) | 74.0% | 0.67 | 43.4% | 30.6% | 0.77 |
| **All** | **78.5%** | **0.70** | 48.2% | 30.3% | 0.80 |

- Box answers are good but underconfident: right 78.5% of the time at an average stated confidence of 48%. The
  confidence still ranks answers well (AUROC 0.80), so it works as a threshold, not as a probability.
- A Box call takes 194 ms median, about the same as Jev's other image calls (182 ms).
- Jev's image docs give 256 px as the shortest side it accepts, but it answered "Invalid image dimensions" for every
  image with a side under 280 px. `build_images.py` keeps every side at 280 px or more.
## Round 5: Jev 1.14 (2026-10-15)

TypeSafe released Jev 1.14 on 2026-10-14 as a preview; Jev 1.13 is still its stable release. It adds image input, a
bounding-box question type and a 262K context window, none of which these text datasets use. It ran all 3,250 cases
through OpenRouter's Decisions API with 8 calls in flight, served as `typesafe/jev-1.14-20261014`. Every call
succeeded. To check the rebuilt cases, Jev 1.13 ran again from the same machine the same day; that control run isn't
published.

| Model | Index | English | Arabic | Calibration error | Median latency | Cost per 1,000 calls |
|---|---|---|---|---|---|---|
| **Jev 1.14** | **79.3** | **78.8** | **80.3** | 6.0% | **136 ms** | $0.028 |
| Jev 1.13, published (2026-10-07) | 79.0 | 78.5 | 79.9 | 6.1% | 150 ms | $0.028 |
| Jev 1.13, control (2026-10-15) | 79.0 | 78.7 | 79.5 | 5.9% | | $0.028 |

- Jev 1.14 places 8th of 16 on the System One Index, 0.3 points above Jev 1.13. That's within run-to-run noise: the
  control run of Jev 1.13 moved individual datasets by up to 1.5 points against the published one.
- The one clear gain is customer-service decisions in typed-decisions: 83.6% against 77.4% and 78.2% for the two Jev
  1.13 runs. Its biggest drop is Arabic offensive language (87.0% against 90.0%).
- Same price, and the same billed tokens: both cost $0.091 for all 3,250 cases.
- Jev 1.14 is the fastest API model on the board, but only just: 136 ms median against 150 ms for Jev 1.13, timed from
  the same machine on the same day (see [latency](#latency-every-api-model-from-one-machine-2026-10-15)). In the control
  run earlier that day the two were 141 ms and 143 ms.

## Latency: every API model from one machine (2026-10-15)

Jev 1.14 ran from a cloud server much closer to OpenRouter than the machine behind every earlier run: Jev 1.13 measured
143 ms there against 372 ms published. So every charted API model ran all 3,250 cases again from that server, with 8
calls in flight for all of them (earlier rounds used 6 for some models and 24 to finish Solar Decide). Models from the
same maker ran at different times so they didn't share capacity. Only latency comes from these runs; accuracy,
calibration and cost stay from each model's original run. The latency columns in the round tables below are as measured
at the time. The retired Decider V1 and the TypeSafe API run of Jev keep their original latency and stay off the charts.

| Model | Maker | Median | 95th percentile | Median before |
|---|---|---|---|---|
| **Jev 1.14** | TypeSafe | **136 ms** | **175 ms** | – |
| Jev 1.13 | TypeSafe | 150 ms | 216 ms | 372 ms |
| d1 | Liquid AI | 188 ms | 297 ms | 659 ms |
| Drex v1.5 | Nace AI | 198 ms | 529 ms | 608 ms |
| Clef Omni | Cloudflare | 208 ms | 290 ms | 544 ms |
| GPT-6 Luna Decisions | OpenAI | 215 ms | 582 ms | 363 ms |
| Tev1 4B Experimental | Together AI | 232 ms | 292 ms | 518 ms |
| Microsoft-Decision-1 | Microsoft | 240 ms | 321 ms | 679 ms |
| Decider V1.1 27B | Perplexity | 263 ms | 605 ms | 678 ms |
| Clef Flash | Cloudflare | 267 ms | 437 ms | 534 ms |
| Mercury Decide | Inception | 276 ms | 820 ms | 490 ms |
| Clef | Cloudflare | 310 ms | 436 ms | 706 ms |
| Kev 4B | Jared Palmer | 552 ms | 3,597 ms | 899 ms |
| Solar Decide Flash | Upstage | 586 ms | 983 ms | 908 ms |
| Solar Decide | Upstage | 715 ms | 17,262 ms | 1,231 ms |

- Every model got faster, but not by the same amount, so the order changed. Jev 1.13 and GPT-6 Luna Decisions looked
  much faster than the rest before; Liquid AI d1, Drex v1.5 and Clef Omni now sit close behind Jev, ahead of Luna.
- The two Jevs are still the fastest and have the tightest tails. Kev 4B and Solar Decide still have long tails (3.6 s
  and 17 s at the 95th percentile).
- GPT-6 Luna Decisions returned 13 gateway timeouts (504) out of 3,250 calls, which are left out of its latency. Solar
  Decide, Solar Decide Flash and Tev1 again rejected all 200 Banking77 cases (too many options); every other call
  succeeded.

## Round 4: four more models from OpenRouter (2026-10-12)

Four decision models that appeared on OpenRouter's Decisions API since round 2, run on all 3,250 cases with 8 calls in
flight: Perplexity Decider V1.1 27B, Cloudflare Clef Omni, Nace AI Drex v1.5 and Upstage Solar Decide Flash. Perplexity
retired Decider V1 27B (its slug now returns 404), so V1.1 replaces it on the charts and in the live race; the V1 run is
kept for reference.

| Model | Maker | Index | English | Arabic | Calibration error | Median latency | Cost per 1,000 calls |
|---|---|---|---|---|---|---|---|
| **Decider V1.1 27B** | Perplexity | **83.4** | 81.1 | **85.0** | 5.7% | 678 ms | **$0.009** |
| Clef Omni | Cloudflare | 79.7 | 78.6 | 80.5 | 3.4% | 544 ms | $0.074 |
| Drex v1.5 | Nace AI | 77.6 | 77.6 | 77.0 | 10.8% | 608 ms | $0.010 |
| Solar Decide Flash | Upstage | 63.6 | 61.3 | 66.5 | 14.4% | 908 ms | $0.042 |

- Decider V1.1 matches V1 on accuracy (83.4 against 83.3) and still leads the System One Index, at half V1's price per token. It's
  now also the cheapest paid model. It's slower: 785 ms one call at a time, against 352 ms for V1.
- Clef Omni, Cloudflare's model that also reads audio and video, places 7th, between Clef Flash and Jev, and is well
  calibrated (3.4%).
- Drex v1.5 costs about the same as Microsoft-Decision-1 and Kev 4B and places 9th, but its confidence runs high
  (10.8% calibration error).
- Solar Decide Flash has Solar Decide's 26-option limit, so it fails all 200 Banking77 cases; those count as wrong. It
  bills the same as Solar Decide.

## Round 3: Microsoft-Decision-1 (2026-10-12)

Microsoft released Microsoft-Decision-1 on 2026-10-09: a decision model post-trained from Qwen3.5-9B, served on
OpenRouter's Decisions API at $0.042 per 1M input tokens. It ran all 3,250 cases through the same gateway and scorer as
round 2, 8 calls in flight, served as `microsoft/microsoft-decision-1-20261009`. Every call succeeded.

| Model | Maker | Index | English | Arabic | Calibration error | Median latency | Cost per 1,000 calls |
|---|---|---|---|---|---|---|---|
| Decider V1 27B | Perplexity | **83.3** | 81.1 | **85.0** | 5.6% | 528 ms | $0.019 |
| d1 | Liquid AI | 82.7 | 81.3 | 83.9 | 2.9% | 659 ms | $0.015 |
| Mercury Decide | Inception | 82.4 | **83.7** | 80.8 | 13.1% | 490 ms | free tier |
| **Microsoft-Decision-1** | Microsoft | 82.0 | 81.0 | 83.2 | 2.8% | 679 ms | $0.010 |
| Clef | Cloudflare | 81.6 | 80.6 | 83.0 | **2.2%** | 706 ms | $0.116 |

- Microsoft-Decision-1 places 4th of 12 on the System One Index, 1.3 points behind Perplexity Decider V1 27B. It's 3rd
  on the Arabic index.
- It's the second-best calibrated model (2.8% calibration error), behind Cloudflare Clef (2.2%).
- It's the cheapest paid model at its accuracy: $0.034 for all 3,250 cases, about the same as Kev 4B, which scores
  5.2 points lower.
- It's the most accurate model on SST-5 (62.5%), typed-decisions (79.0%) and Arabic MIRACL pairs (91.0%). Its weakest
  dataset is Emotion (57.0%, against Mercury Decide's 91.5%).
- Median latency was 679 ms with 8 calls in flight and 613 ms one call at a time, both through OpenRouter and including
  the network. Jev measured 365 ms one at a time from the same machine on 2026-10-07, so part of that gap may be the
  day's network. Microsoft reports 85 ms p50 in its own test.

## Round 2: eleven models (2026-10-07)

Eight more models from OpenRouter's Decisions API, run the same day as Jev and GPT-6 Luna Decisions, all 3,250 cases.
The index is the mean accuracy across the 16 datasets, every dataset weighted equally. API latency is the median per call
through OpenRouter (8 calls in flight for Jev and GPT-6 Luna Decisions, 6 for the rest, Solar Decide finishing at 24);
Laya ran locally on an Apple M5 GPU.

| Model | Maker | Index | Calibration error | Median latency | Cost per 1,000 calls |
|---|---|---|---|---|---|
| **Decider V1 27B** | Perplexity | 83.3 | 5.6% | 528 ms | $0.019 |
| d1 | Liquid AI | 82.7 | 2.9% | 659 ms | $0.015 |
| Mercury Decide | Inception | 82.4 | 13.1% | 490 ms | free tier |
| Clef | Cloudflare | 81.6 | 2.2% | 706 ms | $0.116 |
| Clef Flash | Cloudflare | 80.3 | 3.5% | 534 ms | $0.044 |
| Jev 1.13 | TypeSafe | 79.0 | 6.1% | 372 ms | $0.028 |
| Kev 4B | Jared Palmer | 76.8 | 5.1% | 899 ms | $0.010 |
| GPT-6 Luna Decisions | OpenAI | 76.0 | 9.8% | 363 ms | $0.040 |
| Tev1 4B Experimental | Together AI | 71.5 | 5.3% | 518 ms | $0.019 |
| Solar Decide | Upstage | 68.8 | 20.3% | 1,231 ms | $0.042 |
| Laya Router | Convai Innovations | 60.4 | 20.0% | 75 ms | local |

- Five models beat Jev 1.13 on the index, led by Perplexity Decider V1 27B (83.3) and Liquid AI d1 (82.7). The top five
  are within 3 points of each other.
- Cloudflare Clef and Liquid AI d1 are the best calibrated (2.2% and 2.9% calibration error); Mercury Decide is accurate
  but overconfident (13.1%).
- Jev 1.13 and GPT-6 Luna Decisions remain the fastest API models (about 370 ms median). Kev 4B is the cheapest paid model.
- Together Tev1 accepts at most 20 options per question and Upstage Solar Decide at most 26, so each fails all 200
  Banking77 cases (77 options); failures count as wrong. Respan Span-01 only accepts conversations and wasn't run.
- Every price above is what OpenRouter billed; Mercury Decide ran on the free tier.

## Jev vs OpenAI Decisions (2026-10-07)

All 3,250 cases (4,850 decisions), both models through OpenRouter on the same day, 8 requests in flight. Models as served:
`typesafe/jev-1.13-20260917` and `openai/gpt-6-luna-decisions-20261006`. Nothing was tuned. OpenAI returned a 502 on
the same 2 cases on every retry (`ar_massive_intent-46`, `ar_miracl_rerank-177`); they count as wrong.

| Suite | n | Jev acc | OpenAI acc | Jev ECE | OpenAI ECE |
|---|---|---|---|---|---|
| AG News (4-way topic) | 200 | **0.885** | 0.875 | **0.086** | 0.112 |
| XNLI English | 150 | **0.860** | 0.667 | **0.082** | 0.207 |
| XNLI French | 150 | **0.767** | 0.620 | **0.122** | 0.215 |
| XNLI Arabic | 150 | **0.693** | 0.540 | **0.140** | 0.298 |
| DAIR Emotion (6-way) | 200 | 0.560 | **0.585** | 0.304 | **0.261** |
| SST-2 (noul) | 200 | **0.945** | 0.935 | 0.064 | **0.048** |
| BoolQ (noul) | 200 | **0.895** | 0.855 | **0.039** | 0.086 |
| SST-5 (5-level score) | 200 | **0.620** | 0.615 | 0.161 | **0.160** |
| Banking77 (77-way) | 200 | **0.790** | 0.775 | 0.101 | **0.087** |
| typed-decisions (5 q/case) | 400 | **0.727** | 0.711 | **0.040** | 0.084 |
| MASSIVE-ar scenario (18-way) | 200 | 0.630 | **0.660** | 0.210 | **0.168** |
| MASSIVE-ar intent (20 options) | 200 | 0.840 | **0.845** | **0.035** | 0.051 |
| OSACT4 offensive (noul) | 200 | 0.900 | **0.935** | 0.055 | **0.022** |
| Arabic tweet sentiment (3-way) | 200 | 0.760 | **0.800** | **0.097** | 0.107 |
| MIRACL-ar rerank (1 of 8) | 200 | **0.865** | 0.860 | 0.061 | **0.045** |
| MIRACL-ar pairwise (noul) | 200 | **0.905** | 0.875 | **0.027** | 0.107 |
| **All decisions** | 4,850 | **0.767** | 0.746 | **0.061** | 0.098 |

Log loss over all decisions: Jev 0.795, OpenAI 0.985. Brier: Jev 0.332, OpenAI 0.376.

Latency and cost:

| | Jev (OpenRouter) | OpenAI Decisions |
|---|---|---|
| 1 question, one in flight, p50 / p95 | 360 / 472 ms | **356 / 412 ms** |
| 5 questions, long state, one in flight, p50 / p95 | 376 / 585 ms | **363 / 428 ms** |
| 8 in flight, all cases, p50 / p95 | 372 / 469 ms | **363 / 460 ms** |
| Billed input tokens, whole run | 2.16 M | 1.31 M |
| Cost, whole run (`usage.cost`) | **$0.091** | $0.131 |
| Cost per 1,000 calls | **$0.028** | $0.040 |

- Jev is more accurate overall (+2.1 points) and better calibrated (ECE 0.061 vs 0.098). The gap is mostly NLI: XNLI
  English, French and Arabic are 15–19 points apart. Jev also leads on BoolQ, MIRACL pairwise and typed-decisions.
- OpenAI Decisions wins five suites: Arabic offensive, Arabic sentiment, MASSIVE-ar scenario and intent, and DAIR
  Emotion. Its biggest lead is Arabic sentiment (+4 points).
- Latency is a tie at p50, both about 360 ms through OpenRouter. OpenAI has a tighter tail, most visibly on 5-question
  calls (p95 428 vs 585 ms).
- OpenAI costs about 1.4× more for the same work. Its tokenizer counts 40% fewer input tokens, but it bills $0.10 per
  million against Jev's $0.042. Neither bills output tokens.
- Sanity check: Jev through OpenRouter scores 0.767 overall against 0.770 from the TypeSafe API on 2026-09-23. Same
  model, so the gateway doesn't change answers. OpenRouter was faster at p95 (469 vs 851 ms at 8 in flight).

## Laya vs Jev (2026-09-23, Apple M5, 24 GB)

Laya uses `Router()` as its model card recommends, with its shipped temperatures. Nothing was refit on test data.
Accuracy is scored against each dataset's label (typed-decisions: argmax of the soft gold).

| Suite | n | Laya acc | Jev acc | Laya ECE | Jev ECE |
|---|---|---|---|---|---|
| AG News (4-way topic) | 200 | **0.925** | 0.875 | **0.028** | 0.092 |
| XNLI English | 150 | 0.873 | **0.880** | **0.043** | 0.072 |
| XNLI French | 150 | 0.760 | **0.767** | 0.167 | **0.122** |
| XNLI Arabic | 150 | 0.680 | **0.693** | 0.234 | **0.143** |
| DAIR Emotion (6-way) | 200 | 0.535 | **0.565** | 0.351 | **0.300** |
| SST-2 (noul) | 200 | 0.885 | **0.945** | **0.049** | 0.065 |
| BoolQ (noul) | 200 | 0.815 | **0.895** | 0.093 | **0.037** |
| SST-5 (5-level score) | 200 | 0.340 | **0.635** | 0.381 | **0.181** |
| Banking77 (77-way) | 200 | 0.440 | **0.795** | 0.490 | **0.098** |
| typed-decisions (5 q/case) | 400 | 0.364 | **0.731** | 0.173 | **0.043** |
| **All decisions** | 3,650 | 0.510 | **0.755** | 0.181 | **0.058** |

Latency (one request in flight):

| | Laya on M5 GPU | Jev API |
|---|---|---|
| 1 question, p50 | **~89 ms** | ~400 ms |
| 5 questions, long state (typed-decisions), p50 | 1,140 ms | **~430 ms** |

Jev cost for the whole run: 1.30 M input tokens, about $0.055.

## Laya Arabic fine-tunes vs Jev (2026-09-25)

Adds [Wouze/laya-ara](https://huggingface.co/Wouze/laya-ara) (Arabic NLU fine-tune of laya-multilingual, non-commercial
licence) and [Wouze/laya-ara-rag](https://huggingface.co/Wouze/laya-ara-rag) (Arabic reranking fine-tune). Every model
runs as shipped. The Router sends Arabic to `laya-multilingual`, so its column is the stock base both fine-tunes start from.

| Suite (n=200, XNLI 150) | Router (stock) | laya-ara | laya-ara-rag | Jev | In fine-tune training? |
|---|---|---|---|---|---|
| XNLI-ar (NLI, 3-way) | 0.680 | **0.753** | 0.700 | 0.693 | laya-ara: capped XNLI-ar sample |
| MASSIVE scenario (18-way) | 0.390 | **0.695** | 0.605 | 0.635 | laya-ara: train split |
| MASSIVE intent (20 options) | 0.325 | 0.775 | 0.550 | **0.830** | laya-ara: train split |
| OSACT4 offensive (noul) | 0.825 | 0.885 | 0.845 | **0.895** | laya-ara: train split |
| Tweet sentiment (3-way) | 0.370 | 0.490 | 0.440 | **0.760** | no model (zero-shot) |
| MIRACL rerank (1 of 8 passages) | 0.315 | 0.320 | 0.715 | **0.875** | laya-ara-rag: MIRACL train |
| MIRACL pairwise relevance (noul) | 0.820 | 0.745 | 0.865 | **0.905** | laya-ara-rag: MIRACL train |
| **Mean of 7 suites** | 0.532 | 0.666 | 0.674 | **0.799** | |
| Latency p50 / p95 | **47 / 83 ms** | 54 / 125 ms | 58 / 127 ms | 396 / 550 ms | |

- Each fine-tune lifts the stock base a lot on its own task family: laya-ara on MASSIVE (+30–45 points), laya-ara-rag
  on MIRACL rerank (+40 points). laya-ara-rag's MASSIVE gains come from the small MASSIVE-ar sample in its training
  mix. laya-ara doesn't improve on reranking, and neither fine-tune closes the gap on sentiment, which no model trained on.
- laya-ara beats Jev on XNLI-ar and MASSIVE scenario, but it trained on XNLI-ar and MASSIVE-ar data. Jev leads
  everywhere else, including sentiment, the one fully zero-shot suite.
- Laya variants are 7–8× faster per call on short Arabic inputs. Jev latency was measured at 8 requests in flight;
  sequential p50 was about 400 ms, so the ratio holds.
- Our scores differ from the model cards (for example laya-ara scenario 0.695 here vs 0.865 on its card). The cards
  use their own frozen prompt templates, while every model here gets the same English instructions and criteria.

## Laya takeaways

- Laya is 4–5× faster on short single-question calls and edges Jev on AG News. It is roughly even on XNLI
  (including Arabic and French).
- It falls well behind on ordinal scores (SST-5), high-cardinality choices (Banking77) and multi-question
  structured states (typed-decisions, where it sits below the 0.47 majority-class baseline). This matches the
  model card's own "honest limits" section.
- The card's 0.766 typed-decisions number comes from `laya-typed-decisions`, a checkpoint fine-tuned on that
  benchmark's train split (a specialist). It is not comparable to a zero-shot generalist.
- With several questions per call, Laya on MPS is slower than Jev: each question re-encodes the whole state as its
  own sequence (batched, fp32 on MPS), so five questions cost about five times the compute. The card's ~33 ms figures are for a CUDA GPU.
- Caveat: Laya's training families include topic, emotion, NLI and intent tasks, so some public test sets may
  overlap its training data.

## Contributing, conduct and security

- **Add a model or change the data** under the [benchmark rules](CONTRIBUTING.md); the
  [PR template](.github/pull_request_template.md) checks each one. Or [request a model](https://github.com/alilibx/system-one-bench/issues/new?template=request-a-model.yml)
  and we'll run it.
- **Found a wrong score, label or case?** [Report it](https://github.com/alilibx/system-one-bench/issues/new?template=report-a-problem.yml).
- Everyone here follows the [code of conduct](CODE_OF_CONDUCT.md). Report security issues privately, as
  [SECURITY.md](SECURITY.md) describes.

[![Contributors](https://contrib.rocks/image?repo=alilibx/system-one-bench)](https://github.com/alilibx/system-one-bench/graphs/contributors)
