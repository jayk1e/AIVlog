#!/usr/bin/env python3
"""
Shared Veo 3.1 generation engine for AIVlog.

Every episode is a tiny config module that defines NARRATOR + PROMPTS and calls
`veo_engine.run(__file__, ...)`. All the actual logic lives here, once — fix a bug
here and every series benefits.

Reference-image resolution (first match wins):
    1. <episode dir>/refs/          per-episode override
    2. <series dir>/refs/           per-series override
    3. AIVlog/refs/                 global default face

Clips for an episode land in <series>/clips/<episode_slug>/clip_NN.mp4, so multiple
episodes can live flat in one series folder without colliding.

See ../README.md and ../VEO_API_NOTES.md for the full process and API quirks.
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# AIVlog root = two levels up from this file (AIVlog/lib/veo_engine.py -> AIVlog)
AIVLOG_ROOT = Path(__file__).resolve().parent.parent
GLOBAL_REFS = AIVLOG_ROOT / "refs"

# Load the shared key from AIVlog/.env (episodes never need their own).
load_dotenv(AIVLOG_ROOT / ".env")

# ---- defaults (an episode can override any via run() kwargs) ----------------
DEFAULTS = dict(
    model="veo-3.1-fast-generate-preview",   # Fast=$0.10/s; "veo-3.1-generate-preview"=4x
    aspect_ratio="9:16",                      # "16:9" for YouTube landscape
    resolution="720p",                        # "1080p"=$0.12/s on Fast
    duration_seconds=8,                       # required = 8 with reference images
    reference_images=["me1.jpg", "me2.jpg", "me3.jpg"],  # up to 3
    poll_seconds=10,
)


def get_client():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit(f"ERROR: GEMINI_API_KEY not found. Put it in {AIVLOG_ROOT/'.env'} "
                 "as GEMINI_API_KEY=your_key_here")
    return genai.Client(api_key=key)


def resolve_refs_dir(episode_dir, series_dir):
    """episode/refs -> series/refs -> global AIVlog/refs (first that exists)."""
    for d in (episode_dir / "refs", series_dir / "refs", GLOBAL_REFS):
        if d.is_dir() and any(d.glob("*.jpg")):
            return d
    return GLOBAL_REFS  # may be empty; load_ref_images will warn


def load_ref_images(refs_dir, names):
    refs = []
    for name in names[:3]:
        path = refs_dir / name
        if path.exists():
            img = types.Image(image_bytes=path.read_bytes(), mime_type="image/jpeg")
            refs.append(types.VideoGenerationReferenceImage(
                image=img,
                reference_type=types.VideoGenerationReferenceType.ASSET,
            ))
    print(f"loaded {len(refs)} reference image(s) from {refs_dir}")
    if not refs:
        print("  (no refs found - clips generate but the face won't be locked. "
              f"Add me1/2/3.jpg to {refs_dir}.)")
    return refs


def build_config(cfg, ref_images):
    # Developer-API-safe fields ONLY. seed/generate_audio/negative_prompt are
    # Vertex-only and hard-fail on an AI Studio key. Audio is on by default.
    kwargs = dict(
        aspect_ratio=cfg["aspect_ratio"],
        resolution=cfg["resolution"],
        duration_seconds=cfg["duration_seconds"],
        number_of_videos=1,
    )
    if ref_images:
        kwargs["reference_images"] = ref_images
    return types.GenerateVideosConfig(**kwargs)


def generate(client, cfg, clips_dir, index, prompt_text, narrator, config):
    prompt = prompt_text.format(you=narrator)
    print(f"\n=== Clip {index} === submitting...")
    op = client.models.generate_videos(model=cfg["model"], prompt=prompt, config=config)
    while not op.done:
        time.sleep(cfg["poll_seconds"])
        op = client.operations.get(op)
        print("  ...rendering")
    if op.error:
        print(f"  clip {index} ERROR from API: {op.error}")
        return
    gen = op.response.generated_videos[0]
    client.files.download(file=gen.video)
    out = clips_dir / f"clip_{index:02d}.mp4"
    gen.video.save(str(out))
    print(f"  saved {out}")


def preflight(client, cfg):
    print(f"Preflight: model={cfg['model']}, {cfg['resolution']}, "
          f"{cfg['duration_seconds']}s, {cfg['aspect_ratio']}")
    try:
        client.models.get(model=cfg["model"])
        print("  key can see the Veo model. (Generation needs PAID tier - a "
              "429/permission error on clip 1 means enable billing.)")
    except Exception as e:
        print(f"  WARNING: could not fetch model info ({e}). Continuing.")


def parse_clip_arg(argv, n_prompts, test_only):
    """(no args)->[1] if test_only else all; --all; --clips 5 / 5,7 / 3-6."""
    if "--all" in argv:
        return list(range(1, n_prompts + 1))
    if "--clips" in argv:
        raw = argv[argv.index("--clips") + 1]
        picks = set()
        for part in raw.split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-")
                picks.update(range(int(a), int(b) + 1))
            elif part:
                picks.add(int(part))
        picks = sorted(i for i in picks if 1 <= i <= n_prompts)
        if not picks:
            sys.exit(f"No valid clip numbers in --clips (valid: 1-{n_prompts}).")
        return picks
    return [1] if test_only else list(range(1, n_prompts + 1))


def run(episode_file, *, narrator, prompts, slug=None, test_only=True, **overrides):
    """Entry point an episode config calls.

    episode_file : pass __file__ from the episode module.
    narrator     : the NARRATOR description string.
    prompts      : list of prompt strings (one per 8s clip).
    slug         : episode short name -> clips/<slug>/ . Defaults to the file stem.
    test_only    : if no CLI args, render only clip 1.
    overrides    : model / aspect_ratio / resolution / reference_images / etc.
    """
    cfg = {**DEFAULTS, **overrides}
    episode_path = Path(episode_file).resolve()
    episode_dir = episode_path.parent          # the series folder (episodes are flat)
    series_dir = episode_dir
    slug = slug or episode_path.stem           # e.g. "episode01"

    clips_dir = series_dir / "clips" / slug
    clips_dir.mkdir(parents=True, exist_ok=True)

    refs_dir = resolve_refs_dir(episode_dir, series_dir)

    argv = sys.argv[1:]
    indices = parse_clip_arg(argv, len(prompts), test_only)

    client = get_client()
    preflight(client, cfg)
    refs = load_ref_images(refs_dir, cfg["reference_images"])
    vconfig = build_config(cfg, refs)

    est = len(indices) * cfg["duration_seconds"] * (0.10 if "fast" in cfg["model"] else 0.40)
    print(f"\nEpisode '{slug}' -> {clips_dir}")
    print(f"Rendering clip(s) {indices}. Estimated cost: ~${est:.2f}")
    for i in indices:
        try:
            generate(client, cfg, clips_dir, i, prompts[i - 1], narrator, vconfig)
        except Exception as e:
            print(f"  clip {i} FAILED: {e}")
    print(f"\nDone. Stitch with:  {AIVLOG_ROOT/'lib'/'stitch.sh'} {slug}")
    print(f"Re-render a drifted clip:  python {episode_path.name} --clips 5")
