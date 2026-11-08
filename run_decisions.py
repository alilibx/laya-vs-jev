"""Send every case to a decision model. Resumable: skips ids already in the output file.

By default it calls OpenRouter's Decisions API, which serves most decision models behind one endpoint with one request
and response shape. --provider points it at a vendor's own System One endpoint instead (same request body), and --url
at any other one, such as a local server.

Usage: OPENROUTER_API_KEY=... python run_decisions.py --model openai/gpt-6-luna-decisions --name luna
       OPENROUTER_API_KEY=kerstel://global/OPENROUTER_API_KEY ks run -- python run_decisions.py --model typesafe/jev-1.13 --name or_jev
       CELERIS_API_KEY=kerstel://global/CELERIS_API_KEY ks run -- python run_decisions.py --provider celeris --name celeris
       python run_decisions.py --url http://localhost:8000/v1/systemone --key-env "" --model kev-9b --name kev_9b
Writes preds_<name>.jsonl and, once, latency_<name>.jsonl (one request in flight at a time).

Image cases (build_images.py) run the same way: --cases image_cases.jsonl --out-dir vision. Their state holds
{"image": path} items, sent as image_url parts with a base64 data URL. --suites limits a run to some suites, such as
img_refcoco for the models that answer Box questions.

The cases must match data.lock.json, so every model runs on the same frozen data; --unverified skips that check for a
run that isn't for the board.
"""
import argparse
import asyncio
import base64
import json
import os
import random
import time

import httpx

import data_lock

URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai") + "/api/alpha/decisions"
# Vendors' own System One endpoints: (url, model, env var holding the key, auth header, USD per 1M input tokens).
# Same request body as above. The price fills in usage.cost when a vendor reports tokens but no cost; output is free.
PROVIDERS = {
    "fastino": ("https://api.fastino.ai/v1/systemone", "fastino/GLiDE", "FASTINO_API_KEY", "x-api-key", 0.04),
    "celeris": ("https://inference.celeris.ai/celeris-1-decision/v1/systemone", "celeris-1-decision", "CELERIS_API_KEY", "bearer", 0.04),
    "hanzo": ("https://api.hanzo.ai/v1/decisions", "kai", "HANZO_API_KEY", "bearer", 0.021),
    "meragpt": ("https://meragpt.com/v1/systemone", "decider-1", "MERAGPT_API_KEY", "bearer", 0.04),
}


def usd(x):
    """A cost as a number: meraGPT reports it as a string, such as "$0.000007"."""
    return float(x.strip().lstrip("$")) if isinstance(x, str) else x


def priced(usage, per_m):
    """usage with a USD cost: the reported one, meraGPT's cost_usd, or input tokens at the listed price."""
    if not usage:
        return usage
    if usage.get("cost") is not None:
        return {**usage, "cost": usd(usage["cost"])}
    if usage.get("cost_usd") is not None:
        return {**usage, "cost": usd(usage["cost_usd"])}
    if per_m and usage.get("input_tokens") is not None:
        return {**usage, "cost": usage["input_tokens"] * per_m / 1e6, "cost_from_list_price": True}
    return usage


MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def with_images(x):
    """Replace every {"image": path} with the image_url part the Decisions API reads, as a base64 data URL."""
    if isinstance(x, dict) and set(x) == {"image"}:
        with open(x["image"], "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return {"type": "image_url", "image_url": {"url": f"data:{MIME[os.path.splitext(x['image'])[1]]};base64,{data}"}}
    if isinstance(x, dict):
        return {k: with_images(v) for k, v in x.items()}
    if isinstance(x, list):
        return [with_images(v) for v in x]
    return x


async def call(client, url, model, case, per_m=None):
    body = {"model": model, "state": with_images(case["state"]), "questions": with_images(case["questions"])}
    for attempt in range(8):
        t0 = time.perf_counter()
        try:
            r = await client.post(url, json=body)
        except httpx.TransportError as e:
            err = repr(e)
        else:
            ms = (time.perf_counter() - t0) * 1000
            if r.status_code == 200:
                d = r.json()
                return {"id": case["id"], "answers": d["answers"], "usage": priced(d.get("usage"), per_m), "model": d.get("model"),
                        "provider": d.get("provider"), "ms": ms}
            if r.status_code not in (408, 429, 500, 502, 503, 504, 529):
                return {"id": case["id"], "error": f"{r.status_code} {r.text[:300]}", "ms": ms}
            err = f"{r.status_code}"
        await asyncio.sleep(min(30, 2 ** attempt) + random.random())
    return {"id": case["id"], "error": f"gave up: {err}"}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", help="model id, e.g. openai/gpt-6-luna-decisions; defaults to the provider's model")
    ap.add_argument("--provider", choices=PROVIDERS, help="call a vendor's own endpoint instead of OpenRouter")
    ap.add_argument("--url", help="any endpoint that takes the System One request body, e.g. a local server")
    ap.add_argument("--key-env", help="env var holding the API key; empty for none (default OPENROUTER_API_KEY)")
    ap.add_argument("--auth", choices=["bearer", "x-api-key"], help="how the key is sent (default bearer)")
    ap.add_argument("--name", required=True, help="short name for the output files")
    ap.add_argument("--cases", default="cases.jsonl", help="cases file, e.g. image_cases.jsonl")
    ap.add_argument("--suites", help="comma-separated suites to run (default: every suite in the cases file)")
    ap.add_argument("--out-dir", default=".", help="folder for the output files, e.g. vision")
    ap.add_argument("--unverified", action="store_true", help="run even if the cases don't match data.lock.json")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--sequential-latency", type=int, default=60, help="single-question cases timed one at a time")
    a = ap.parse_args()
    url, model, key_env, auth, per_m = PROVIDERS.get(a.provider, (URL, None, "OPENROUTER_API_KEY", "bearer", None))
    url = a.url or url
    model = a.model or model
    key_env = key_env if a.key_env is None else a.key_env
    auth = a.auth or auth
    if not model:
        ap.error("--model is required unless --provider sets it")
    if key_env and not os.environ.get(key_env):
        ap.error(f"{key_env} is not set: export it, wrap the command in `ks run --` with a kerstel:// reference, "
                 f"or pass --key-env \"\" for an endpoint without a key")
    os.makedirs(a.out_dir, exist_ok=True)
    out, lat_path = os.path.join(a.out_dir, f"preds_{a.name}.jsonl"), os.path.join(a.out_dir, f"latency_{a.name}.jsonl")
    cases = [json.loads(l) for l in open(a.cases)]
    if a.suites:
        cases = [c for c in cases if c["suite"] in a.suites.split(",")]
    problems = [] if a.unverified else data_lock.check(a.cases, {c["suite"] for c in cases})
    if problems:
        ap.error(f"{a.cases} doesn't match data.lock.json, so results wouldn't compare with the board:\n  " + "\n  ".join(problems)
                 + "\nRebuild it with the build_*.py scripts, or pass --unverified for a run that isn't for the board.")
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["id"] for l in open(out) if "error" not in json.loads(l)}
    todo = [c for c in cases if c["id"] not in done]
    headers = {}
    if key_env:
        k = os.environ[key_env].strip()
        headers = {"X-API-Key": k} if auth == "x-api-key" else {"Authorization": f"Bearer {k}"}
    async with httpx.AsyncClient(headers=headers, timeout=60) as client:
        # Latency probe: one request in flight at a time, like a single interactive caller.
        if a.sequential_latency and not os.path.exists(lat_path) and any(c["suite"] == "ag_news" for c in cases):
            probe = [c for c in cases if c["suite"] == "ag_news"][: a.sequential_latency]
            probe += [c for c in cases if c["suite"] == "typed-decisions"][: a.sequential_latency // 2]
            await call(client, url, model, probe[0], per_m)  # warm the connection
            with open(lat_path, "w") as f:
                for c in probe:
                    r = await call(client, url, model, c, per_m)
                    f.write(json.dumps({"id": c["id"], "suite": c["suite"], "nq": len(c["questions"]), "ms": r.get("ms"),
                                        "error": r.get("error")}) + "\n")
                    f.flush()
            print("latency probe done")
        sem = asyncio.Semaphore(a.concurrency)
        n = 0

        async def one(c):
            async with sem:
                return await call(client, url, model, c, per_m)

        with open(out, "a") as f:
            for fut in asyncio.as_completed([one(c) for c in todo]):
                r = await fut
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                f.flush()
                n += 1
                if n % 100 == 0:
                    print(n, "/", len(todo), flush=True)
    print("done", n)


asyncio.run(main())
