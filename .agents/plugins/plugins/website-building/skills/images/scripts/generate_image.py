#!/usr/bin/env python3
"""Generate a website image with the OpenAI image API (standard library only).

Needs OPENAI_API_KEY in the environment (load it from .env yourself; never print it).
This spends money: use --dry-run first to see exactly what would be sent.

Example:
  python3 generate_image.py --dry-run --prompt "warm sunlit desk" \
      --brand output/BRAND.md --out public/site/assets/hero.png
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

MODEL = "gpt-image-2-2026-04-21"
NO_TEXT = " No text, no letters, no logos, no watermark."
WITH_TEXT = (" Render all text crisply, spelled exactly as quoted. "
             "No other text anywhere. No watermark.")


def brand_hint(path):
    """Pull colour hex codes and the first mood line from BRAND.md so images match."""
    if not path or not os.path.exists(path):
        return ""
    text = open(path, encoding="utf-8").read()
    import re
    colours = list(dict.fromkeys(re.findall(r"#[0-9a-fA-F]{6}\b", text)))[:5]
    return " Brand colours: %s. Warm, editorial, matte, subtle grain." % ", ".join(colours) if colours else ""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prompt", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--brand", help="path to BRAND.md; its hex colours are added to the prompt")
    p.add_argument("--with-text", action="store_true",
                   help="the image carries quoted words (social card); default is text-free")
    p.add_argument("--size", default="1536x1024", choices=["1024x1024", "1536x1024", "1024x1536"])
    p.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    p.add_argument("--model", default=MODEL)
    p.add_argument("--dry-run", action="store_true", help="print the request, send nothing, spend nothing")
    a = p.parse_args()

    prompt = a.prompt.rstrip() + brand_hint(a.brand) + (WITH_TEXT if a.with_text else NO_TEXT)
    body = {"model": a.model, "prompt": prompt, "size": a.size, "n": 1, "quality": a.quality}

    if a.dry_run:
        print("DRY RUN - nothing sent, nothing spent.")
        print(json.dumps(body, indent=2))
        print("Would save to: %s" % a.out)
        return

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY is not set. Use hand-built SVG or CSS gradients instead, and keep "
                 "this command in an HTML comment where the image goes.")

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("HTTP %s from OpenAI: %s" % (e.code, e.read().decode(errors="replace")[:400]))
    except urllib.error.URLError as e:
        sys.exit("Network error: %s" % e.reason)

    data = [d.get("b64_json") for d in resp.get("data", []) if d.get("b64_json")]
    if not data:
        sys.exit("No image returned: %s" % json.dumps(resp)[:300])
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "wb") as f:
        f.write(base64.b64decode(data[0]))
    print("saved %s" % a.out)


if __name__ == "__main__":
    main()
