#!/usr/bin/env python3
"""Imagen 4 Fast background generator for GCSE Boss Daily Content Agent.

Usage:
    python3 gemini_background.py --out /path/source-YYYY-MM-DD.png --prompt "..." [--prompt "...fallback..."]

Tries each prompt in order. Advances on safety-filter block (HTTP 200, empty body).
Prints the index of the prompt that succeeded to stdout as `VARIANT=<n>`.
"""
import argparse, base64, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

BASE = "https://generativelanguage.googleapis.com/v1beta/models"
SUFFIX = "no text, no letters, no logos, no watermarks"

# 2026-08-24: imagen-4.0-fast-generate-001 now returns HTTP 404 NOT_FOUND on this
# key ("not found for API version v1beta, or is not supported for predict").
# The account's available image models are the generateContent-based Gemini image
# family. MODELS is tried in order; the first that responds wins. The Imagen
# predict path is retained first so the pipeline self-heals if it is restored.
MODELS = [
    ("imagen-4.0-fast-generate-001", "predict"),
    ("gemini-3.1-flash-image", "generateContent"),
    ("gemini-2.5-flash-image", "generateContent"),
]


def load_env(env_path):
    if not Path(env_path).exists():
        return
    for line in Path(env_path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def _payload(model, method, prompt, aspect):
    if method == "predict":
        return {"instances": [{"prompt": prompt}],
                "parameters": {"sampleCount": 1, "aspectRatio": aspect,
                               "personGeneration": "allow_adult"}}
    return {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": aspect}}}


def _extract(method, data):
    """Return raw image bytes, or raise RuntimeError('SAFETY') on empty result."""
    if method == "predict":
        preds = data.get("predictions") or []
        if not preds:
            raise RuntimeError("SAFETY")
        return base64.b64decode(preds[0]["bytesBase64Encoded"])
    cands = data.get("candidates") or []
    if not cands:
        raise RuntimeError("SAFETY")
    reason = cands[0].get("finishReason")
    for part in (cands[0].get("content") or {}).get("parts") or []:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            return base64.b64decode(inline["data"])
    raise RuntimeError(f"SAFETY (finishReason={reason})")


def _call(model, method, prompt, api_key, aspect, attempts=3):
    """One prompt against one model, with backoff on transient errors only.
    Raises RuntimeError('SAFETY...') on a safety block, or 'HTTP 404...' if the
    model is gone (caller advances to the next model)."""
    url = f"{BASE}/{model}:{method}"
    body = json.dumps(_payload(model, method, prompt, aspect)).encode()
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(
                url, data=body, headers={"x-goog-api-key": api_key,
                                         "Content-Type": "application/json"})
            return _extract(method, json.loads(
                urllib.request.urlopen(req, timeout=180).read()))
        except RuntimeError:
            raise
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:300]
            last = f"HTTP {e.code}: {detail}"
            if e.code in (400, 401, 403, 404):
                raise RuntimeError(last)   # not transient, do not retry
            time.sleep(2 ** i)
        except Exception as e:  # noqa: BLE001
            last = repr(e)
            time.sleep(2 ** i)
    raise RuntimeError(f"exhausted retries: {last}")


def generate(prompt, api_key, aspect="9:16", attempts=3):
    """Try each model in MODELS until one produces an image.
    Re-raises the SAFETY error if a live model blocks the prompt, so the caller
    advances to the next prompt variant rather than the next model."""
    full = prompt if SUFFIX in prompt else f"{prompt}, {SUFFIX}"
    errs = []
    for model, method in MODELS:
        try:
            img = _call(model, method, full, api_key, aspect, attempts)
            sys.stderr.write(f"  [model {model}] ok\n")
            return img
        except RuntimeError as e:
            msg = str(e)
            sys.stderr.write(f"  [model {model}] {msg[:150]}\n")
            if msg.startswith("SAFETY"):
                raise            # live model, prompt refused: try next prompt
            errs.append(f"{model}: {msg[:120]}")
    raise RuntimeError("no image model reachable | " + " | ".join(errs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--prompt", action="append", required=True)
    ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--env", default="/sessions/serene-funny-hawking/mnt/GCSEBoss/.env")
    a = ap.parse_args()

    load_env(a.env)
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("FATAL: GEMINI_API_KEY not set", file=sys.stderr)
        return 2

    for idx, p in enumerate(a.prompt, 1):
        sys.stderr.write(f"[variant {idx}] {p[:110]}...\n")
        try:
            img = generate(p, key, a.aspect)
        except RuntimeError as e:
            sys.stderr.write(f"[variant {idx}] BLOCKED/ERROR: {e}\n")
            continue
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_bytes(img)
        print(f"VARIANT={idx}")
        print(f"OUT={a.out}")
        print(f"BYTES={len(img)}")
        return 0

    print("FATAL: all prompt variants blocked", file=sys.stderr)
    return 3


if __name__ == "__main__":
    sys.exit(main())
