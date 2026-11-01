# Plan: the reference benchmark for decision models

System One Bench is useful only if people use its numbers: model makers when they ship, teams when they pick a model,
researchers when they compare methods. This plan lists what gets it there. Items move to done as they ship, with the
pull request that shipped them.

**What doesn't change:** only scores measured here go on the board, every model runs under the
[same rules](../CONTRIBUTING.md), and corrections are published openly. Reach never comes at the cost of neutrality.

## 1. Easy to find, share and cite

- [x] Link previews: Open Graph and Twitter card tags, a card image, and a favicon, so shared links show a title and
  image on LinkedIn, X, Slack and Discord.
- [x] Licence: Apache-2.0 for the code, CC BY 4.0 for the results, and the source datasets' own licences for the cases.
- [x] `CITATION.cff`, so GitHub offers "Cite this repository".
- [x] `robots.txt` and `sitemap.xml`.
- [x] One page per model, and pages comparing two models, generated from the results at deploy time, so searches for a
  model's name find its results.
- [x] Analytics that respect privacy, to see which channels bring readers: page views only, no cookies.
- [ ] A short technical report on arXiv: the method (frozen data, identical requests, calibration, latency from one
  machine) and the findings, such as what reading text from pixels costs in Arabic.
- [ ] Results and per-case predictions as a Hugging Face dataset, and a leaderboard Space. Only data whose licence
  allows redistribution.

## 2. Quick, fair coverage of new models

- [ ] Score every new decision model within 48 hours of release, and say so on the site.
- [ ] Share results with the model's maker a day before publishing, so mistakes are caught before they go out.
- [x] A "Request a model" issue form, so anyone can ask for a run in public.
- [x] A badge model makers can put on their model card, linking to that model's results.
- [ ] Run the open-weight roadmap locally (Liquid AI d1-3B and d1-omni-600M, the Kev sizes, the Naluri encoders,
  vLLM d3) and add a local-hardware latency chart.
- [ ] The models on their own APIs (Celeris-1 Decision, Hanzo Kai 1, meraGPT Decider 1) once keys are in place.

## 3. Something people use, not just read

- [x] Every round is a [GitHub release](https://github.com/alilibx/system-one-bench/releases), with an Atom feed to
  follow.
- [ ] Score your own model in one command (a pip package or a GitHub Action), so teams can run the benchmark in their
  own CI.
- [ ] A hosted live race with a spending cap.
- [ ] A stable JSON endpoint for the results, documented, for dashboards and papers.

## 4. Reaching people

- [ ] One finding per round, written up as a short post with a chart. Findings travel further than leaderboards.
- [ ] Show HN, r/LocalLLaMA (with the open-weight runs), r/MachineLearning, X and Bluesky, tagging the makers.
- [ ] Arabic NLP communities and MENA tech press: few benchmarks test decision models in Arabic.
- [ ] AI newsletters and podcasts, with one finding each.
- [ ] Ask OpenRouter to link the board from its Decisions API docs, since every API model here runs through it.

## 5. Trust

- [ ] State any ties between the maintainers and a model maker on the site.
- [ ] Show independent reproductions: when someone else re-runs a model and matches the score, say so.
- [ ] A submission to the NeurIPS Datasets and Benchmarks track.
