# Veo 3.1 via Gemini Developer API — hard-won notes

Verified empirically 2026-07-05 with `google-genai 2.10.0` and an **AI Studio
(Gemini Developer API)** key — NOT Vertex AI. These matter because the SDK
*exposes* config fields that the Developer API then *rejects* at request time.

## Auth
- A standard `GEMINI_API_KEY` from AI Studio **works for Veo** — but only on the
  **paid tier** (billing enabled). Free tier returns "not available".
- Our key (from `Deal_Analyzer/.env`) is confirmed paid-tier: clip 1 rendered fine.

## Config fields — what the Developer API ACCEPTS
`GenerateVideosConfig(...)`:
- `aspect_ratio`      ("9:16" or "16:9")  ✅
- `resolution`        ("720p" / "1080p")  ✅
- `duration_seconds`  (8 required w/ reference images)  ✅
- `number_of_videos`  ✅
- `reference_images`  (up to 3, Ingredients-to-Video, `reference_type=ASSET`)  ✅

## Config fields that FAIL on the Developer API (Vertex/Enterprise ONLY)
These raise `"... only supported in Gemini Enterprise Agent Platform mode,
not in Gemini Developer API mode"` and cost nothing (rejected pre-billing),
EXCEPT they block the whole request:
- `seed`             ❌  (so re-renders are NOT reproducible on this key)
- `generate_audio`   ❌  (but audio is ON BY DEFAULT for Veo 3 — don't set the flag)
- `negative_prompt`  ❌  (400 INVALID_ARGUMENT "Negative prompt is not supported")

Workarounds baked into `generate_veo_clips.py`:
- Audio: rely on the default (works — clip 1 has 48kHz AAC).
- Negative prompt: fold the "avoid X" intent into the POSITIVE prompt text
  (e.g. "background signage stays soft, blurred, out of focus, no readable text").
- Seed: none available; each re-render is a fresh roll. Re-render drifted clips
  individually with `--clips N` until you get a good take.

## Gotcha that cost money
Probing "which fields are accepted" by calling `generate_videos` — **ACCEPTED ==
a real billable job submitted**, even if you never poll it. Cost ~$0.80 each.
To test field validity cheaply, validate the pydantic model client-side, or
accept that a successful submit = a charge. (Burned ~$3.20 learning this.)

## Cost actuals (Veo 3.1 Fast, 720p, 8s)
$0.10/s → $0.80/clip → 9 clips ≈ $7.20. Standard model is 4×.
